"""Calculate Income vs expenses
"""
import argparse
import collections
import datetime
import logging
import os
from functools import partial
from os import path
from typing import Dict, List, Tuple

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from beancount import loader
from beancount.core import (account_types, convert, data, display_context,
                            getters, inventory, prices)
from beancount.core.number import Decimal
from beancount.parser import options, printer
from google.protobuf import text_format

from income_expense_config_pb2 import IncomeExpenseConfig
from monthly_expenses import compute_monthly_expenses, compute_monthly_income

Date = datetime.date
Month = str


def read_config(
    config_filename: str,
) -> IncomeExpenseConfig:
    """Read the configuration, perform globbing expansions, and whittle down the
    list of reports and investments to the requested minimal."""

    # Read the file.
    config = IncomeExpenseConfig()
    with open(config_filename, "r") as infile:
        text_format.Merge(infile.read(), config)
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip())

    parser.add_argument("ledger", help="Beancount ledger file")
    parser.add_argument(
        "config", action="store", help="Configuration for accounts and reports"
    )
    parser.add_argument(
        "output", help="Output directory to write all output files to."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose mode"
    )
    parser.add_argument(
        "-s",
        "--start-date",
        action="store",
        type=datetime.date.fromisoformat,
        help="The start date to compute from.",
    )
    parser.add_argument(
        "-e",
        "--end-date",
        action="store",
        type=datetime.date.fromisoformat,
        help="The end date to compute to.",
    )
    parser.add_argument(
        "--pdf",
        "--pdfs",
        action="store_true",
        help="Render as PDFs. Default is HTML directories.",
    )

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG, format="%(levelname)-8s: %(message)s"
        )
        logging.getLogger("matplotlib.font_manager").disabled = True

    # TODO:make this configurable
    decimal_precison = "0.00"
    Q = Decimal(decimal_precison)

    # Load the example file.
    logging.info("Reading ledger: %s", args.ledger)
    entries, _, options_map = loader.load_file(args.ledger)
    # accounts = getters.get_accounts(entries)
    dcontext = options_map["dcontext"]
    acctypes = options.get_account_types(options_map)
    price_map = prices.build_price_map(entries)

    # Figure out start and end date.
    start_date = args.start_date or entries[0].date
    end_date = args.end_date or datetime.date.today()

    # Load, filter and expand the configuration.
    config = read_config(args.config)
    os.makedirs(args.output, exist_ok=True)
    with open(path.join(args.output, "config.pbtxt"), "w") as efile:
        print(config, file=efile)

    pruned_entries: List[data.Transaction] = data.filter_txns(entries)
    pruned_entries = prune_date_range(pruned_entries, start_date, end_date)
    pruned_entries = prune_non_budget_transactions(pruned_entries, config)

    income_data = compute_monthly_income(pruned_entries, acctypes, price_map, Q)
    expense_data = compute_monthly_expenses(
        pruned_entries, acctypes, price_map, Q
    )
    write_html(args.output, "Income vs Expenses", income_data, expense_data)


def prune_date_range(
    entries: List[data.Transaction], start: Date, end: Date
) -> List[data.Transaction]:
    """Prune the entriet to contain only those that fall within date range"""
    return [
        entry for entry in entries if entry.date >= start and entry.date <= end
    ]


def prune_non_budget_transactions(
    txns: List[data.Transaction], config: IncomeExpenseConfig
) -> List[data.Transaction]:
    """Prune the entriet to contain only those that include an account from
    the budget accounts"""
    accounts = set()
    accounts.update(config.budget_accounts)
    return [
        txn
        for txn in txns
        if any(posting.account in accounts for posting in txn.postings)
    ]


def write_month_file(
    dcontext: display_context.DisplayContext,
    entries: data.Entries,
    filename: str,
):
    """Write out a file with details, for inspection and debugging."""
    logging.info("Writing details file: %s", filename)
    epr = printer.EntryPrinter(dcontext=dcontext, stringify_invalid_types=True)
    os.makedirs(path.dirname(filename), exist_ok=True)
    with open(filename, "w") as outfile:
        fprint = partial(print, file=outfile)
        fprint(";; -*- mode: beancount; coding: utf-8; fill-column: 400 -*-")
        for entry in entries:
            fprint(epr(entry))


STYLE = """
@media print {
    @page { margin: 0in; }
    body { margin: 0.2in; }
    .new-page { page-break-before: always; }
}
body, table { font: 9px Noto Sans, sans-serif; }
p { margin: 0.2em; }
table { border-collapse: collapse; }
table td, table th { border: thin solid black; }
table.full { width: 100%; }
/* p { margin-bottom: .1em } */
"""

RETURNS_TEMPLATE_PRE = """
<html>
  <head>
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap" rel="stylesheet">
    <style>
      {style}
    </style>
  <head>
    <body>
      <h1>{title}</h1>
"""
RETURNS_TEMPLATE_POST = """
    </body>
</html>
"""


def write_html(
    dirname: str,
    title: str,
    income_data: Tuple[List[Tuple[int, int]], List[List[str]]],
    expense_data: Tuple[List[Tuple[int, int]], List[List[str]]],
):
    logging.info("Writing returns dir for %s: %s", title, dirname)
    os.makedirs(dirname, exist_ok=True)
    with open(path.join(dirname, "index.html"), "w") as indexfile:
        fprint = partial(print, file=indexfile)
        fprint(RETURNS_TEMPLATE_PRE.format(style=STYLE, title=title))
        fprint("<h2>Income vs Expenses</h2>")
        plot = plot_inc_vs_expenses(dirname, income_data, expense_data)
        fprint('<img src={} style="width: 100%"/>'.format(plot))


def set_axis(ax_, date_min, date_max):
    """Setup X axis for dates."""

    years = mdates.YearLocator()
    years_fmt = mdates.DateFormatter("%Y")
    months = mdates.MonthLocator()

    ax_.xaxis.set_major_locator(years)
    ax_.xaxis.set_major_formatter(years_fmt)
    ax_.xaxis.set_minor_locator(months)

    if date_min and date_max:
        datemin = np.datetime64(date_min, "Y")
        datemax = np.datetime64(date_max, "Y") + np.timedelta64(1, "Y")
        ax_.set_xlim(datemin, datemax)

    ax_.format_xdata = mdates.DateFormatter("%Y-%m-%d")
    ax_.format_ydata = "{:,}".format
    ax_.grid(True)


def plot_inc_vs_expenses(
    dirname: str,
    income_data: Tuple[List[Tuple[int, int]], List[List[str]]],
    expense_data: Tuple[List[Tuple[int, int]], List[List[str]]],
) -> str:
    filename = "inc_exp.svg"
    filename_path = path.join(dirname, "inc_exp.svg")
    fig, ax = plt.subplots(figsize=[10, 4])
    ax.set_title("Income vs Expenses")
    all_months = expense_data[0]

    inc_vs_exp = np.zeros(len(all_months))
    for account in expense_data[1]:
        logging.info(account)
        index = 0
        for month in account[1:]:
            if month == "":
                continue
            logging.info(month)
            inc_vs_exp[index] += -float(month)
            index += 1
    for account in income_data[1]:
        logging.info(account)
        index = 0
        for month in account[1:]:
            if month == "":
                continue
            logging.info(month)
            inc_vs_exp[index] += -float(month)
            index += 1

    start = all_months[0] if all_months else None
    end = all_months[-1] if all_months else None
    date_start = datetime.date(start[0], start[1], 1) if start else None
    date_end = datetime.date(end[0], end[1], 1) if end else None
    dates_all = [datetime.date(x[0], x[1], 1) for x in all_months]
    set_axis(
        ax,
        date_start,
        date_end,
    )
    lw = 0.8
    ax.axhline(0, color="#000", linewidth=lw)
    ax.plot(dates_all, inc_vs_exp, color="#000", alpha=0.7, linewidth=lw)
    logging.info(dates_all)
    logging.info(inc_vs_exp)
    plt.savefig(filename_path)
    plt.close(fig)
    return filename


if __name__ == "__main__":
    main()

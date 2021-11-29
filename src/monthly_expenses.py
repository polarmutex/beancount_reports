"""Pivot table on monthly expenses, with custom rollups and exemptions.
from:https://github.com/beancount/beanlabs/blob/master/beanlabs/budget/monthly_expenses.py
"""
__copyright__ = "Copyright (C) 2015-2016  Martin Blais"
__license__ = "GNU GPLv2"

import collections
import datetime
import re
from typing import List, Set, Tuple

from beancount.core import account_types, convert, data, inventory

MAPS = [
    # (re.compile("Expenses:Online:Media"), "Expenses:Online:Media"),
    # (re.compile("Expenses:Online:Apps"), "Expenses:Online:Apps"),
    # (re.compile("Expenses:Online:Services"), "Expenses:Online:Services"),
    # (re.compile("Expenses:Health:Medical"), "Expenses:Health:Medical"),
    # (re.compile("Expenses:Health:Dental"), "Expenses:Health:Dental"),
    # (
    #    re.compile("Expenses:Health:PhysicalTherapy"),
    #    "Expenses:Health:PhysicalTherapy",
    # ),
    # (re.compile("Expenses:Health:Vision"), "Expenses:Health:Vision"),
    # (
    #    re.compile("Expenses:(Financial|PayPal|Ebay)" ":(Fees|Commissions)"),
    #    "Expenses:Financial:Fees",
    # ),
    # (re.compile("Expenses:Clothing"), "Expenses:Clothing"),
    # (re.compile("Expenses:Scuba"), "Expenses:Scuba"),
    # (re.compile("Expenses:Fun"), "Expenses:Fun"),
    # (re.compile("Expenses:Govt-Services"), "Expenses:Govt-Services"),
    # (re.compile("Expenses:Charity"), "Expenses:Charity"),
    # (
    #    re.compile("Expenses:Communications:Internet"),
    #    "Expenses:Communications:Internet",
    # ),
    # (
    #    re.compile("Expenses:Transportation:Public"),
    #    "Expenses:Transportation:Public",
    # ),
]


def compute_monthly_expenses(
    entries: List[data.Transaction],
    acctypes,
    price_map,
    Q,
) -> Tuple[List[Tuple[int, int]], List[List[str]]]:

    # Accumulate expenses for the period.
    balances = collections.defaultdict(
        lambda: collections.defaultdict(inventory.Inventory)
    )
    all_months: Set[Tuple[int, int]] = set()
    for entry in data.filter_txns(entries):

        month: Tuple[int, int] = (entry.date.year, entry.date.month)
        all_months.add(month)
        for posting in entry.postings:
            if (
                account_types.get_account_type(posting.account)
                != acctypes.expenses
            ):
                continue
            if posting.units.currency != "USD":
                continue
            account = posting.account
            for regexp, target_account in MAPS:
                if regexp.match(account):
                    account = target_account
                    break
            balances[account][month].add_position(posting)

    # Reduce the final balances to numbers.
    sbalances = collections.defaultdict(dict)
    for account, months in sorted(balances.items()):
        for month, balance in sorted(months.items()):
            year, mth = month
            date = datetime.date(year, mth, 1)
            balance = balance.reduce(convert.get_value, price_map, date)
            balance = balance.reduce(
                convert.convert_position, "USD", price_map, date
            )
            try:
                pos = balance.get_only_position()
            except AssertionError:
                print(balance)
                raise
            total = pos.units.number if pos and pos.units else None
            sbalances[account][month] = total

    # Pivot the table.
    header_months = sorted(all_months)
    header = ["account"] + ["{}-{:02d}".format(*m) for m in header_months]
    rows: List[List[str]] = []
    for account in sorted(sbalances.keys()):
        row = [account]
        for month in header_months:
            total = sbalances[account].get(month, None)
            row.append(str(total.quantize(Q)) if total else "")
        rows.append(row)
    return (header_months, rows)


def compute_monthly_income(
    entries: List[data.Transaction],
    acctypes,
    price_map,
    Q,
) -> Tuple[List[Tuple[int, int]], List[List[str]]]:

    # Accumulate income for the period.
    balances = collections.defaultdict(
        lambda: collections.defaultdict(inventory.Inventory)
    )
    all_months = set()
    for entry in data.filter_txns(entries):

        month = (entry.date.year, entry.date.month)
        all_months.add(month)
        for posting in entry.postings:
            if (
                account_types.get_account_type(posting.account)
                != acctypes.income
            ):
                continue
            if posting.units.currency != "USD":
                continue
            account = posting.account
            for regexp, target_account in MAPS:
                if regexp.match(account):
                    account = target_account
                    break
            balances[account][month].add_position(posting)

    # Reduce the final balances to numbers.
    sbalances = collections.defaultdict(dict)
    for account, months in sorted(balances.items()):
        for month, balance in sorted(months.items()):
            year, mth = month
            date = datetime.date(year, mth, 1)
            balance = balance.reduce(convert.get_value, price_map, date)
            balance = balance.reduce(
                convert.convert_position, "USD", price_map, date
            )
            try:
                pos = balance.get_only_position()
            except AssertionError:
                print(balance)
                raise
            total = pos.units.number if pos and pos.units else None
            sbalances[account][month] = total

    # Pivot the table.
    header_months = sorted(all_months)
    header = ["account"] + ["{}-{:02d}".format(*m) for m in header_months]
    rows: List[List[str]] = []
    for account in sorted(sbalances.keys()):
        row = [account]
        for month in header_months:
            total = sbalances[account].get(month, None)
            row.append(str(total.quantize(Q)) if total else "")
        rows.append(row)
    return (header_months, rows)

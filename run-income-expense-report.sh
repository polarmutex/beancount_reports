#!/bin/sh
python src/compute_income_vs_expenses.py -v --start-date "2021-01-01" ~/repos/personal/beancount/journal.beancount configs/income_expense_config output/

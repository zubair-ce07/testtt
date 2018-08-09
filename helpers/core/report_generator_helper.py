from helpers.core.calculator_helper import month_with_num


def readable_date(date):
    # assumed date is given in YYYY-MM-DD method
    split_date = date.split('-')
    return month_with_num(split_date[1]) + " " + split_date[2]

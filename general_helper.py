import datetime


def change_month_to_month_name(month):
    """

    :param month:
    :return:
    """
    current_date = datetime.datetime.now()
    month = current_date.replace(month=month).strftime("%b")
    return month

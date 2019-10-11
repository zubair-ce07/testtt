import datetime


class DateTimeUtil:
    @staticmethod
    def __parse(date_string, format_string):
        return datetime.datetime.strptime(date_string, format_string)

    @staticmethod
    def __format(datetime_obj, format_string):
        return datetime.datetime.strftime(datetime_obj, format_string)

    @staticmethod
    def parse_date(date_string, date_format="%Y/%m"):
        return DateTimeUtil._DateTimeUtil__parse(date_string, date_format)

    @staticmethod
    def get_year_month(date_string):
        datetime_obj = DateTimeUtil.parse_date(date_string)
        return (datetime_obj.year, datetime_obj.month)

    @staticmethod
    def month_name(date_string, date_format="%Y/%m", short_name=True):
        month_format = "%b" if short_name else "%B"
        datetime_obj = DateTimeUtil.parse_date(date_string, date_format)
        return DateTimeUtil._DateTimeUtil__format(datetime_obj, month_format)

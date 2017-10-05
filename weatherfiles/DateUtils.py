from datetime import datetime

ISO_DATE_FORMAT = "%Y-%m-%d"
OUTPUT_MONTH_DAY_FORMAT = '%B %d'
NUMBER_DAY_FORMAT = '%d'
MONTH_YEAR_FORMAT = '%B %Y'

class DateUtils:
    @staticmethod
    def get_date(date):
        datetime_object = DateUtils.parse_to_date(date)
        return datetime_object.strftime(OUTPUT_MONTH_DAY_FORMAT)

    @staticmethod
    def get_month_and_day(date):
        datetime_object = DateUtils.parse_to_date(date)
        return datetime_object.strftime(OUTPUT_MONTH_DAY_FORMAT)

    @staticmethod
    def get_day(date):
        datetime_object = DateUtils.parse_to_date(date)
        return datetime_object.strftime(NUMBER_DAY_FORMAT)

    @staticmethod
    def get_month_with_year(date):
        datetime_object = DateUtils.parse_to_date(date)
        return datetime_object.strftime(MONTH_YEAR_FORMAT)

    @staticmethod
    def parse_to_date(date):
        return datetime.strptime(date, ISO_DATE_FORMAT)
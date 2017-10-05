from datetime import datetime

ISO_DATE_FORMAT = "%Y-%m-%d"
OUTPUT_MONTH_DAY_FORMAT = '%B %d'

class DateUtils:
    @staticmethod
    def get_date(date):
        datetime_object = datetime.strptime(date, ISO_DATE_FORMAT)
        return (datetime_object.strftime(OUTPUT_MONTH_DAY_FORMAT))

    @staticmethod
    def get_month_and_day(date):
        datetime_object = datetime.strptime(date, ISO_DATE_FORMAT)
        return (datetime_object.strftime(OUTPUT_MONTH_DAY_FORMAT))

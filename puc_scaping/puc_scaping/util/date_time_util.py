""" Utility class for performing date time actions"""
import datetime
import logging


class DateTimeUtil:
    @staticmethod
    def parse_date(date_string, date_format="%m/%d/%Y"):
        """
        This function parses date string with given format
        Parameters:
            date_string (str): Date string to parsed.
            format_string (str)[optional]: Format of the given date
        Returns:
            datetime: datetime object from the given date string.
        """
        return datetime.datetime.strptime(date_string, date_format)

    def format_date(date_string,
                    date_format="%m/%d/%Y",
                    output_format="%B %d, %Y"):
        """
        This function formats date string to given format
        Parameters:
            date_string (str): Date string to formatted.
            ormat_string (str)[optional]: Format of the given date
            output_format (str)[optional]: Format of the returned date string
        Returns:
            str: formatted date in given format
        """
        datetime_obj = DateTimeUtil.parse_date(date_string, date_format)
        return datetime.datetime.strftime(datetime_obj, output_format)

    @staticmethod
    def validate_dates(from_date, to_date, date_format):
        """
        Validates and Compare if both from and to date are not in future and
        from date is not ahead of to date
        Parameters:
            from_date (str): from date string.
            to_date (str): to date string
            date_format (str): Format of the given dates
        Returns:
            bool: True if valid and False incase of invalid
        """
        if not (from_date and to_date):
            logging.error("from date or to date missing")
            return False

        today = datetime.datetime.now()

        try:
            f_date = DateTimeUtil.parse_date(from_date, date_format)
            t_date = DateTimeUtil.parse_date(to_date, date_format)
        except ValueError:
            logging.error("Invald date format: <MM/DD/YYYY>")
            return False

        if (f_date > today or t_date > today):
            logging.error("From and to date must not be in future")
            return False

        if f_date > t_date:
            logging.error("From date must be less than or equal to to date")
            return False

        return True

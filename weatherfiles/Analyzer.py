"""
This class will do all the computations and generate reports against given data
"""
import calendar
from datetime import datetime

from dateutil.parser import parse



class Analyzer:
    @staticmethod
    def parse_date(date, delimeter):
        """
        split date string according to given delimiter
        :param date: date string
        :param delimeter: separator
        :return: year, month, day
        """

        complete_date_format = '%Y{delim}%m{delim}%d'
        month_date_format = '%Y{delim}%m'

        date_format = complete_date_format if date.count(delimeter) > 1 else month_date_format
        return datetime.strptime(date, date_format.format(delim=delimeter))

    @staticmethod
    def yearly_report(years_records):
        """
        compute make report of highest temperature , lowest temperature and  most humid day of the year
        :param years_records: list of dictionaries containing records of that year
        :return: dictionary containing final report of the year or an empty dictionary if data is not found
        """

        highest_temp_record = max(
            years_records,
            key=lambda record: record['Max TemperatureC']
            if record['Max TemperatureC'] != ''
            else float('-inf')
        )
        lowest_temp_record = min(
            years_records,
            key=lambda record: record['Min TemperatureC']
            if record['Min TemperatureC'] != ''
            else float('inf')
        )
        humidity_record = max(
            years_records,
            key=lambda record: record['Max Humidity']
            if record['Max Humidity'] != ''
            else 0
        )

        results = {
            'highest': highest_temp_record,
            'lowest': lowest_temp_record,
            'humidity': humidity_record,
        }

        return results

    @staticmethod
    def monthly_report(month_records, date):
        """
        Method for generating monthly report for average highest temperature, average lowest temperature
        and average mean humidity
        :param month_records: list of dictionaries
        :param date: yyyy/mm  format date for the month or which report is required
        :return: a dictionary of report or empty dictionary if no data is found
        """
        sum_max_tempc = sum(record['Max TemperatureC'] for record in month_records if record['Max TemperatureC'] != '')
        sum_min_tempc = sum(record['Min TemperatureC'] for record in month_records if record['Min TemperatureC'] != '')
        sum_humidity = sum(record[' Mean Humidity'] for record in month_records if record[' Mean Humidity'] != '')

        total_days = calendar.monthrange(int(date.year),
                                         int(date.month),
                                         )[1]
        results = {
            'Highest Average': sum_max_tempc / total_days,
            'Lowest Average': sum_min_tempc / total_days,
            'Average Mean Humidity': sum_humidity / total_days,
        }

        return results

    @staticmethod
    def monthly_chart(month_records):
        """
        Method to generate data report of highest and lowest temperature each day for
        chart to Display for a given month
        :param month_records: list of dictionaries with records of that month
        :return: a dictionary containing values for highest and lowest temperature against each day of month
        """
        results = {}

        for record in month_records:

            day = parse(str(record['PKT'].day)).strftime('%d')
            max_tempc = int(record['Max TemperatureC'] if record['Max TemperatureC'] != '' else 0)
            min_tempc = int(record['Min TemperatureC'] if record['Min TemperatureC'] != '' else 0)

            results[day] = [max_tempc, min_tempc]

        return results

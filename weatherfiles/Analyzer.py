"""
This class will do all the computations and generate reports against given data
"""
import calendar
from datetime import datetime


class Analyzer:
    @staticmethod
    def parse_date(date, delimeter):
        """
        split date string according to given delimiter
        :param date: date string
        :param delimeter: separator
        :return: year, month, day
        """
        if date.count(delimeter) > 1:
            return datetime.strptime(date, '%Y' + delimeter + '%m' + delimeter + '%d')
        return datetime.strptime(date, '%Y' + delimeter + '%m')

    @staticmethod
    def yearly_report(data, year):
        """
        compute make report of highest temperature , lowest temperature and  most humid day of the year
        :param data: list of dictionaries
        :param year: year for which report is required
        :return: dictionary containing final report of the year or an empty dictionary if data is not found
        """

        years_records = [record for record in data if record['PKT'].year == year]

        if not years_records:
            return {}

        highest_temp_record = max(
            years_records,
            key=lambda record: record['Max TemperatureC']
            if record['Max TemperatureC'] != ''
            else -200
        )
        lowest_temp_record = min(
            years_records,
            key=lambda record: record['Min TemperatureC']
            if record['Min TemperatureC'] != ''
            else 200
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
    def monthly_report(data, date):
        """
        Method for generating monthly report for average highest temperature, average lowest temperature
        and average mean humidity
        :param data: dictionary containing the required data to process on with keys features , values
        :param date: yyyy/mm  format date for the month or which report is required
        :return: a dictionary of report or empty dictionary if no data is found
        """
        date = Analyzer.parse_date(date, '/')

        month_records = [
            record
            for record in data
            if record['PKT'].year == date.year and record['PKT'].month == date.month
        ]

        if not month_records:
            return {}

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
    def monthly_chart(data, date):
        """
        Method to generate data report of highest and lowest temperature each day for
        chart to Display for a given month
        :param data: dictionary containing the required data to process on with keys features , values
        :param date:  yyyy/mm  format date for the month or which report is required
        :return: a dictionary containing values for highest and lowest temperature against each day of month
        """
        results = {}

        date = Analyzer.parse_date(date, '/')

        month_records = [
            record
            for record in data
            if record['PKT'].year == date.year and record['PKT'].month == date.month
        ]

        for record in month_records:
            day = str(record['PKT'].day)
            if len(day) < 2:
                day = '0' + day

            max_tempc = int(record['Max TemperatureC'] if record['Max TemperatureC'] != '' else 0)
            min_tempc = int(record['Min TemperatureC'] if record['Min TemperatureC'] != '' else 0)

            results[day] = [max_tempc, min_tempc]

        return results

"""
This class will do all the computations and generate reports against given data
"""
import calendar


class Analyzer:
    @staticmethod
    def parse_date(date, delimeter):
        """
        split date string according to given delimiter
        :param date: date string
        :param delimeter: separator
        :return: year, month, day
        """
        return date.split(delimeter)

    @staticmethod
    def yearly_report(data, year):
        """
        compute make report of highest temperature , lowest temperature and  most humid day of the year
        :param data: list of dictionaries
        :param year: year for which report is required
        :return: dictionary containing final report of the year or an empty dictionary if data is not found
        """
        highest_temp = humidity = 0

        # 200 because never in history of mankind temperature went this high
        lowest_temp = 200

        year_exist = False

        for record in data:
            date_in_record = record['PKT']
            if year in date_in_record:
                year_exist = True
                if record['Max TemperatureC'] != '' and record['Max TemperatureC'] > highest_temp:
                    highest_temp = record['Max TemperatureC']
                    date_highest = date_in_record

                if record['Min TemperatureC'] != '' and record['Min TemperatureC'] < lowest_temp:
                    lowest_temp = record['Min TemperatureC']
                    date_lowest = date_in_record

                if record['Max Humidity'] != '' and record['Max Humidity'] > humidity:
                    humidity = record['Max Humidity']
                    date_humidity = date_in_record

        if not year_exist:
            return {}

        results = {
            'highest tempc': highest_temp,
            'date highest tempc': date_highest,
            'lowest tempc': lowest_temp,
            'date lowest tempc': date_lowest,
            'humidity': humidity,
            'date humidity': date_humidity,
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
        year, month = Analyzer.parse_date(date, '/')

        highest_sum = lowest_sum = humidity_sum = 0

        month_exists = False

        for record in data:
            record_year, record_month, record_day = record['PKT'].split('-')
            if year in record_year and month == record_month:
                month_exists = True
                if record[' Mean Humidity'] != '':
                    humidity_sum += record[' Mean Humidity']
                if record['Max TemperatureC'] != '':
                    highest_sum += record['Max TemperatureC']
                if record['Min TemperatureC'] != '':
                    lowest_sum += record['Min TemperatureC']

        if not month_exists:
            return {}

        total_days = calendar.monthrange(int(year),
                                         int(month),
                                         )[1]
        results = {
            'Highest Average': highest_sum / total_days,
            'Lowest Average': lowest_sum / total_days,
            'Average Mean Humidity': humidity_sum / total_days,
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

        year, month = Analyzer.parse_date(date, '/')

        for record in data:
            record_year, record_month, record_day = record['PKT'].split('-')

            if year in record_year and month == record_month:
                day = record_day
                if len(day) < 2:
                    day = '0' + day

                max_tempc = record['Max TemperatureC'] if record['Max TemperatureC'] != '' else 0
                min_tempc = record['Min TemperatureC'] if record['Min TemperatureC'] != '' else 0

                results[day] = [max_tempc, min_tempc]

        return results

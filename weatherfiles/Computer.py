""" class for computation """

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
        :param data: dictionary containing features and their values
        :param year: year for which report is required
        :return: dictionary containing final report of the year or an empty dictionary if data is not found
        """
        highest = humidity = 0

        # 200 because never in history of mankind temperature went this high
        lowest = 200

        index_of_maxtemp = data['features'].index('Max TemperatureC')
        index_of_mintemp = data['features'].index('Min TemperatureC')
        index_of_humidity = data['features'].index('Max Humidity')

        year_exist = False

        for record in data['values']:
            date_in_record = record[0]
            if year in date_in_record:
                year_exist = True
                if record[index_of_maxtemp] != '' and record[index_of_maxtemp] > highest:
                    highest = record[index_of_maxtemp]
                    date_highest = date_in_record

                if record[index_of_mintemp] != '' and record[index_of_mintemp] < lowest:
                    lowest = record[index_of_mintemp]
                    date_lowest = date_in_record

                if record[index_of_humidity] != '' and record[index_of_humidity] > humidity:
                    humidity = record[index_of_humidity]
                    date_humidity = date_in_record

        if not year_exist:
            return {}

        year, month, day_high = Analyzer.parse_date(date_highest, '-')
        month_high = calendar.month_name[int(month)]

        year, month, day_low = Analyzer.parse_date(date_lowest, '-')
        month_low = calendar.month_name[int(month)]

        year, month, day_humid = Analyzer.parse_date(date_humidity, '-')
        month_humid = calendar.month_name[int(month)]

        results = {
            'Highest': "{}C on {} {}".format(highest, month_high, day_high),
            'Lowest': "{}C on {} {}".format(lowest, month_low, day_low),
            'Humidity': "{}% on {} {}".format(humidity, month_humid, day_humid),
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

        highest = lowest = humidity = 0

        index_of_maxtemp = data['features'].index('Max TemperatureC')
        index_of_mintemp = data['features'].index('Min TemperatureC')
        index_of_humidity = data['features'].index(' Mean Humidity')

        month_exists = False

        for record in data['values']:
            record_year, record_month, record_day = record[0].split('-')
            if year in record_year and month == record_month:
                month_exists = True
                if record[index_of_humidity] != '':
                    humidity += record[index_of_humidity]
                if record[index_of_maxtemp] != '':
                    highest += record[index_of_maxtemp]
                if record[index_of_mintemp] != '':
                    lowest += record[index_of_mintemp]

        if not month_exists:
            return {}

        total_days = calendar.monthrange(int(year),
                                         int(month),
                                         )[1]
        results = {
            'Highest Average': str(highest / total_days) + "C",
            'Lowest Average': str(lowest / total_days) + 'C',
            'Average Mean Humidity': str(humidity / total_days) + '%',
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

        index_of_maxtemp = data['features'].index('Max TemperatureC')
        index_of_mintemp = data['features'].index('Min TemperatureC')

        year, month = Analyzer.parse_date(date, '/')

        for record in data['values']:
            record_year, record_month, record_day = record[0].split('-')

            if year in record_year and month == record_month:
                day = record_day
                if len(day) < 2:
                    day = '0' + day

                results[day] = []

                max_tempc = record[index_of_maxtemp]
                min_tempc = record[index_of_mintemp]

                if max_tempc != '':
                    temp = '+' * max_tempc
                    temp = '{} {}C'.format(temp, max_tempc)
                    results[day].append(temp)

                if min_tempc != '':
                    temp = '+' * min_tempc
                    temp = '{} {}C'.format(temp, min_tempc)
                    results[day].append(temp)

        return results

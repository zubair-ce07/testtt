""" class for computation """

import calendar


class Analyzer:
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

        for record in data['values']:
            if year in record[0]:
                if record[index_of_maxtemp] != '' and record[index_of_maxtemp] > highest:
                    highest = record[index_of_maxtemp]
                    date_highest = record[0]

                if record[index_of_mintemp] != '' and record[index_of_mintemp] < lowest:
                    lowest = record[index_of_mintemp]
                    date_lowest = record[0]

                if record[index_of_humidity] != '' and record[index_of_humidity] > humidity:
                    humidity = record[index_of_humidity]
                    date_humidity = record[0]
        try:

            year, month, day = date_highest.split('-')
            month_high = calendar.month_name[int(month)]
            day_high = day

            year, month, day = date_lowest.split('-')
            month_low = calendar.month_name[int(month)]
            day_low = day

            year, month, day = date_humidity.split('-')
            month_humid = calendar.month_name[int(month)]
            day_humid = day

            results = {
                'Highest': "{}C on {} {}".format(highest, month_high, day_high),
                'Lowest': "{}C on {} {}".format(lowest, month_low, day_low),
                'Humidity': "{}% on {} {}".format(humidity, month_humid, day_humid),
            }

            return results
        except UnboundLocalError:
            return {}

    @staticmethod
    def monthly_report(data, date):
        """
        Method for generating monthly report for average highest temperature, average lowest temperature
        and average mean humidity
        :param data: dictionary containing the required data to process on with keys features , values
        :param date: yyyy/mm  format date for the month or which report is required
        :return: a dictionary of report or empty dictionary if no data is found
        """
        year = date.split('/')[0]
        month = date.split('/')[1]

        highest = lowest = humidity = 0

        index_of_maxtemp = data['features'].index('Max TemperatureC')
        index_of_mintemp = data['features'].index('Min TemperatureC')
        index_of_humidity = data['features'].index(' Mean Humidity')

        for record in data['values']:
            if year in record[0] and month == record[0].split('-')[1]:
                if record[index_of_humidity] != '':
                    humidity += record[index_of_humidity]
                if record[index_of_maxtemp] != '':
                    highest += record[index_of_maxtemp]
                if record[index_of_mintemp] != '':
                    lowest += record[index_of_mintemp]

        try:
            total_days = calendar.monthrange(int(year),
                                            int(month),
                                            )[1]
            results = {
                'Highest Average': str(highest / total_days) + "C",
                'Lowest Average': str(lowest / total_days) + 'C',
                'Average Mean Humidity': str(humidity / total_days) + '%',
            }

            return results

        except UnboundLocalError:
            return {}

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

        year = date.split('/')[0]
        month = date.split('/')[1]

        for record in data['values']:
            if year in record[0] and month == record[0].split('-')[1]:
                key = record[0].split('-')[2]
                if len(key) < 2:
                    key = '0' + key

                results[key] = []

                if record[index_of_maxtemp] != '':
                    temp = ''
                    for i in range(record[index_of_maxtemp]):
                        temp += '+'

                    temp += ' ' + str(record[index_of_maxtemp]) + 'C'
                    results[key].append(temp)

                if record[index_of_mintemp] != '':
                    temp = ''
                    for i in range(record[index_of_mintemp]):
                        temp += '+'

                    temp += ' ' + str(record[index_of_mintemp]) + 'C'
                    results[key].append(temp)

        return results

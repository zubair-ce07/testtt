""" class for computation """

import calendar


class Computer:

    @staticmethod
    def compute_e(data, year):
        highest = humidity = 0

        # 200 because never in history of mankind temperature went this high
        lowest = 200

        index_of_maxtemp = data['Features'].index('Max TemperatureC')
        index_of_mintemp = data['Features'].index('Min TemperatureC')
        index_of_humidity = data['Features'].index('Max Humidity')

        for day in data['values']:
            if year in day[0]:
                if day[index_of_maxtemp] != '' and day[index_of_maxtemp] > highest:
                    highest = day[index_of_maxtemp]
                    datehighest = day[0]

                if day[index_of_mintemp] != '' and day[index_of_mintemp] < lowest:
                    lowest = day[index_of_mintemp]
                    datelowest = day[0]

                if day[index_of_humidity] != '' and day[index_of_humidity] > humidity:
                    humidity = day[index_of_humidity]
                    datehumidity = day[0]
        try:

            dates = datehighest.split('-') + datelowest.split('-') + datehumidity.split('-')
            dayhigh = dates[2]
            monthhigh = calendar.month_name[int(dates[1])]

            daylow = dates[5]
            monthlow = calendar.month_name[int(dates[4])]

            dayhumid = dates[8]
            monthhumid = calendar.month_name[int(dates[7])]

            results = {
                'Highest': "{}C on {} {}".format(highest, monthhigh, dayhigh),
                'Lowest': "{}C on {} {}".format(lowest, monthlow, daylow),
                'Humidity': "{}% on {} {}".format(humidity, monthhumid, dayhumid),
            }

            return results
        except UnboundLocalError:
            return {}

    @staticmethod
    def compute_a(data, date):
        year = date.split('/')[0]
        month = date.split('/')[1]

        highest = lowest = humidity = 0

        index_of_maxtemp = data['Features'].index('Max TemperatureC')
        index_of_mintemp = data['Features'].index('Min TemperatureC')
        index_of_humidity = data['Features'].index(' Mean Humidity')

        for day in data['values']:
            if year in day[0] and month == day[0].split('-')[1]:
                if day[index_of_humidity] != '':
                    humidity += day[index_of_humidity]
                if day[index_of_maxtemp] != '':
                    highest += day[index_of_maxtemp]
                if day[index_of_mintemp] != '':
                    lowest += day[index_of_mintemp]

        try:
            totaldays = calendar.monthrange(int(year),
                                            int(month),
                                            )[1]
            results = {
                'Highest Average': str(highest / totaldays) + "C",
                'Lowest Average': str(lowest / totaldays) + 'C',
                'Average Mean Humidity': str(humidity / totaldays) + '%',
            }

            return results

        except UnboundLocalError:
            return {}

    @staticmethod
    def compute_c(data, date):
        results = {}

        index_of_maxtemp = data['Features'].index('Max TemperatureC')
        index_of_mintemp = data['Features'].index('Min TemperatureC')

        year = date.split('/')[0]
        month = date.split('/')[1]

        for day in data['values']:
            if year in day[0] and month == day[0].split('-')[1]:
                key=day[0].split('-')[2]
                if len(key)<2:
                    key='0'+key

                results[key] = []

                if day[index_of_maxtemp] != '':
                    temp = ''
                    for i in range(day[index_of_maxtemp]):
                        temp += '+'

                    temp += ' ' + str(day[index_of_maxtemp]) + 'C'
                    results[key].append(temp)
                # else:
                #     results[key].append('No data!')

                if day[index_of_mintemp] != '':
                    temp = ''
                    for i in range(day[index_of_mintemp]):
                        temp += '+'

                    temp += ' ' + str(day[index_of_mintemp]) + 'C'
                    results[key].append(temp)
                # else:
                #     results[key].append('No data!')

        return results

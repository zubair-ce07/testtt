"""
WeatherReadingsCalculator takes data from WeatherFilesParser and then processes it
"""

from weather_data import WeatherData


class WeatherReadingsCalculator:
    """
    Get populated Data from WeatherData then
    performs calculations according to entered command
    calculated_weather_results are stored in following structure
    {
        'type': '-e',
        'data': [
                {'date': '', 'value': '', 'text': '', 'ending': ''},
        ]
     }
    """

    calculated_weather_results = []

    def __init__(self, command):
        """
        :param command:
        copy data from WeatherData to self.weather_data for processing and perform calculations
        """
        self.weather_data = WeatherData.yearly
        self.calculate(command)

    def save_results(self, data_storage_type, calculated_result):
        """
        appends each data results to calculated_weather_results
        :param data_storage_type: can be -e, -a, -c, -d
        :param calculated_result: data according to above type
        :return:
        """
        self.calculated_weather_results.append({'type': data_storage_type,
                                                'data': calculated_result})

    @staticmethod
    def month_with_num(num):
        """
        take num and returns corresponding month
        e.g. month_with_num(2) will return 'Feb'
        :param num:
        :return:
        """
        month_dict = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun',
                      '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
        return month_dict.get(num, '')

    @staticmethod
    def calculate_average(list_of_numbers):
        """
        takes list of numbers, perform sum operation on it
        then divide by number of entries in list_of_numbers
        before returning round the result up to two decimal places
        :rtype: float
        :param list_of_numbers:
        :return:
        """
        return round(sum(list_of_numbers) / float(len(list_of_numbers)), 2)

    @staticmethod
    def get_keys_from_list(key_to_return, list_of_dictionaries):
        """
        getting a specific keys from a list of dicts
        :param key_to_return:
        :param list_of_dictionaries:
        :return list:
        """
        return [int(d[key_to_return]) for d in list_of_dictionaries if key_to_return in d]

    def calculate(self, command):
        """
        command is array of args given at terminal e.g. ['-e', '2015', '-a', '2013/6']
        :param command:
        command -c print 2 lines of + in different colors
        command -d print 1 + line of + in mixed colors
        command -a for specific month show highest avg, lowest avg and avg mean humidity
        command -e show yearly MIN/MAX temperatures & Max humidity
        input format "-e 2013"
        input format "-a 2013/6"  "-c 2013/6"  "-d 2013/6"
        :return:
        """
        print()
        try:
            for entry in command:

                if "-e" in entry:
                    self.calculate_highlow_temperature_humidity(entry, command)

                elif "-a" in entry or "-c" in entry or "-d" in entry:

                    index = command.index(entry)
                    arg = command[index + 1]
                    # for given year of month 2012/6
                    year, month = arg.split('/')[0], self.month_with_num(arg.split('/')[1])
                    if month is None:
                        raise ValueError()

                    if "-a" in entry:
                        self.calculate_average_temperature_humidity(month, year, entry)

                    elif "-c" in entry or "-d" in entry:

                        index = command.index(entry)
                        arg = command[index + 1]
                        # for given year of month 2012/6
                        year, month = arg.split('/')[0], self.month_with_num(arg.split('/')[1])
                        if month is None:
                            raise ValueError()

                        calculated_data = [
                            {'text': f"{year} {month}", 'value': self.weather_data[year][month]}]
                        self.save_results(entry, calculated_data)
        except ValueError as value_error:
            print(f"got value error! {value_error}")
            return
        except IndexError as index_error:
            print(f"got index error! {index_error}")
            return
        except KeyError as key_error:
            print(f"got key error! {key_error}")
            print(f"for years try {WeatherData.years_added_so_far}")
            return

    def calculate_highlow_temperature_humidity(self, entry, command):
        """
        command -e show yearly MIN/MAX temperatures & Max humidity
        input format "-e 2013"
        :param entry:
        :param command:
        :return:
        """
        index = command.index(entry)
        arg = command[index + 1]  # getting entered year
        max_temp_list = []

        # appending entries of all months of year in one list
        year_months = set()
        for key, value in self.weather_data[arg].items():
            max_temp_list = max_temp_list + value
            year_months.add(key)

        calculated_data = []
        sorted_arr = sorted(max_temp_list, key=lambda k: k['max_temperature_c'])
        date = sorted_arr.pop()['pkt']
        value = str(sorted_arr.pop()['max_temperature_c'])
        text = 'Highest: '
        ending = ''
        calculated_data.append(WeatherReadingsCalculator.calculated_dict(text, value, date, ending))

        sorted_arr = sorted(max_temp_list, key=lambda k: k['min_temperature_c'])
        date = sorted_arr.pop()['pkt']
        value = str(sorted_arr.pop()['min_temperature_c'])
        text = 'Lowest: '
        ending = ''
        calculated_data.append(WeatherReadingsCalculator.calculated_dict(text, value, date, ending))

        sorted_arr = sorted(max_temp_list, key=lambda k: k['max_humidity'])
        date = sorted_arr.pop()['pkt']
        value = str(sorted_arr.pop()['max_humidity'])
        text = 'Humidity: '
        ending = '%'
        calculated_data.append(WeatherReadingsCalculator.calculated_dict(text, value, date, ending))

        # saving calculated results
        self.save_results(entry, calculated_data)

    def calculate_average_temperature_humidity(self, month, year, entry):
        """
        command -a for specific month show highest avg, lowest avg and avg mean humidity
        :param month:
        :param year:
        :param entry:
        :return:
        """
        avg_high_temp = self.calculate_average(
            self.get_keys_from_list('max_temperature_c',
                                    self.weather_data[year][month]))
        avg_low_temp = self.calculate_average(
            self.get_keys_from_list('min_temperature_c',
                                    self.weather_data[year][month]))
        avg_humid_temp = self.calculate_average(
            self.get_keys_from_list('mean_humidity',
                                    self.weather_data[year][month]))

        calculated_data = [
            WeatherReadingsCalculator.calculated_dict('Highest Average', str(avg_high_temp)),
            WeatherReadingsCalculator.calculated_dict('Lowest Average', str(avg_low_temp)),
            WeatherReadingsCalculator.calculated_dict('Average Mean Humidity', str(avg_humid_temp),
                                                      '', '%')]

        # saving calculated results
        self.save_results(entry, calculated_data)

    @staticmethod
    def calculated_dict(text, value, date='', ending=''):
        """
        returns dictionary of calculated results as
        {text: text, value: value, date: date, ending: ending}
        :param text:
        :param value:
        :param date:
        :param ending:
        :return:
        """
        return {'text': text, 'value': value, 'date': date, 'ending': ending}

from operator import itemgetter

from weather_data import WeatherData


class WeatherReadingsCalculator:
    """
    Get populated Data from WeatherData then
    performs calculations according to entered command
    """

    calculated_weather_results = []

    def __init__(self, command):
        """
        :param command:
        copy data from WeatherData to self.weather_data for processing and perform calculations
        """
        self.weather_data = WeatherData.weather_yearly_data
        self.calculate(command)

    @staticmethod
    def save_results(data_storage_type, calculated_result):
        """
        appends each data results to calculated_weather_results
        :param data_storage_type: can be -e, -a, -c, -d
        :param calculated_result: data according to above type
        :return:
        """
        WeatherReadingsCalculator.calculated_weather_results.append({'type': data_storage_type,
                                                                     'data': calculated_result})

    @staticmethod
    def month_with_num(num):
        """
        take num and returns corresponding month
        e.g. month_with_num(2) will return 'Feb'
        :param num:
        :return:
        """
        num = int(num)
        month = None
        if num == 1:
            month = 'Jan'
        elif num == 2:
            month = 'Feb'
        elif num == 3:
            month = 'Mar'
        elif num == 4:
            month = 'Apr'
        elif num == 5:
            month = 'May'
        elif num == 6:
            month = 'Jun'
        elif num == 7:
            month = 'Jul'
        elif num == 8:
            month = 'Aug'
        elif num == 9:
            month = 'Sep'
        elif num == 10:
            month = 'Oct'
        elif num == 11:
            month = 'Nov'
        elif num == 12:
            month = 'Dec'
        return month

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

                if entry == "-e":

                    index = command.index(entry)
                    arg = command[index + 1]  # getting entered year
                    max_temp_list = []

                    # appending entries of all months of year in one list
                    for key, value in self.weather_data[arg].items():
                        max_temp_list = max_temp_list + value
                    calculated_data = []
                    sorted_arr = sorted(max_temp_list, key=itemgetter('max_temperature_c'))
                    calculated_data.append({'date': sorted_arr.pop()['pkt'],
                                 'value': str(sorted_arr.pop()['max_temperature_c']),
                                 'text': 'Highest:', 'ending': ''})

                    sorted_arr = sorted(max_temp_list, key=itemgetter('min_temperature_c'))
                    calculated_data.append({'date': sorted_arr.pop()['pkt'],
                                 'value': str(sorted_arr.pop()['min_temperature_c']),
                                 'text': 'Lowest:', 'ending': ''})
                    sorted_arr = sorted(max_temp_list, key=itemgetter('max_humidity'))
                    calculated_data.append({'date': sorted_arr.pop()['pkt'],
                                 'value': str(sorted_arr.pop()['max_humidity']),
                                 'text': 'Humidity:', 'ending': '%'})

                    # saving calculated results
                    WeatherReadingsCalculator.save_results(entry, calculated_data)

                elif entry == "-a" or entry == "-c" or entry == "-d":

                    index = command.index(entry)
                    arg = command[index + 1]
                    # for given year of month 2012/6
                    year, month = arg.split('/')[0], self.month_with_num(arg.split('/')[1])
                    if month is None:
                        raise ValueError()

                    if entry == "-a":

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
                            {'text': 'Highest Average', 'value': str(avg_high_temp), 'ending': ''},
                            {'text': 'Lowest Average', 'value': str(avg_low_temp), 'ending': ''},
                            {'text': 'Average Mean Humidity', 'value': str(avg_humid_temp),
                             'ending': '%'}]

                        # saving calculated results
                        WeatherReadingsCalculator.save_results(entry, calculated_data)

                    elif entry == "-c" or entry == "-d":

                        index = command.index(entry)
                        arg = command[index + 1]
                        # for given year of month 2012/6
                        year, month = arg.split('/')[0], self.month_with_num(arg.split('/')[1])
                        if month is None:
                            raise ValueError()

                        calculated_data = [
                            {'text': f"{year} {month}", 'value': self.weather_data[year][month]}]
                        WeatherReadingsCalculator.save_results(entry, calculated_data)
        except ValueError as ve:
            print(f"got value error! {ve}")
            return
        except IndexError as ie:
            print(f"got index error! {ie}")
            return
        except KeyError as ke:
            print(f"got key error! {ke}")
            print(f"for years try {WeatherData.years_added_so_far}")
            return

class ReportPrinter:
    @staticmethod
    def averages(max_avg, least_avg, max_humidity):
        """ Prints the mean min/max temperatures and humidity """
        print('-' * 60)
        print("Highest Average Temperature:", max_avg.max_avg_temp, "C")
        print("Lowest Average Temperature:", least_avg.min_avg_temp, "C")
        print("Highest Average Humidity:", max_humidity.max_avg_humidty, "%")
        print('-' * 60)
        print('')

    @staticmethod
    def extrema(max_temp, min_temp, max_humidity, min_humidity):
        """For a given list of weather data, displays the highest temperature
        and day, lowest temperature and day, most humid day and humidity."""
        print('-'*60)
        print('Highest Temperature: ', max_temp.max_temp,
              'C on ' + max_temp.date.replace('-', '/'))
        print('Lowest Temperature: ', min_temp.min_temp,
              'C on ' + min_temp.date.replace('-', '/'))
        print('Most Humid: ', max_humidity.max_humidity,
              '% on ' + max_humidity.date.replace('-', '/'))
        print('Least Humid: ', min_humidity.min_humidity,
              '% on ' + min_humidity.date.replace('-', '/'))
        print('-' * 60)
        print('')


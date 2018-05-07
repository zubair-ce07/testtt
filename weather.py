import os.path
from weatherReport import *

class Weather:
    """ Variables to be used for yearly and monthly analysis of different
    waether parameters
    """
    def __init__(self):

        self.yearly_highest_temperature = -100
        self.yearly_lowest_temperature = 100
        self.yearly_highest_humidity = -100
        self.yearly_hightest_temperature_date = ''
        self.yearly_lowest_temperature_date = ''
        self.yearly_highest_humidity_date = ''
        self.monthly_highest_average = 0
        self.monthly_lowest_average = 0
        self.monthly_average_mean_humidity = 0

    def readDataForMonth(self, filepath):                                                     #reads data from file against particular month
        print('in read data of parent')
        total_days_count = 0
        self.month_file = filepath

        with open(self.month_file) as weather_details:

            for line in range (1):
                next(weather_details)
            for line in weather_details:
                weather_parameters = line.split(',')

                for weather_parameters_index,weather_parameter in enumerate (weather_parameters):
                    if weather_parameters[weather_parameters_index] == '':
                        weather_parameters[weather_parameters_index] = '0'

                self.monthly_highest_average += int(weather_parameters[1])
                self.monthly_lowest_average += int(weather_parameters[3])
                self.monthly_average_mean_humidity += int(weather_parameters[8])
                total_days_count += 1


            self.monthly_highest_average = int(self.monthly_highest_average / total_days_count)
            self.monthly_lowest_average = int(self.monthly_lowest_average / total_days_count)
            self.monthly_average_mean_humidity = int(self.monthly_average_mean_humidity / total_days_count)

        weather_details.close()

    def readFilesForParticularYear (self,filenames):
        self.years_filenames = filenames                                         #reads all monthly files for particular year
        for month_wise_files_counter in self.years_filenames:
            if os.path.exists(month_wise_files_counter):
                with open(month_wise_files_counter) as weather_details:
                    for line in range (1):
                        next(weather_details)
                    for line in weather_details:
                        weather_parameters = line.split(',')

                        if weather_parameters[1] is not '':
                            if int(weather_parameters[1]) > self.yearly_highest_temperature:
                                self.yearly_highest_temperature = int(weather_parameters[1])
                                self.yearly_hightest_temperature_date = weather_parameters[0]

                        if weather_parameters[3] is not '':
                            if int(weather_parameters[3]) < self.yearly_lowest_temperature:
                                self.yearly_lowest_temperature = int(weather_parameters[3])
                                self.yearly_lowest_temperature_date = weather_parameters[0]

                        if weather_parameters[7] is not '':
                            if int(weather_parameters[7]) > self.yearly_highest_humidity:
                                self.yearly_highest_humidity = int(weather_parameters[7])
                                self.yearly_highest_humidity_date = weather_parameters[0]

                weather_details.close();

    def getMonthlyWeatherDetails (self):
        monthly_weather_report = {"monthly_highest_average" : self.monthly_highest_average,
                                  "monthly_lowest_average" : self.monthly_lowest_average,
                                  "monthly_average_mean_humidity" : self.monthly_average_mean_humidity }
        return monthly_weather_report

    def getYearlyWeatherDetails (self):
        yearly_weather_details = {"highest_annual_temperature": self.yearly_highest_temperature,
                                  "highest_annual_temperature_date": self.yearly_hightest_temperature_date,
                                  "lowest_annual_temperature": self.yearly_lowest_temperature,
                                  "lowest_annual_temperature_date": self.yearly_lowest_temperature_date,
                                  "highest_annual_humidity": self.yearly_highest_humidity,
                                  "highest_annual_humidity_date": self.yearly_highest_humidity_date,}
        return yearly_weather_details

class YearlyWeather(Weather):
    """ Serves the functionality for Yearly Analysis of Weather
    """
    def __init__(self,filenames):
        Weather.__init__(self)
        self.filenames = filenames
        self.readFilesForParticularYear (self.filenames)

    def verifyYearlyData (self):                                                    #verifies file existence per year record
        file_found = False
        for file_count in self.filenames:
            if os.path.exists(file_count):
                return True

        return False

    def getYearlyValuesForTemperature (self):                                       #prints yearly record of temperature
        return self.getYearlyWeatherDetails()


class MonthlyWeather(Weather):
    """ Serves the functionality for Monthly Analysis of Weather i.e.
    reading files, finding min, max, humidity and making graphs
    """
    def __init__(self,filepath):
        Weather.__init__(self)
        self.filepath = filepath
        return self.readDataForMonth(self.filepath)

    def verifyDataForMonth(self):                                                   #verifies file existence for particular month
        file_found = False

        if os.path.exists(self.filepath):
            file_found = True

        return file_found

    def getDataForMonth (self):
        return self.getMonthlyWeatherDetails();

    def readMaxAndMinTemperaturePerDay(self):                                       #finds max and min temperature for month
        with open(self.filepath) as weather_details:
            for line in range (1):
                next(weather_details)
            for line in weather_details:
                weather_parameters = line.split(',')

                for weather_parameters_index,weather_parameter in enumerate (weather_parameters):
                    if weather_parameters[weather_parameters_index] == '':
                        weather_parameters[weather_parameters_index] = '0'

                date = weather_parameters[0].split('-')
                weather_graph = WeatherReport(int(weather_parameters[1]),int(weather_parameters[3]))
                print('\033[91m'+date[2],end='')
                weather_graph.printGraphForMaxTemperature(date[2])
                print ('\033[91m'+weather_parameters[1])
                print('\033[94m'+date[2],end='')
                weather_graph.printGraphForMinTemperature(date[2])
                print ('\033[94m'+weather_parameters[3])

        weather_details.close()

    def readDataForDailyGraph(self):                                                #reads file data for daily record graph
        with open(self.filepath) as weather_details:
            for line in range (1):
                next(weather_details)
            for line in weather_details:
                weather_parameters = line.split(',')

                for weather_parameters_index,weather_parameter in enumerate (weather_parameters):
                    if weather_parameters[weather_parameters_index] == '':
                        weather_parameters[weather_parameters_index] = '0'

                date = weather_parameters[0].split('-')

                weather_graph = WeatherReport(int(weather_parameters[1]),int(weather_parameters[3]))
                weather_graph.printMinMaxTemperatureGraphForDay(date[2])

        weather_details.close()

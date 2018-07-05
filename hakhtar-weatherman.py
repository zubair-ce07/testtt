import sys


class Argument:

    def __init__(self, action=None, year_month=None):
        self.action = action
        self.year_month = year_month


class DayForecast:

    def __init__(self, date=None, max_temp=None, mean_temp=None, min_temp=None, max_dew_point=None,
                 mean_dew_point=None, min_dew_point=None, max_humidity=None, mean_humidity=None, min_humidity=None,
                 max_sea_pressure=None, mean_sea_pressure=None, min_sea_pressure=None, max_visibility=None,
                 mean_visibility=None, min_visibility=None, max_wind_speed=None, mean_wind_speed=None,
                 max_gust_speed=None, precipitation=None, cloud_cover=None, events=None, wind_air_degrees=None):
        self.date = date
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp
        self.max_dew_point = max_dew_point
        self.mean_dew_point = mean_dew_point
        self.min_dew_point = min_dew_point
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.max_sea_pressure = max_sea_pressure
        self.mean_sea_pressure = mean_sea_pressure
        self.min_sea_pressure = min_sea_pressure
        self.max_visibility = max_visibility
        self.mean_visibility = mean_visibility
        self.min_visibility = min_visibility
        self.max_wind_speed = max_wind_speed
        self.mean_wind_speed = mean_wind_speed
        self.max_gust_speed = max_gust_speed
        self.precipitation = precipitation
        self.cloud_cover = cloud_cover
        self.events = events
        self.wind_air_degrees = wind_air_degrees


argument_list = []
readings_list = []
files_directory = sys.argv[1] + '/'  # Files Directory
temp_list = sys.argv[2:]  # List of all the arguments

month_tuple = ('Jan', 'Feb', 'Mar', 'Apr',
               'May', 'Jun', 'Jul', 'Aug',
               'Sep', 'Oct', 'Nov', 'Dec')

# Constants
WEATHER_CITY = "Murree_weather"
TOTAL_REPORTS = int(len(temp_list) / 2)
REPORT_PARAMS = 2
YEAR_LENGTH = len(month_tuple)


def get_argument_list():
    index = 0
    for i in range(0, TOTAL_REPORTS):
        argument_list.append(Argument(temp_list[i + index], temp_list[i + index + 1]))
        index += 1


def generate_reports(file_dir):
    for i in range(0, TOTAL_REPORTS):
        parse_files(argument_list[i], file_dir)


def parse_files(arg_list, directory):
    if arg_list.action == '-e':
        for i in range(0, YEAR_LENGTH):
            file_name = WEATHER_CITY + "_" + arg_list.year_month + "_" + month_tuple[i] + ".txt"
            file_location = directory + file_name

            try:
                weather_file = open(file_location, "r")
                temp_readings = [line.split(",") for line in weather_file]

                for j in range(1, len(temp_readings)):
                    # Try to
                    readings_list.append(DayForecast(temp_readings[j][0], temp_readings[j][1],
                                                     temp_readings[j][2], temp_readings[j][3],
                                                     temp_readings[j][4], temp_readings[j][5],
                                                     temp_readings[j][6], temp_readings[j][7],
                                                     temp_readings[j][8], temp_readings[j][9],
                                                     temp_readings[j][10], temp_readings[j][11],
                                                     temp_readings[j][12], temp_readings[j][13],
                                                     temp_readings[j][14], temp_readings[j][15],
                                                     temp_readings[j][16], temp_readings[j][17],
                                                     temp_readings[j][18], temp_readings[j][19],
                                                     temp_readings[j][20], temp_readings[j][21],
                                                     temp_readings[j][22]))

            except:
                print("", end="")

        calculate_results(readings_list)


def calculate_results(yearly_readings):
    max_temp_readings = find_max(yearly_readings)  # Max Temperature
    min_temp_readings = find_lowest(yearly_readings)  # Min Temperature
    max_humidity_readings = find_max_humidity(readings_list)  # Max Humidity

    max_temp_month = yearly_readings[max_temp_readings[1]].date
    min_temp_month = yearly_readings[min_temp_readings[1]].date
    max_humidity_month = yearly_readings[max_humidity_readings[1]].date

    max_temp_month_index = int(max_temp_month.split("-")[1]) - 1
    max_temp_day = int(max_temp_month.split("-")[2])

    min_temp_month_index = int(min_temp_month.split("-")[1]) - 1
    min_temp_day = int(min_temp_month.split("-")[2])

    max_humidity_month_index = int(max_humidity_month.split("-")[1]) - 1
    max_humidity_day = int(max_humidity_month.split("-")[2])

    print("Highest: %dC on %s %d" %
          (max_temp_readings[0],
           month_tuple[max_temp_month_index],
           max_temp_day))

    print("Lowest: %dC on %s %d" %
          (min_temp_readings[0],
           month_tuple[min_temp_month_index],
           min_temp_day))

    print("Humidity: %d%% on %s %d" %
          (max_humidity_readings[0],
           month_tuple[max_humidity_month_index],
           max_humidity_day))


def find_max(read_list):
    max = int(read_list[0].max_temp)
    max_index = 0

    for i in range(1, len(read_list)):
        if read_list[i].max_temp != '':
            if max < int(read_list[i].max_temp):
                max = int(read_list[i].max_temp)
                max_index = i

    return [max, max_index]


def find_lowest(read_list):
    min = int(read_list[0].min_temp)
    min_index = 0

    for i in range(1, len(read_list)):
        if read_list[i].min_temp != '':
            if min > int(read_list[i].min_temp):
                min = int(read_list[i].min_temp)
                min_index = i

    return [min, min_index]


def find_max_humidity(read_list):
    max = int(read_list[0].max_humidity)
    max_index = 0

    for i in range(1, len(read_list)):
        if read_list[i].max_humidity != '':
            if max < int(read_list[i].max_humidity):
                max = int(read_list[i].max_humidity)
                max_index = i

    return [max, max_index]


def main():
    get_argument_list()
    generate_reports(files_directory)


main()

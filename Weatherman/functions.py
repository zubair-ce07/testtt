from FIleGetters import get_file_names, get_file_names_one
from Classes import Weather , YearlyWeatherReport, MonthlyReport

def year(args):

    weather_files = get_file_names(args)
    weather_files_count = len(weather_files)

    yearly_report = YearlyWeatherReport()
    count = 0
    first_min_temp = 0

    for index in range(0, weather_files_count):

        f = open(weather_files[index], "r")

        line = f.readline()
        line = f.readline()

        first_line = line.split(',')

        first_min_temp = int(first_line[3])

        while line:

            splitted_line = line.split(',')
            weather = Weather(splitted_line)

            if weather.max_temp and int(weather.max_temp) > yearly_report.highest_temp:
                yearly_report.highest_temp = int(weather.max_temp)
                yearly_report.highest_temp_day = weather.get_month_day()

            if count >= 1:
                    if weather.min_temp and int(weather.max_temp) < yearly_report.lowest_temp:
                        yearly_report.lowest_temp = int(weather.max_temp)
                        yearly_report.lowest_temp_day = weather.get_month_day()
            else:
                    yearly_report.lowest_temp_day = weather.get_month_day()
                    yearly_report.lowest_temp = first_min_temp

            if weather.max_humidity and int(weather.max_humidity) > yearly_report.highest_humidity:
                yearly_report.highest_humidity = int(weather.max_humidity)
                yearly_report.highest_humidity_day = weather.get_month_day()

            count = count + 1
            line = f.readline()

    yearly_report.results()


def month(args):


    files_list = get_file_names_one(args)

    monthly_report = MonthlyReport()

    f = open(files_list[0], "r")

    line = f.readline()
    line = f.readline()
    first = line.split(',')



    while line:

        splited_line = line.split(',')
        weather = Weather(splited_line)


        monthly_report.days_count = monthly_report.days_count + 1

        if weather.max_temp:
            monthly_report.total_max_temp = monthly_report.total_max_temp + int(weather.max_temp)

        if weather.min_temp:
            monthly_report.total_min_temp = monthly_report.total_min_temp + int(weather.min_temp)

        if weather.mean_humidity:
            monthly_report.total_mean_humidity = monthly_report.total_mean_humidity + int(weather.mean_humidity)

        line = f.readline()

    monthly_report.results()

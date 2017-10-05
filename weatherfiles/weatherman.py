import sys
import os
import fnmatch

class MonthlyWeatherInfo:
    def __init__(self, weather_info_list):
        del(weather_info_list[0])
        self.month = weather_info_list[0].split(',')[0]
        self.daily_weathers_info = [DailyWeatherInfo(weather_info) for weather_info in weather_info_list]


class DailyWeatherInfo:
    def __init__(self, weather_info_string):
        weather_info = weather_info_string.split(',')
        self.date = weather_info[0]
        self.max_temp = weather_info[1]
        self.mean_temp = weather_info[2]
        self.min_temp = weather_info[3]
        self.max_humidity = weather_info[7]
        self.mean_humidity = weather_info[8]
        self.min_humidity = weather_info[9]

class ReportGeneratorFactory:
    def get_report_generator(self, option):
        if option == '-e':
            return EReportGenerator()

class ReportGenerator:
    def generate_report(self, data):
        return

class EReportGenerator(ReportGenerator):
    def generate_report(self, data):
        print(data[0].month)
        print(data[0].daily_weathers_info[0].max_temp)
        return


def get_filenames_from_dir(dir, year):
    filenames = []
    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, 'Murree_weather_' + year + '_*.txt'):
            filename = os.path.join(dir, file)
            filenames.append(filename)
    return filenames


def read_files(filenames):
    filesdata = {}
    for filename in filenames:
        filedata = open(filename, 'rU').readlines()
        filesdata[filename] = filedata
    return filesdata


def read_files_from_path(dir, year):
    filenames = get_filenames_from_dir(dir, year)
    filesdata = read_files(filenames)
    weathers_info = [MonthlyWeatherInfo(filedata) for filedata in filesdata.values()]
    return weathers_info


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('''usage: weatherman.py /path/to/files-dir -option year [-option year] [-option year]
        options: -a, -e, -c''')
        sys.exit(1)

    weathers_info = read_files_from_path(args[0], args[2])
    report_generator = ReportGeneratorFactory().get_report_generator(args[1])
    report_generator.generate_report(weathers_info)

if __name__ == '__main__':
    main()
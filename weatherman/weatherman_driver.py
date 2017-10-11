import os
import sys

from weatherman import WeatherReport


def parse_arguments():
    argv = sys.argv
    if len(argv) > 3 and len(argv):
        path_to_files = argv[1]
        options = {}
        while argv:
            if argv[0][0] == '-':
                options[argv[0]] = argv[1]
            argv = argv[1:]
        return options, path_to_files.split('-')[0]
    else:
        return None, None


def main():
    actions_to_perform, path_to_files = parse_arguments()
    if actions_to_perform and path_to_files:
        try:
            for root, dirs, file_names in os.walk(path_to_files):
                pass
            file_names.remove('.DS_Store')
            weather_report = WeatherReport(file_names)
            if '-e' in actions_to_perform:
                weather_report.get_yearly_weather_insights(actions_to_perform['-e'], path_to_files)
            if '-a' in actions_to_perform:
                weather_report.get_monthly_weather_insights(actions_to_perform['-a'], path_to_files)
            if '-c' in actions_to_perform:
                weather_report.get_days_weather_insights(actions_to_perform['-c'], path_to_files)

        except FileNotFoundError:
            print('Files path is incorrect')
    else:
        print("usage: weatherman.py /path/to/files-dir [option] [year/month] \n"
              "Options:\n"
              "-e\tYearly Report\n"
              "-a\tMonthly Report\n"
              "-c\tDaily Report")


if __name__ == "__main__":
    main()

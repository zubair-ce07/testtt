import os
import datetime
import argparse
import csv
import glob


class Color:
    PURPLE = '\033[95m'
    BLUE = '\033[34m'
    RED = '\033[91m'
    END = '\033[0m'


class Weatherman:

    def __init__(self, records):
        self.highest_temp = records.get('Max TemperatureC')
        self.date = records.get('PKT')


def check_validity_of_records(record):
    if (record.get("PKST") or record.get("PKT")) and record.get("Max TemperatureC") and \
            record.get("Min TemperatureC") and record.get("Max Humidity") and record.get(" Mean Humidity"):
        return True
    else:
        return False


def read_and_parse_data_reports(file_name):
    weather_records = [record for record in csv.DictReader(open(file_name))
                       if check_validity_of_records(record) is True]
    return weather_records


def calculate_yearly_report(required_date, all_weather_records):
    desired_records = []
    for record in all_weather_records:
        if record['PKT'].year == required_date.year:
            desired_records.append(record)
    highest_temp = max(desired_records, key=lambda x: x['Max TemperatureC'])
    lowest_temp = min(desired_records, key=lambda x: x['Min TemperatureC'])
    most_humid = max(desired_records, key=lambda x: x[' Mean Humidity'])
    return highest_temp, lowest_temp, most_humid


def generate_yearly_report(highest_temp, lowest_temp, most_humid):
    print(f'Highest: {highest_temp[0]} on {highest_temp[1]}')
    print(f'Highest: {lowest_temp[0]} on {lowest_temp[1]}')
    print(f'Highest: {most_humid[0]} on {most_humid[1]}')


def calculate_monthly_report(required_date, all_weather_records):
    desired_records = []
    for record in all_weather_records:
        if record['date'].year == required_date.year and record['date'].month == required_date.month:
            desired_records.append(record)
    highest_avg_temp = sum(desired_records, key=lambda x: x['Max TemperatureC']) / len(desired_records)
    lowest_avg_temp = sum(desired_records, key=lambda x: x['Min TemperatureC']) / len(desired_records)
    avg_mean_humid = sum(desired_records, key=lambda x: x['Max_Humidity']) / len(desired_records)
    return highest_avg_temp, lowest_avg_temp, avg_mean_humid


def generate_monthly_report(highest_avg_temp, lowest_avg_temp, avg_mean_humid):
    print(f'Highest: {highest_avg_temp[0]} on {highest_avg_temp[1]}')
    print(f'Highest: {lowest_avg_temp[0]} on {lowest_avg_temp[1]}')
    print(f'Highest: {avg_mean_humid[0]} on {avg_mean_humid[1]}')


def draw_two_line_monthly_chart(required_date, all_weather_records):
    desired_weatherman_entries = list(filter(lambda x: by and required_date.year in x and
                                                       required_date.month in x, self.entries.keys()))
    for entry in desired_weatherman_entries:
        print("{}, {}".format(required_date.month, required_date.year))
        for record in self.entries[entry]:
            max_temp = record.get('Max TemperatureC')
            min_temp = record.get('Min TemperatureC')
            if max_temp and min_temp:
                pkt = record.get("PKT") or record.get("PKST")
                print(Color.PURPLE + pkt + Color.RED + "+" * int(max_temp) + Color.PURPLE + " " + max_temp + "C")
                print(Color.PURPLE + pkt + Color.BLUE + "+" * int(min_temp) + Color.PURPLE + " " + min_temp + "C")
            print(Color.END + header_line)


def draw_one_line_monthly_bar_chart(required_date, all_weather_records):
    desired_weatherman_entries = list(filter(lambda x: by and required_date.year in x and
                                                       required_date.month in x, self.entries.keys()))
    for entry in desired_weatherman_entries:
        print("{}, {}".format(required_date.month, required_date.year))
        for record in self.entries[entry]:
            max_temp = record.get('Max TemperatureC')
            min_temp = record.get('Min TemperatureC')
            if max_temp and min_temp:
                pkt = record.get("PKT") or record.get("PKST")
                print(Color.PURPLE + pkt + Color.BLUE + "+" * int(min_temp) + Color.RED + "+" * int(
                    max_temp) + Color.PURPLE + " " + min_temp + "C-" + max_temp + "C")
            print(Color.END + header_line)


def main():
    parser = argparse.ArgumentParser(description='Displaying Murree weather reports')
    parser.add_argument('path', help='Path of directory')
    parser.add_argument('-e', '--year_to_report', type=lambda d: datetime.datetime.strptime(d, '%Y').date())

    parser.add_argument('-a', '--month_to_report', type=lambda d: datetime.datetime.strptime(d, '%Y/%m').date())

    parser.add_argument('-c', '--plot_graph', type=lambda d: datetime.datetime.strptime(d, '%Y/%m').date())
    args = parser.parse_args()
    all_weather_records = []
    files_path = f'*{args.path}/.txt'
    for file_name in glob.glob(files_path):
        all_weather_records += read_and_parse_data_reports(file_name)
    if args.year_to_report:
        highest_temp, lowest_temp, most_humid = calculate_yearly_report(args.year_to_report, all_weather_records)
        generate_yearly_report(highest_temp, lowest_temp, most_humid)
    if args.month_to_report:
        avg_highest_temp, avg_lowest_temp, avg_most_humid = calculate_monthly_report(args.month_to_report,
                                                                                     all_weather_records)
        generate_monthly_report(avg_highest_temp, avg_lowest_temp, avg_most_humid)
    if args.plot_graph:
        draw_two_line_monthly_chart(args.plot_graph, all_weather_records)
        draw_one_line_monthly_bar_chart(args.plot_graph, all_weather_records)


if __name__ == "__main__":
    main()

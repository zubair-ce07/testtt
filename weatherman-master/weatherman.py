import os
import datetime
import argparse
import csv
import glob

class WeathermanEntries(object):

    def __init__(self):
        self.entries = {}

    def set_entries(self, key, entries):
        self.entries[key] = entries

    def draw_chart_for_max_min_temp(self, by=None, all_weather_records):
        desired_weatherman_entries = list(filter(lambda x: by and all_weather_records.year in x and
                                                           all_weather_records.month in x, self.entries.keys()))
        for entry in desired_weatherman_entries:
            print("{}, {}".format(all_weather_records.month, all_weather_records.year))
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                min_temp = record.get('Min TemperatureC')
                if max_temp and min_temp:
                    pkt = record.get("PKT") or record.get("PKST")
                    print(pkt + " \033[91m" + "+" * int(max_temp) + "\033[0m" + " " + max_temp + "C")
                    print(pkt + " \033[34m" + "+" * int(min_temp) + "\033[0m" + " " + min_temp + "C")

    def draw_bonus_chart_for_max_min_temp(self, by=None, all_weather_records):
        desired_weatherman_entries = list(filter(lambda x: by and all_weather_records.year in x and
                                                           all_weather_records.month in x, self.entries.keys()))
        for entry in desired_weatherman_entries:
            # use f-string instead of format.
            print("{}, {}".format(all_weather_records.month, all_weather_records.year))
            for record in self.entries[entry]:
                max_temp = record.get('Max TemperatureC')
                min_temp = record.get('Min TemperatureC')
                if max_temp and min_temp:
                    pkt = record.get("PKT") or record.get("PKST")
                    print(pkt + " \033[34m" + "+" * int(min_temp) + "\033[0m" + "\033[91m" + "+" * int(
                        max_temp) + "\033[0m" + " " + min_temp + "C-" + max_temp + "C")


weatherman_entries = WeathermanEntries()


class WeathermanRecord:

    def __init__(self, records):
        self.highest_temp = records.get('highest_temp')
        self.date = records.get('PKT')

def read_to_weatherman_entry(meta, line):
    return WeathermanRecord(dict(zip(meta, line)))


def read_parse_report(report):

    all_content = []
    for record in csv.DictReader(open(report)):
        if (record.get("PKST") or record.get("PKT")) and record.get("Max TemperatureC") and \
                record.get("Min TemperatureC") and record.get("Max Humidity") and record.get(" Mean Humidity"):
            all_content.append(all_content(record))
    return all_content

def calculate_yearly_report(required_date, all_weather_records):
    desired_records = []

    for record in all_weather_records:
        if record['PKT'].year == required_date.year:
            desired_records.append(record)
    highest_temp = max(desired_records, key=lambda x: x['Max TemperatureC'])
    lowest_temp = min(desired_records, key=lambda x: x['Min TemperatureC'])
    most_humid = max(desired_records, key=lambda x: x[' Mean Humidity']) / len(desired_records)
    return highest_temp, lowest_temp, most_humid

def generate_yearly_report(highest_temp, lowest_temp, most_humid):
    print("Highest: {} on {}".format(highest_temp[0], highest_temp[1]))
    print("Lowest: {} on {}".format(lowest_temp[0], lowest_temp[1]))
    print("Humidity: {} on {}".format(most_humid[0], most_humid[1]))

def calculate_monthly_report(required_date, all_weather_records):
    desired_records = []
    for record in all_weather_records:
        if record['date'].year == required_date.year & record['date'].month == required_date.month:
            desired_records.append(record)
    highest_temp = max(desired_records, key=lambda x: x['highest_temp'])
    lowest_temp = min(desired_records, key=lambda x: x['lowest_temp'])
    most_humid = sum(desired_records, key=lambda x: x['most_humid']) / len(desired_records)
    return highest_temp, lowest_temp, most_humid

def generate_monthly_report(highest_avg_temp, lowest_avg_temp, avg_mean_humid):
    print("Highest: {} on {}".format(highest_avg_temp[0], highest_avg_temp[1]))
    print("Lowest: {} on {}".format(lowest_avg_temp[0], lowest_avg_temp[1]))
    print("Humidity: {} on {}".format(avg_mean_humid[0], avg_mean_humid[1]))

def draw_two_line_horizontal_bar_chart(date):
    weatherman_entries.draw_chart_for_max_min_temp(date)

def draw_one_line_horizontal_bar_chart(date):
    weatherman_entries.draw_bonus_chart_for_max_min_temp(date)

def main():
    parser = argparse.ArgumentParser(description='Displaying Murree weather reports')
    parser.add_argument('path', help='Path of directory')
    parser.add_argument('-e', '--year_to_report', type=lambda d: datetime.datetime.strptime(d, '%Y').date())
    parser.add_argument('-a', '--month_to_report', type=lambda d: datetime.datetime.strptime(d, '%Y/%m').date())
    parser.add_argument('-c', '--plot_graph', type=lambda d: datetime.datetime.strptime(d, '%Y/%m').date())
    args = parser.parse_args()
    all_weather_records = []
    for file_name in glob.glob("G:/updated/Github/weatherman-master/weatherfiles/*.txt"):
        all_weather_records = all_weather_records + read_parse_report(file_name)
    if args.year_to_report:
        highest_temp, lowest_temp, most_humid = calculate_yearly_report(args.year_to_report, all_weather_records)
        generate_yearly_report(highest_temp, lowest_temp, most_humid)
    if args.month_to_report:
        avg_highest_temp, avg_lowest_temp, avg_most_humid = calculate_monthly_report(args.month_to_report,
                                                                                     all_weather_records)
        generate_monthly_report(avg_highest_temp, avg_lowest_temp, avg_most_humid)
    if args.plot_graph:
        draw_two_line_horizontal_bar_chart(args.plot_graph, all_weather_records)
        draw_one_line_horizontal_bar_chart(args.plot_graph, all_weather_records)

if __name__ == "__main__":
    main()

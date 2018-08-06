from __future__ import print_function
import os
import glob
import sys
import csv
import argparse

month_names = {
    "1": "Jan", "2": "Feb",
    "3": "Mar", "4": "Apr",
    "5": "May", "6": "Jun",
    "7": "Jul", "8": "Aug",
    "9": "Sep", "10": "Oct",
    "11": "Nov", "12": "Dec"
}


class WeatherRecord:

    def __init__(self):
        self.weather_data = None

    def file_reader(self, folder_path):
        txt_files = glob.glob(folder_path + "/*.txt")  # Read text files
        self.weather_data = []

        for txt_file in txt_files:
            with open(txt_file, 'r') as opened_file:
                csv_reader = csv.DictReader(opened_file)
                for line in csv_reader:
                    year_month_date = (line.get("PKST") or
                                       line.get("PKT")
                                       ).split('-')
                    self.weather_data.append(
                        self.data_populater(
                            line, year_month_date))

    def data_populater(self, data, year_month_date):
        sub_key_level_dictionary = {
            str(year_month_date[0]): {
                str(year_month_date[1]): {
                    str(year_month_date[2]):
                    data
                }
            }
        }
        return sub_key_level_dictionary


class ResultsCalculator:

    def __init__(self):
        self.calculated_results = {}

    def daily_temp_calc(self, weather_data, year, month):
        self.calculated_results = {
            "Month": month_names[month], "Year": year
        }
        self.calculated_results.setdefault("MaxTempreture", {})
        self.calculated_results.setdefault("MinTemperature", {})

        for data in weather_data:
            year_level_data = data.get(year)
            if year_level_data:
                month_level_data = year_level_data.get(month)
                if month_level_data:
                    for day in month_level_data:
                        day_level_data = month_level_data.get(day)
                        if day_level_data.get("Max TemperatureC"):
                            self.calculated_results["MaxTempreture"].update({
                                str(day): day_level_data.get("Max TemperatureC")})

                        if day_level_data.get("Min TemperatureC"):
                            self.calculated_results["MinTemperature"].update({
                                str(day): day_level_data.get("Min TemperatureC")})

    def monthly_temp_n_humidity_calc(
            self, weather_data, year, month):
        self.calculated_results = {
            "HighestAverage": 0, "LowestAverage": 0, "AverageMeanHumidity": 0
        }
        total_days = 0

        for data in weather_data:
            year_level_data = data.get(year)
            if year_level_data:
                month_level_data = year_level_data.get(month)
                if month_level_data:
                    for day in month_level_data:
                        total_days += 1
                        day_level_data = month_level_data.get(day)
                        if day_level_data.get("Max TemperatureC"):
                            self.calculated_results["HighestAverage"] = (
                                float(day_level_data.get("Max TemperatureC"))
                                + float(self.calculated_results["HighestAverage"]))

                        if day_level_data.get("Min TemperatureC"):
                            self.calculated_results["LowestAverage"] = (
                                float(day_level_data.get("Min TemperatureC"))
                                + float(self.calculated_results["LowestAverage"]))

                        if day_level_data.get(" Mean Humidity"):
                            self.calculated_results["AverageMeanHumidity"] = (
                                float(day_level_data.get(" Mean Humidity"))
                                + float(self.calculated_results["AverageMeanHumidity"]))

        self.calculated_results["HighestAverage"] = int(
            self.calculated_results["HighestAverage"]
            / total_days
        )
        self.calculated_results["LowestAverage"] = int(
            self.calculated_results["LowestAverage"]
            / total_days
        )
        self.calculated_results["AverageMeanHumidity"] = int(
            self.calculated_results["AverageMeanHumidity"]
            / total_days
        )

    def yearly_temp_n_humidity_calc(self, weather_data, year):
        first_iteration = True  # Flag to memorize to do initial setup

        for data in weather_data:
            year_level_data = data.get(year)
            if year_level_data:
                for month in year_level_data:
                    month_level_data = year_level_data.get(month)
                    for day in month_level_data:
                        temp_data = month_level_data.get(day)
                        if first_iteration:
                            first_iteration = False
                            self.calculated_results = {
                                "MaxYearlyTempreature": (
                                    temp_data.get("Max TemperatureC")
                                ), "HighestTempretureDay": day, "HighestTempretureMonth": (
                                    month_names[month]
                                ), "MinYearlyTempreature": (
                                    temp_data.get("Min TemperatureC")
                                ), "LowestTempretureDay": day, "LowestTempretureMonth": (
                                    month_names[month]
                                ), "Humidity": (
                                    temp_data.get(" Mean Humidity")
                                ), "MostHumidDay": day, "MostHumidMonth": (
                                    month_names[month]
                                )
                            }
                        elif ((temp_data.get("Max TemperatureC")
                                or temp_data.get("Min TemperatureC"))
                                and temp_data.get(" Mean Humidity")):

                            if (float(temp_data.get("Max TemperatureC")) 
                                    > float(self.calculated_results.get("MaxYearlyTempreature"))):
                                self.calculated_results["MaxYearlyTempreature"] = (
                                    temp_data.get("Max TemperatureC"))
                                self.calculated_results["HighestTempretureMonth"] = month_names[month]
                                self.calculated_results["HighestTempretureDay"] = day
                            elif (float(temp_data.get("Min TemperatureC"))
                                    < float(self.calculated_results.get("MinYearlyTempreature"))):
                                self.calculated_results["MinYearlyTempreature"] = (
                                    temp_data.get("Min TemperatureC"))
                                self.calculated_results["LowestTempretureMonth"] = (
                                    month_names[month])
                                self.calculated_results["LowestTempretureDay"] = day

                            if(float(temp_data.get(" Mean Humidity")) 
                                    > float(self.calculated_results.get("Humidity"))):
                                self.calculated_results["Humidity"] = (
                                    temp_data.get(" Mean Humidity")
                                )
                                self.calculated_results["MostHumidDay"] = day
                                self.calculated_results["MostHumidMonth"] = (
                                    month_names[month]
                                )


class ReportsGenrator:

    def __init__(self):
        pass

    def yearly_report_genrator(self, calculated_results):
        print("Highest: {} C on {} {}".format(
            calculated_results["MaxYearlyTempreature"],
            calculated_results["HighestTempretureDay"],
            calculated_results["HighestTempretureMonth"]
        ))
        print("Lowest: {} C on {} {}".format(
            calculated_results["MinYearlyTempreature"],
            calculated_results["LowestTempretureDay"],
            calculated_results["LowestTempretureMonth"]
        ))
        print("Humidity: {}% on {}".format(
            calculated_results["MostHumidDay"],
            calculated_results["MostHumidMonth"]
        ))

    def monthly_report_genrator(self, calculated_results):
        print("Highest Average: {} C".format(
            calculated_results["HighestAverage"]
        ))
        print("Lowest Average: {} C".format(
            calculated_results["LowestAverage"]
        ))
        print("Average Mean Humidity: {}%".format(
            calculated_results["AverageMeanHumidity"]
        ))

    def daily_report_genrator(self, calculated_results, caller_flag):
        print("{} {}".format(
            calculated_results["Month"],
            calculated_results["Year"]
        ))
        daily_max_data = calculated_results.get("MaxTempreture")
        daily_min_data = calculated_results.get("MinTemperature")

        if caller_flag:  # Called from daily calculator
            for day in zip(daily_max_data, daily_min_data):
                print(day[0], end="")
                for iterator in range(0, int(daily_max_data.get(day[0]))):
                    sys.stdout.write("\033[1;31m")  # Red color
                    print("+", end="")
                    sys.stdout.write("\033[1;00m")  # White
                print(" {} C".format(daily_max_data.get(day[0])))
                print(day[0], end="")
                for iterator in range(0, int(daily_min_data.get(day[0]))):
                    sys.stdout.write("\033[1;34m")  # Blue color
                    print("+", end="")
                    sys.stdout.write("\033[1;00m")  # White
                print(" {} C".format(daily_min_data.get(day[0])))

        else:
            for day in zip(daily_max_data, daily_min_data):
                print(day[0], end="")
                for iterator in range(0, int(daily_min_data.get(day[0]))):
                    sys.stdout.write("\033[1;34m")  # Blue color
                    print("+", end="")
                    sys.stdout.write("\033[1;00m")  # White

                for iterator in range(0, int(daily_max_data.get(day[0]))):
                    sys.stdout.write("\033[1;31m")  # Red color
                    print("+", end="")
                    sys.stdout.write("\033[1;00m")  # White
                print(" {} C".format(daily_min_data.get(day[0])), end="")
                print(" - {} C".format(daily_max_data.get(day[0])))


class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(
            namespace,
            self.dest,
            os.path.abspath(
                os.path.expanduser(values)))


def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname

def input_parser():
    parser = argparse.ArgumentParser()
    # Match file path
    parser.add_argument(
        'directory',
        help="Path to directory containing data",
        action=FullPaths,
        type=is_dir)
    parser.add_argument("-c", help="Daily Report")
    parser.add_argument("-e", help="Yearly Report")
    parser.add_argument("-a", help="Monthly Report")
    parser.add_argument("-b", help="Detailed Monthly Report")
    args = parser.parse_args()

    weather_record = WeatherRecord()
    weather_record.file_reader(args.directory)

    results_calculator = ResultsCalculator()

    reports_genrator = ReportsGenrator()
    if args.a:
        year_n_month = args.a.split("/")
        results_calculator.monthly_temp_n_humidity_calc(
            weather_record.weather_data, 
            year = year_n_month[0], month = year_n_month[1]
        )
        reports_genrator.monthly_report_genrator(
            results_calculator.calculated_results
        )


    if args.e:
        results_calculator.yearly_temp_n_humidity_calc(
            weather_record.weather_data, year=str(args.e)
        )
        reports_genrator.yearly_report_genrator(
            results_calculator.calculated_results
        )

    if args.c:
        year_n_month = args.c.split("/")
        year_n_month[1] = year_n_month[1].replace("0", "")
        results_calculator.daily_temp_calc(
            weather_record.weather_data,
            year = year_n_month[0], month = year_n_month[1]
        )
        reports_genrator.daily_report_genrator(
            results_calculator.calculated_results,
            caller_flag = True
        )
    
    if args.b:
        year_n_month = args.c.split("/")
        year_n_month[1] = year_n_month[1].replace("0", "")
        results_calculator.daily_temp_calc(
            weather_record.weather_data,
            year = year_n_month[0], month = year_n_month[1]
        )
        reports_genrator.daily_report_genrator(
            results_calculator.calculated_results,
            caller_flag = False
        )
        

if __name__ == "__main__":
    input_parser()
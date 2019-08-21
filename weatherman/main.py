import argparse
import calendar
import csv
import datetime
import glob


class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        try:
            self.file = open(self.filename, self.mode)
            self.file.__next__()
            csv_reader = csv.DictReader(self.file)
            return csv_reader
        except EnvironmentError:
            print("%s File not found" % self.filename)
            return []

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not self.file.closed:
            self.file.close()


class Formatter:
    @staticmethod
    def display_extremes(results):
        print("\n\nHighest: {}C on {} {}".format(
            results["highest"],
            datetime.datetime.strptime(results["highest_day"], "%Y-%m-%d").strftime("%b"),
            datetime.datetime.strptime(results["highest_day"], "%Y-%m-%d").day))
        print("Lowest: {}C on {} {}".format(
            results["lowest"],
            datetime.datetime.strptime(results["lowest_day"], "%Y-%m-%d").strftime("%b"),
            datetime.datetime.strptime(results["lowest_day"], "%Y-%m-%d").day))
        print("Humid: {}C on {} {}".format(
            results["humid"],
            datetime.datetime.strptime(results["humid_day"], "%Y-%m-%d").strftime("%b"),
            datetime.datetime.strptime(results["humid_day"], "%Y-%m-%d").day))

    @staticmethod
    def display_averages(results):
        print("\n\nHighest Average: {}C".format(int(results["sum_high_temp"] / results["days_high_temp"])))
        print("Lowest Average: {}C".format(int(results["sum_low_temp"] / results["days_low_temp"])))
        print("Average Humidity: {}".format(int(results["sum_humidity"] / results["days_humidity"])))

    @staticmethod
    def display_bars(results):
        for day, bars in results.items():
            print("{}\033[0;32;40m {}\033[0;31;40m{} \033[0;37;40m{}C - {}C \n".format(
                day, bars[0], bars[1], len(bars[0]), len(bars[1])))


class Operations:
    def find_extremes(self, files):
        results = {}
        for file in files:
            with FileManager(file, 'r') as rows:
                rows.__next__()
                for row in rows:
                    flag, high, max_day = self.get_max_temperature(row, results)
                    if flag:
                        results["highest"], results["highest_day"] = high, max_day

                    flag, low, low_day = self.get_lowest_temperature(row, results)
                    if flag:
                        results["lowest"], results["lowest_day"] = low, low_day

                    flag, humid, humid_day = self.get_max_humidity(row, results)
                    if flag:
                        results["humid"], results["humid_day"] = humid, humid_day
        return results

    @staticmethod
    def get_max_temperature(row, results):
        if ("highest" not in results and row["Max TemperatureC"]) \
                or (row["Max TemperatureC"]
                    and int(row["Max TemperatureC"]) > results["highest"]):
            keys = list(row.keys())
            return True, int(row["Max TemperatureC"]), row[keys[0]]
        return False, None, None

    @staticmethod
    def get_lowest_temperature(row, results):
        if ("lowest" not in results and row["Min TemperatureC"]) \
                or (row["Min TemperatureC"]
                    and int(row["Min TemperatureC"]) < results["lowest"]):
            keys = list(row.keys())
            return True, int(row["Min TemperatureC"]), row[keys[0]]
        return False, None, None

    @staticmethod
    def get_max_humidity(row, results):
        if ("humid" not in results and row["Max Humidity"]) \
                or (row["Max Humidity"]
                    and int(row["Max Humidity"]) > results["humid"]):
            keys = list(row.keys())
            return True, int(row["Max Humidity"]), row[keys[0]]
        return False, None, None

    @staticmethod
    def calculate_averages(file):
        results = {
            "sum_high_temp": 0,
            "days_high_temp": 0,
            "sum_low_temp": 0,
            "days_low_temp": 0,
            "sum_humidity": 0,
            "days_humidity": 0,
        }
        with FileManager(file, 'r') as rows:
            rows.__next__()
            for row in rows:
                if row["Max TemperatureC"]:
                    results["sum_high_temp"] += int(row["Max TemperatureC"])
                    results["days_high_temp"] += 1
                if row["Min TemperatureC"]:
                    results["sum_low_temp"] += int(row["Min TemperatureC"])
                    results["days_low_temp"] += 1
                if row[" Mean Humidity"]:
                    results["sum_humidity"] += int(row[" Mean Humidity"])
                    results["days_humidity"] += 1
        return results

    @staticmethod
    def generate_bars(file):
        results = {}
        with FileManager(file, 'r') as rows:
            for row in rows:
                low_temp_str = ''
                high_temp_str = ''
                keys = list(row.keys())

                if row["Min TemperatureC"]:
                    for x in range(int(row["Min TemperatureC"])):
                        high_temp_str += '+'
                if row["Max TemperatureC"]:
                    for x in range(int(row["Max TemperatureC"])):
                        low_temp_str += '+'
                results[row[keys[0]]] = [low_temp_str, high_temp_str]
        return results


def parse_arguments():
    parser = argparse.ArgumentParser(description='Weatherman app')
    parser.add_argument('-e', "--extremes", action="store_true", help='find extreme conditions during e whole year')
    parser.add_argument('-a', "--averages", action="store_true", help='find average conditions during a month')
    parser.add_argument('-c', "--colours", action="store_true", help='print temperature bars during a month')
    parser.add_argument('time_span', type=str, help='time span on which the operation should be performed')
    parser.add_argument('indir', type=str, help='Input dir for data files')
    args = parser.parse_args()
    return args


def main():
    ops = Operations()
    fmt = Formatter()
    args = parse_arguments()
    all_files = glob.glob(args.indir + "/*.txt")
    if args.extremes:
        files_to_read = []
        for file in all_files:
            if file.__contains__(args.time_span):
                files_to_read.append(file)
        fmt.display_extremes(ops.find_extremes(files_to_read))
    elif args.averages:
        year, mon = args.time_span.split("/")[0], args.time_span.split("/")[1]
        file_to_read = ''
        for file in all_files:
            if file.__contains__(year) and file.__contains__(calendar.month_abbr[int(mon)]):
                file_to_read = file
        fmt.display_averages(ops.calculate_averages(file_to_read))
    elif args.colours:
        year, mon = args.time_span.split("/")[0], args.time_span.split("/")[1]
        file_to_read = ''
        for file in all_files:
            if file.__contains__(year) and file.__contains__(calendar.month_abbr[int(mon)]):
                file_to_read = file
        fmt.display_bars(ops.generate_bars(file_to_read))
    else:
        print("Operation unknown")


if __name__ == '__main__':
    main()

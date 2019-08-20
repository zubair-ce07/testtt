import csv
import datetime
import glob
import sys

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


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
        print("\n\nHighest: %sC on %s %s"
              % (results["highest"],
                 datetime.datetime.strptime(results["highest_day"], "%Y-%m-%d").strftime("%b"),
                 datetime.datetime.strptime(results["highest_day"], "%Y-%m-%d").day))
        print("Lowest: %sC on %s %s"
              % (results["lowest"],
                 datetime.datetime.strptime(results["lowest_day"], "%Y-%m-%d").strftime("%b"),
                 datetime.datetime.strptime(results["lowest_day"], "%Y-%m-%d").day))
        print("Humid: %sC on %s %s"
              % (results["humid"],
                 datetime.datetime.strptime(results["humid_day"], "%Y-%m-%d").strftime("%b"),
                 datetime.datetime.strptime(results["humid_day"], "%Y-%m-%d").day))

    @staticmethod
    def display_averages(results):
        print("\n\nHighest Average: %dC" % (results["sum_high_temp"] / results["days_high_temp"]))
        print("Lowest Average: %dC" % (results["sum_low_temp"] / results["days_low_temp"]))
        print("Average Humidity: %d" % (results["sum_humidity"] / results["days_humidity"]))

    @staticmethod
    def display_bars(results):
        for day, bars in results.items():
            print("%s\033[0;32;40m %s\033[0;31;40m%s \033[0;37;40m%sC - %sC \n"
                  % (day, bars[0], bars[1], len(bars[0]), len(bars[1])))


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
        if ("highest" not in results and row["Max TemperatureC"] != '') \
                or (row["Max TemperatureC"] != ''
                    and row["Max TemperatureC"] is not None
                    and int(row["Max TemperatureC"]) > results["highest"]):
            keys = list(row.keys())
            return True, int(row["Max TemperatureC"]), row[keys[0]]
        return False, None, None

    @staticmethod
    def get_lowest_temperature(row, results):
        if ("lowest" not in results and row["Min TemperatureC"] != '') \
                or (row["Min TemperatureC"] != ''
                    and row["Min TemperatureC"] is not None
                    and int(row["Min TemperatureC"]) < results["lowest"]):
            keys = list(row.keys())
            return True, int(row["Min TemperatureC"]), row[keys[0]]
        return False, None, None

    @staticmethod
    def get_max_humidity(row, results):
        if ("humid" not in results and row["Max Humidity"] != '') \
                or (row["Max Humidity"] != ''
                    and row["Max Humidity"] is not None
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
                if row["Max TemperatureC"] != '' and row["Max TemperatureC"] is not None:
                    results["sum_high_temp"] += int(row["Max TemperatureC"])
                    results["days_high_temp"] += 1
                if row["Min TemperatureC"] != '' and row["Min TemperatureC"] is not None:
                    results["sum_low_temp"] += int(row["Min TemperatureC"])
                    results["days_low_temp"] += 1
                if row[" Mean Humidity"] != '' and row[" Mean Humidity"] is not None:
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

                if row["Min TemperatureC"] != '' and row["Min TemperatureC"] is not None:
                    for x in range(int(row["Min TemperatureC"])):
                        high_temp_str += '+'
                if row["Max TemperatureC"] != '' and row["Max TemperatureC"] is not None:
                    for x in range(int(row["Max TemperatureC"])):
                        low_temp_str += '+'
                results[row[keys[0]]] = [low_temp_str, high_temp_str]
        return results


def main():
    args = sys.argv
    ops = Operations()
    fmt = Formatter()
    all_files = glob.glob(args[3] + "/*.txt")
    if args[1] == "-e":
        files_to_read = []
        for file in all_files:
            if file.__contains__(args[2]):
                files_to_read.append(file)
        fmt.display_extremes(ops.find_extremes(files_to_read))
    elif args[1] == "-a":
        year, mon = args[2].split("/")[0], args[2].split("/")[1]
        file_to_read = ''
        for file in all_files:
            if file.__contains__(year) and file.__contains__(months[int(mon) - 1]):
                file_to_read = file
        fmt.display_averages(ops.calculate_averages(file_to_read))
    elif args[1] == "-c":
        year, mon = args[2].split("/")[0], args[2].split("/")[1]
        file_to_read = ''
        for file in all_files:
            if file.__contains__(year) and file.__contains__(months[int(mon) - 1]):
                file_to_read = file
        fmt.display_bars(ops.generate_bars(file_to_read))
    else:
        print("Operation unknown")


if __name__ == '__main__':
    main()

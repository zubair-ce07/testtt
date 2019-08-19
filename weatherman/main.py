import csv
import sys

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class FileReader:
    def read(self, path):
        try:
            csv_file = open(path, mode='r')
            csv_file.__next__()
            csv_reader = csv.DictReader(csv_file)
            return csv_reader
        except EnvironmentError:
            print("%s File not found" % path)
            return []


class Formatter:
    def display_extremes(self, results):
        print("\n\nHighest: %sC on %s %s"
              % (results["highest"],
                 months[int(results["highest_day"].split("-")[1]) - 1],
                 results["highest_day"].split("-")[2]))
        print("Lowest: %sC on %s %s"
              % (results["lowest"],
                 months[int(results["lowest_day"].split("-")[1]) - 1],
                 results["lowest_day"].split("-")[2]))
        print("Humid: %sC on %s %s"
              % (results["humid"],
                 months[int(results["humid_day"].split("-")[1]) - 1],
                 results["humid_day"].split("-")[2]))

    def display_averages(self, results):
        print("\n\nHighest Average: %dC" % (results["sum_high_temp"] / results["days_high_temp"]))
        print("Lowest Average: %dC" % (results["sum_low_temp"] / results["days_low_temp"]))
        print("Average Humidity: %d" % (results["sum_humidity"] / results["days_humidity"]))

    def display_bars(self, results):
        for day, bars in results.items():
            print("%s\033[0;32;40m %s\033[0;31;40m%s \033[0;37;40m%sC - %sC \n"
                  % (day, bars[0], bars[1], len(bars[0]), len(bars[1])))


class Operations:
    def find_extremes(self, args):
        results = {}
        for month in months:
            abs_file_path = ("%s/lahore_weather_%s_%s.txt" % (args[3], args[2], month))
            rows = FileReader().read(abs_file_path)
            line_count = 0
            for row in rows:
                if line_count > 0:
                    flag, high, max_day = self.get_max_temperature(row, results)
                    if flag:
                        results["highest"], results["highest_day"] = high, max_day

                    flag, low, low_day = self.get_lowest_temperature(row, results)
                    if flag:
                        results["lowest"], results["lowest_day"] = low, low_day

                    flag, humid, humid_day = self.get_max_humidity(row, results)
                    if flag:
                        results["humid"], results["humid_day"] = humid, humid_day

                line_count += 1
        return results

    def get_max_temperature(self, row, results):
        if ("highest" not in results and row["Max TemperatureC"] != '') \
                or (row["Max TemperatureC"] != ''
                    and row["Max TemperatureC"] is not None
                    and int(row["Max TemperatureC"]) > results["highest"]):
            keys = list(row.keys())
            return True, int(row["Max TemperatureC"]), row[keys[0]]
        return False, None, None

    def get_lowest_temperature(self, row, results):
        if ("lowest" not in results and row["Min TemperatureC"] != '') \
                or (row["Min TemperatureC"] != ''
                    and row["Min TemperatureC"] is not None
                    and int(row["Min TemperatureC"]) < results["lowest"]):
            keys = list(row.keys())
            return True, int(row["Min TemperatureC"]), row[keys[0]]
        return False, None, None

    def get_max_humidity(self, row, results):
        if ("humid" not in results and row["Max Humidity"] != '') \
                or (row["Max Humidity"] != ''
                    and row["Max Humidity"] is not None
                    and int(row["Max Humidity"]) > results["humid"]):
            keys = list(row.keys())
            return True, int(row["Max Humidity"]), row[keys[0]]
        return False, None, None

    def calculate_averages(self, args):
        abs_file_path = ("%s/lahore_weather_%s_%s.txt"
                         % (args[3], args[2].split("/")[0], months[int(args[2].split("/")[1]) - 1]))
        rows = FileReader().read(abs_file_path)
        results = {
            "sum_high_temp": 0,
            "days_high_temp": 0,
            "sum_low_temp": 0,
            "days_low_temp": 0,
            "sum_humidity": 0,
            "days_humidity": 0,
        }
        line_count = 0
        for row in rows:
            if line_count > 0:
                if row["Max TemperatureC"] != '' and row["Max TemperatureC"] is not None:
                    results["sum_high_temp"] += int(row["Max TemperatureC"])
                    results["days_high_temp"] += 1
                if row["Min TemperatureC"] != '' and row["Min TemperatureC"] is not None:
                    results["sum_low_temp"] += int(row["Min TemperatureC"])
                    results["days_low_temp"] += 1
                if row[" Mean Humidity"] != '' and row[" Mean Humidity"] is not None:
                    results["sum_humidity"] += int(row[" Mean Humidity"])
                    results["days_humidity"] += 1
            line_count += 1
        return results

    def generate_bars(self, args):
        abs_file_path = ("%s/lahore_weather_%s_%s.txt"
                         % (args[3], args[2].split("/")[0], months[int(args[2].split("/")[1]) - 1]))
        rows = FileReader().read(abs_file_path)
        results = {}

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
    if args[1] == "-e":
        fmt.display_extremes(ops.find_extremes(args))
    elif args[1] == "-a":
        fmt.display_averages(ops.calculate_averages(args))
    elif args[1] == "-c":
        fmt.display_bars(ops.generate_bars(args))
    else:
        print("Operation unknown")


if __name__ == '__main__':
    main()

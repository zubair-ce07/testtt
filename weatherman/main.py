import argparse
import calendar
import csv
import datetime
import glob


class FileManager:
    @staticmethod
    def read(filename, mode):
        csv_file = open(filename, mode)
        csv_file.__next__()
        dict_reader = csv.DictReader(csv_file)
        for row in dict_reader:
            yield row


class Formatter:
    @staticmethod
    def display_extremes(result):
        print("\n\nHighest: {}C on {} {}".format(
            result["highest"],
            datetime.datetime.strptime(result["highest_day"], "%Y-%m-%d").strftime("%b"),
            datetime.datetime.strptime(result["highest_day"], "%Y-%m-%d").day))
        print("Lowest: {}C on {} {}".format(
            result["lowest"],
            datetime.datetime.strptime(result["lowest_day"], "%Y-%m-%d").strftime("%b"),
            datetime.datetime.strptime(result["lowest_day"], "%Y-%m-%d").day))
        print("Humid: {}C on {} {}".format(
            result["humid"],
            datetime.datetime.strptime(result["humid_day"], "%Y-%m-%d").strftime("%b"),
            datetime.datetime.strptime(result["humid_day"], "%Y-%m-%d").day))

    @staticmethod
    def display_averages(result):
        print("\n\nHighest Average: {}C".format(result["avg_high_temp"]))
        print("Lowest Average: {}C".format(result["avg_low_temp"]))
        print("Average Humidity: {}".format(result["avg_humidity"]))

    @staticmethod
    def display_bars(result):
        for day, bars in result.items():
            print("{}\033[0;32;40m {}\033[0;31;40m{} \033[0;37;40m{}C - {}C \n".format(
                day, bars[0], bars[1], len(bars[0]), len(bars[1])))


class Operations:
    def find_extremes(self, files):
        result = {}
        file_manager = FileManager()
        for file in files:
            for row in file_manager.read(file, 'r'):
                max_temp_data = self.compare_values(row, "Max TemperatureC", result, "highest", ">")
                if max_temp_data:
                    result["highest"], result["highest_day"] = max_temp_data["max_val"], max_temp_data["day"]

                low_temp_data = self.compare_values(row, "Min TemperatureC", result, "lowest", "<")
                if low_temp_data:
                    result["lowest"], result["lowest_day"] = low_temp_data["min_val"], low_temp_data["day"]

                max_humidity_data = self.compare_values(row, "Max Humidity", result, "humid", ">")
                if max_humidity_data:
                    result["humid"], result["humid_day"] = max_humidity_data["max_val"], max_humidity_data["day"]
        return result

    @staticmethod
    def compare_values(row, row_key, result, result_key, operation):
        if operation == ">":
            if (result_key not in result and row[row_key]) \
                    or (row[row_key]
                        and int(row[row_key]) > result[result_key]):
                keys = list(row.keys())
                return {"max_val": int(row[row_key]), "day": row[keys[0]]}
        elif operation == "<":
            if (result_key not in result and row[row_key]) \
                    or (row[row_key]
                        and int(row[row_key]) < result[result_key]):
                keys = list(row.keys())
                return {"min_val": int(row[row_key]), "day": row[keys[0]]}

    @staticmethod
    def calculate_averages(file):
        result = {
            "avg_high_temp": 0,
            "avg_low_temp": 0,
            "avg_humidity": 0,
        }
        days_high_temp = 0
        days_low_temp = 0
        days_humidity = 0
        file_manager = FileManager()
        for row in file_manager.read(file, 'r'):
            if row["Max TemperatureC"]:
                result["avg_high_temp"] += int(row["Max TemperatureC"])
                days_high_temp += 1
            if row["Min TemperatureC"]:
                result["avg_low_temp"] += int(row["Min TemperatureC"])
                days_low_temp += 1
            if row[" Mean Humidity"]:
                result["avg_humidity"] += int(row[" Mean Humidity"])
                days_humidity += 1
        result["avg_high_temp"] = int(result["avg_high_temp"] / days_high_temp)
        result["avg_low_temp"] = int(result["avg_low_temp"] / days_low_temp)
        result["avg_humidity"] = int(result["avg_humidity"] / days_humidity)
        return result

    @staticmethod
    def generate_bars(file):
        result = {}
        file_manager = FileManager()
        for row in file_manager.read(file, 'r'):
            low_temp_str = ''
            high_temp_str = ''
            keys = list(row.keys())
            if row["Min TemperatureC"]:
                high_temp_str = "+" * int(row["Min TemperatureC"])
            if row["Max TemperatureC"]:
                low_temp_str = "+" * int(row["Min TemperatureC"])
            result[row[keys[0]]] = [low_temp_str, high_temp_str]
        return result


def parse_arguments():
    parser = argparse.ArgumentParser(description='Weatherman app')
    parser.add_argument('-e', "--extremes", action="store_true", help='find extreme conditions during e whole year')
    parser.add_argument('-a', "--averages", action="store_true", help='find average conditions during a month')
    parser.add_argument('-c', "--colours", action="store_true", help='print temperature bars during a month')
    parser.add_argument('time_span', type=str, help='time span on which the operation should be performed')
    parser.add_argument('indir', type=str, help='Input dir for data files')
    args = parser.parse_args()
    return args


def get_file_to_read(args, all_files):
    date_values = args.time_span.split("/")
    year, mon = date_values[0], date_values[1]
    file_to_read = ''
    for file_path in all_files:
        if year in file_path and calendar.month_abbr[int(mon)] in file_path:
            file_to_read = file_path
    return file_to_read


def main():
    ops = Operations()
    fmt = Formatter()
    args = parse_arguments()
    all_files = glob.glob(args.indir + "/*.txt")
    if args.extremes:
        files_to_read = []
        for file in all_files:
            if args.time_span in file:
                files_to_read.append(file)
        fmt.display_extremes(ops.find_extremes(files_to_read))
    elif args.averages:
        file_to_read = get_file_to_read(args, all_files)
        fmt.display_averages(ops.calculate_averages(file_to_read))
    elif args.colours:
        file_to_read = get_file_to_read(args, all_files)
        fmt.display_bars(ops.generate_bars(file_to_read))
    else:
        print("Operation unknown")


if __name__ == '__main__':
    main()

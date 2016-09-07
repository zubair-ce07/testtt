from datetime import datetime
import csv
import sys
'''
    WeatherData class is responsible for reading and parsing the files
    and sorting the data accordingly
'''


class WeatherData(object):
    __date_format = "%Y-%m-%d"

    def __init__(self, path, year, month=0):
        if path[0] == "\\":
            path = path[1:]
        if path[0] == "/":
            path = path[1:]
        self.path = path
        self.year = year
        self.month = month

    def __get_lowest(self, column_num):
        # Gives the lowest element of any column from the data file
        sorted_list = sorted([row for row in self.__get_rows() if row[column_num] != ''],
                             key=lambda row: int(row[column_num]), reverse=False)
        return sorted_list[0][0], sorted_list[0][column_num]

    def __get_highest(self, column_num):
        # Gives the highest element of any column from the data files
        sorted_list = sorted([row for row in self.__get_rows() if row[column_num] != ''],
                             key=lambda row: int(row[column_num]), reverse=True)
        return sorted_list[0][0], sorted_list[0][column_num]

    def __get_average(self, column_num):
        # Calculate the average of a column
        sum = 0
        count = 0
        for row in self.__get_rows():
            if row[column_num] != '':
                count += 1
                sum += int(row[column_num])
        if count == 0:
            return 0
        return sum/count

    def __get_rows(self):
        # Checks if the we have to apply operation on a single month file or all files of the given year
        # and returns the generator for the files to access rows
        if self.month:
            file_name = "/lahore_weather_" + str(self.year) + "_" + WeatherData.__get_month_name(self.month) + ".txt"
            try:
                csv_file = open(self.path+file_name, "r")
                reader = csv.reader(csv_file, delimiter=',')
                for row in WeatherData.__get_next_row(reader):
                    yield row
            except:
                raise
        else:
            file_not_found_count = 0
            for i in range(1,13):
                file_name = "/lahore_weather_" + str(self.year) + "_" + WeatherData.__get_month_name(i) + ".txt"
                try:
                    csv_file = open(self.path + file_name, "r")
                    reader = csv.reader(csv_file, delimiter=',')
                    for row in WeatherData.__get_next_row(reader):
                        yield row
                except:
                    file_not_found_count += 1
                    if file_not_found_count == 12:
                        raise

    @staticmethod
    def __get_month_name(month):
        # Gives the name of the given month number
        return WeatherData.__get_formatted_date("2000-" + str(month) + "-01").strftime("%b")

    @staticmethod
    def __get_next_row(reader):
        # Generator is modified so that we can ignore the first & last line of the data
        prev = None
        is_first = True
        for row in reader:
            if len(row) == 0:
                continue
            if prev:
                yield prev
            if is_first:
                is_first = False
                continue
            prev = row

    @staticmethod
    def __get_formatted_date(date_str=""):
        # Format the date and time
        format = "%Y-%m-%d"
        from datetime import datetime
        if not date_str:
            return datetime.today().date()
        return datetime.strptime(date_str, format).date()

    def task1(self):
        # Function to handle task1
        # Highest Temp is in column 1
        current = self.__get_highest(1)
        date_object = WeatherData.__get_formatted_date(current[0])
        print("Highest: ", str(current[1]) + "C", " on", date_object.strftime("%B"), " ", date_object.strftime("%d"))
        # Lowest temp is in column 3
        current = self.__get_lowest(3)
        date_object = WeatherData.__get_formatted_date(current[0])
        print("Lowest: ", str(current[1]) + "C", " on", date_object.strftime("%B"), " ", date_object.strftime("%d"))
        # Humidity is in column 7
        current = self.__get_highest(7)
        date_object = WeatherData.__get_formatted_date(current[0])
        print("Humid: ", str(current[1]) + "%", " on", date_object.strftime("%B"), " ", date_object.strftime("%d"))

    def task2(self):
        # Function to handle task2
        # Average temp is in column 2
        current = self.__get_highest(2)
        print("Highest Average: ", str(current[1]) + "C")
        current = self.__get_lowest(2)
        print("Lowest Average: ", str(current[1]) + "C")
        # Average Humidity is in column 8
        current = self.__get_average(8)
        print("Average Humidity: ", str(current) + "%")

    def task3(self):
        # Function to handle task 3
        date_object = self.__get_formatted_date(str(self.year)+"-" + str(self.month) + "-01")
        print(date_object.strftime("%B"),self.year)
        for row in self.__get_rows():
            date_object = self.__get_formatted_date(row[0])
            try:
                max = int(row[1])
                print(date_object.strftime("%d"), end="")
                for temp in range(0, max):
                    print("\033[91m+", end="")
                print("\033[0m", max, "C")
                min = int(row[3])
                print(date_object.strftime("%d"), end="")
                for temp in range(0, min):
                    print("\033[94m+", end="")
                print("\033[0m", str(min) + "C")
            except:
                pass

    def task4(self):
        # Function to handle task 4
        date_object = self.__get_formatted_date(str(self.year)+"-" + str(self.month) + "-01")
        print(date_object.strftime("%B"),self.year)
        for row in self.__get_rows():
            date_object = self.__get_formatted_date(row[0])
            try:
                max = int(row[1])
                min = int(row[3])
                print(date_object.strftime("%d"), end="")
                for temp in range(0, min):
                    print("\033[94m+", end="")
                for temp in range(1, max):
                    print("\033[91m+", end="")
                print("\033[0m", str(min) + "C-" + str(max) + "C")
            except:
                pass


def print_err(msg):
    print(msg+"\nWrong arguments!!\nweatherman.py -switch year/month /path/to/file")


def main():
    if len(sys.argv) == 4:
        try:
            if sys.argv[1] == "-e":
                weather_data = WeatherData(sys.argv[3],sys.argv[2])
                weather_data.task1()
            elif sys.argv[1] == "-a":
                temp = sys.argv[2].split("/")
                weather_data = WeatherData(sys.argv[3],temp[0], int(temp[1]))
                weather_data.task2()
            elif sys.argv[1] == "-c":
                temp = sys.argv[2].split("/")
                weather_data = WeatherData(sys.argv[3],temp[0], int(temp[1]))
                weather_data.task3()
            elif sys.argv[1] == "-b":
                temp = sys.argv[2].split("/")
                weather_data = WeatherData(sys.argv[3],temp[0], int(temp[1]))
                weather_data.task4()
        except FileNotFoundError:
            print_err("No Such File Exists!!")
        except:
            print_err("")
    else:
        print_err("")

if __name__ == "__main__":
    main()
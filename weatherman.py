import csv
import glob
from datetime import datetime




class WeatherReport:
    def __init__(self):
        print('')

    def chart_report_bonus(self, file_data):

        for file_rows in file_data:
            file_value = 0
            file_value2 = 0
            if file_rows["Max TemperatureC"] != "":
                to_convert = file_rows["Max TemperatureC"]
                file_value = int(to_convert)
                split_date = file_rows["PKT"].split("-")
                get_day = split_date[2]
                print(get_day, end="")
                for max_temp_count in range(file_value):
                    print("\033[1;31m+\033[1;m", end="")
            if file_rows["Min TemperatureC"] != "":
                to_convert = file_rows["Min TemperatureC"]
                file_value2 = int(to_convert)
                if file_value2 < 0:
                    for min_temp_count in range(abs(file_value2)):
                        print("\033[1;34m-\033[1;m", end="")
                    
                for min_temp_count in range(file_value2):
                    print("\033[1;34m+\033[1;m", end="")
            print(file_value, end="")
            print("C- ", end="")
            print(file_value2, end="")
            print("C")

    def monthly_report(self, file_data):
        high_temp = self.required_info_from_file(file_data, "Mean TemperatureC", True)
        print("Highest Average : {}C".format(high_temp["Mean TemperatureC"]))

        low_temp = self.required_info_from_file(file_data, "Mean TemperatureC", False)
        print("Lowest Average : {}C".format(low_temp["Mean TemperatureC"]))

        mean_humidity = self.required_info_from_file(file_data, " Mean Humidity", True)
        print("Average Mean Humidity : {}% ".format(mean_humidity[" Mean Humidity"]))

    def chart_report(self, file_data):
        self.file_data = file_data
        for file_row in file_data:
            if file_row["Max TemperatureC"] != "":
                to_convert = file_row["Max TemperatureC"]
                file_value = int(to_convert)
                split_date = file_row["PKT"].split("-")
                get_day = split_date[2]
                print(get_day, end="")
                for max_temp_count in range(file_value):
                    print("\033[1;31m+\033[1;m", end="")
                print(" ", file_value, "C")

            if file_row["Min TemperatureC"] != "":
                to_convert = file_row["Min TemperatureC"]
                file_value2 = int(to_convert)
                split_date = file_row["PKT"].split("-")
                get_day = split_date[2]
                print(get_day, end="")
                if file_value2 < 0:
                    for min_temp_count in range(abs(file_value2)):
                        print("\033[1;34m-\033[1;m", end="")
                    print(" {}C".format(file_value2))
                else:
                    for min_temp_count in range(file_value2):
                        print("\033[1;34m+\033[1;m", end="")
                    print(" {}C".format(file_value2))
        
    def yearly_report(self, file_data):

        high_temp = self.required_info_from_file(
            file_data, "Max TemperatureC", reverse_flag=True
        )
        temperature = high_temp["Max TemperatureC"]
        date_key = "PKT" if "PKT" in high_temp else "PKST"
        date_to_parse = high_temp.get(date_key)
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Highest: {}C on {} {}".format(temperature,date.strftime("%B"),date.day))
       
        low_temp = self.required_info_from_file(
            file_data, "Min TemperatureC", reverse_flag=False
        )
        temperature = low_temp["Min TemperatureC"]
        min_temp_key = "PKT" if "PKT" in high_temp else "PKST"
        date_to_parse = high_temp.get(min_temp_key)
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Lowest: {}C on {} {}".format(temperature,date.strftime("%B"),date.day))

        mean_humidity = self.required_info_from_file(
            file_data, " Mean Humidity", reverse_flag=True
        )
        temperature = mean_humidity[" Mean Humidity"]
        humidity_key = "PKT" if "PKT" in high_temp else "PKST"
        date_to_parse = high_temp.get(humidity_key)
        date = datetime.strptime(date_to_parse, "%Y-%m-%d")
        print("Humidity: {}% on {} {}".format(temperature,date.strftime("%B"),date.day))

    def required_info_from_file(self, file_data, col_name, reverse_flag):
        file_data = [file_rows for file_rows in file_data if file_rows[col_name] != ""]

        file_data.sort(key=lambda x: int(x[col_name]), reverse=reverse_flag)
        return file_data[0]

class FileData:
    def reading_file(self,file_names):
        files_data = []
        for file in file_names:
            with open(file, newline="") as csvfile:
                file_data = csv.DictReader(csvfile)
                for row in file_data:
                    files_data.append(row)
        return files_data


    def get_file_name(self,arguments, file_name, file_path):
        pattern = "*{}_{}*.txt"

        if arguments == "a" or arguments == "c":
            file_month = datetime.strptime(file_name, "%Y/%m").strftime("%b")
            pattern = pattern.format(file_name.split("/")[0], file_month)
        elif arguments == "e":
            pattern = pattern.format(file_name, "")

        return glob.glob(file_path + pattern)


        




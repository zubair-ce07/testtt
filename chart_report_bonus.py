import sys
from read_file import read_file
from data import data


class chart_report_bonus(data):
    def generate_chart_report_bonus(self, file_names):
        read_file.read_file(file_names,
                            self.day_record, self.weather_data)
        RED = "\033[1;31m"
        BLUE = "\033[1;34m"
        RESET = "\033[0;0m"
        if self.day_record is not None:
            for data in self.day_record:
                print(data["PKT"], end='')
                # min temp
                max_temp = data["Max TemperatureC"]
                min_tmep = data["Min TemperatureC"]
                sys.stdout.write(BLUE)
                if min_tmep != "":
                    for count in range(int(min_tmep)):
                        print("+", end="")
                    # max temp
                    max_temp = data["Max TemperatureC"]
                else:
                    sys.stdout.write(RESET)
                    print(" None")
                sys.stdout.write(RED)
                if max_temp != "":
                    for count in range(int(max_temp)):
                        print("+", end="")
                    sys.stdout.write(RESET)
                    print(" ", min_tmep, "C", end=" ")
                    print(" ", max_temp, "C")
                sys.stdout.write(RESET)
        else:
            print("NO data found")


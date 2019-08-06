import sys
from read_file import read_file
from data import data


class chart_report(data):

    def generate_chart_report(self, file_names):
        read_file.read_file(file_names,
                            self.day_record, self.weather_data)
        RED = "\033[1;31m"
        BLUE = "\033[1;34m"
        RESET = "\033[0;0m"
        if self.day_record is not None:
            for data in self.day_record:
                print(data["PKT"], end='')
                # max temp
                max_temp = data["Max TemperatureC"]
                sys.stdout.write(RED)
                if max_temp != "":
                    for count in range(int(max_temp)):
                        print("+", end="")
                    sys.stdout.write(RESET)
                    print(" ", max_temp, "C")
                else:
                    sys.stdout.write(RESET)
                    print(" None")
                sys.stdout.write(RESET)
                # min temp
                print(data["PKT"], end='')
                min_tmep = data["Min TemperatureC"]
                sys.stdout.write(BLUE)
                if min_tmep != "":
                    for count in range(int(min_tmep)):
                        print("+", end="")
                    sys.stdout.write(RESET)
                    print(" ", min_tmep, "C")
                else:
                    sys.stdout.write(RESET)
                    print(" None")
                sys.stdout.write(RESET)

        else:
            print("NO data found")


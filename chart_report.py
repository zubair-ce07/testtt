import sys
from read_file import ReadFile
from data import data


class ChartReport(data):

    def __init__(self):
        
        super(ChartReport, self).__init__()
        self.RED = "\033[1;31m"
        self.BLUE = "\033[1;34m"
        self.RESET = "\033[0;0m"
   
    def generate_chart_report(self, file_names,chart_option):

        ReadFile.read_file(file_names, self.day_record, self.weather_data)

        if self.day_record is None:
            return False

        self.print_chart() if chart_option == 0 else self.print_chart_bonus()


    def  print_chart(self):
        
        for data in self.day_record:
    
            print(data["PKT"], end='')

            max_temp = data["Max TemperatureC"]
            sys.stdout.write(self.RED)

            if max_temp != "":
                for count in range(int(max_temp)):
                    print("+", end="")
                sys.stdout.write(self.RESET)
                print(f" {max_temp} C")
            else:
                sys.stdout.write(self.RESET)
                print(" None")

            sys.stdout.write(self.RESET)

            print(data["PKT"], end='')
            min_tmep = data["Min TemperatureC"]
            sys.stdout.write(self.BLUE)

            if min_tmep != "":
                for count in range(int(min_tmep)):
                    print("+", end="")
                sys.stdout.write(self.RESET)
                print(f" {min_tmep} C")
            else:
                sys.stdout.write(self.RESET)
                print(" None")

            sys.stdout.write(self.RESET)

    def print_chart_bonus(self):
        
        for data in self.day_record:
    
            print(data["PKT"], end='')
 
            max_temp = data["Max TemperatureC"]
            min_tmep = data["Min TemperatureC"]
            sys.stdout.write(self.BLUE)

            if min_tmep != "":
                for count in range(int(min_tmep)):
                    print("+", end="")

                max_temp = data["Max TemperatureC"]
            else:
                sys.stdout.write(self.RESET)
                print(" None")
                
            sys.stdout.write(self.RED)

            if max_temp != "":
                for count in range(int(max_temp)):
                    print("+", end="")
                sys.stdout.write(self.RESET)
                print(f" {max_temp} C", end=" ")
                print(f" {min_tmep} C")

            sys.stdout.write(self.RESET)


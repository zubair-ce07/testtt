from yearly_temperature import YearlyTemperature
from average_temperature import AverageTemperatue
from temperature_in_chart import TemperatureInChart
import utilities

class WeatherMaster:
    def __init__(self, args):
        self.args=args


    def do_work(self):
        if self.args.yearly:
            yearly_temperature = YearlyTemperature()
            yearly_temperature.show_yearly_temperature(self.args.date_string,
                                                       self.args.file_path)

        elif self.args.monthly:
            if utilities.validate_date_str(self.args.date_string, 1) is False:
                print("Date should be of the form 'YYYY/MM'")
                exit(-1)
            average_temperature = AverageTemperatue()
            average_temperature.show_average_temperature(self.args.date_string,
                                                         self.args.file_path)
        elif self.args.monthly_chart or self.args.monthly_chart:
            if utilities.validate_date_str(self.args.date_string, 1) is False:
                print("Date should be of the form 'YYYY/MM'")
                exit(-1)
            temperature_in_chart = TemperatureInChart(self.args.monthly_chart,
                                                      self.args.monthly_chart)
            temperature_in_chart.display_temperature_in_chart(self.args.date_string,
                                                         self.args.file_path)
        else:
            print("Please re run the program and give one of the following input")
            print("'-e' for yearly report")
            print("'-a' for average monthly report")
            print("'-c for monthly report in bar chart in two lines'")
            print("'-b for monthly report in bar chart in one line'")

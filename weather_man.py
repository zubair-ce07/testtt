from __future__ import print_function
from report_generator_weather_man import ReportGenerator
from argument_handler_weather_man import ArgumentHandler
from file_detector_weather_man import FileDetector
from data_calculation_weather_man import DataCalculation

argument_obtainer = ArgumentHandler()
flag_set = argument_obtainer.mode
argument_obtainer.year_month_handler()
file_detector = FileDetector(argument_obtainer)
file_detector.detect_file()
data_calculator = DataCalculation(file_detector)


if flag_set == '-e':

    data_calculator.yearly_analysis()
    reporter = ReportGenerator(data_calculator)
    reporter.yearly_report()

elif flag_set == '-a':
    data_calculator.monthly_analysis()
    reporter = ReportGenerator(data_calculator)
    reporter.monthly_report()

elif flag_set == '-c':
    data_calculator.monthly_chart()

elif flag_set == '-b':
    data_calculator.monthly_bonus()

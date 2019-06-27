import sys
from input_handler import ArgumentExtractor
from file_locator import FileDetector
from data_calculator import CalculatingData
from report_generator import ReportGenerator

"""Importing the necessary modules from other files"""

date = str(sys.argv[3])
calc_mode = sys.argv[2]
"""Initializing the date and mode for first command"""

total_arguments = len(sys.argv)
loop_iterator = 1
multiple_counter = total_arguments - 2
"""loop_iterator provides a stop condition for loop to exit when
all arguments are attended for

multiple_counter provides a count for the controller so it can pass the
system arguments of multiple commands to other modules"""

while loop_iterator == 1:

    arguments = ArgumentExtractor
    arguments.initialization(arguments, date, calc_mode)
    file_handler = FileDetector(arguments)
    file_handler.locate_file()
    data = CalculatingData(file_handler)
    report = ReportGenerator(data)
    """All modules are initialized and an instance made"""

    if calc_mode == '-e':
        """Yearly analysis"""
        data.yearly_analysis()
        report.generate_yearly_report(data)

    elif calc_mode == '-b':
        """Monthly bonus analysis"""
        data.monthly_bonus()

    elif calc_mode == '-a':
        """Monthly average analysis"""
        data.monthly_analysis()
        report.generate_monthly_report(data)

    if total_arguments > 4:
        """This is the main module which makes sure all arguments are 
        attended for"""
        calc_mode = sys.argv[multiple_counter]
        date = str(sys.argv[multiple_counter+1])
        total_arguments -= 2
        multiple_counter -= 2
    else:
        loop_iterator = 0

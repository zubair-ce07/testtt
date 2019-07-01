import argparse
import sys
from data_calculator import CalculatingData
from input_handler import ArgumentExtractor
from input_handler import FileHandler
from report_generator import ReportGenerator

total_arguments = len(sys.argv)
loop_iterator = 1
multiple_counter = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='The file path of weather files')
    parser.add_argument('calc_mode', type=str,
                        help='Mode of selecting which action to perform')
    parser.add_argument('date', help='Date of the command to be executed')
    parser.add_argument('multiple_options', nargs='*',
                        help='Multiple arguments')
    args = parser.parse_args()
    date = args.date
    calc_mode = args.calc_mode

    while loop_iterator == 1:

        arguments = ArgumentExtractor()
        arguments.initialization(date, calc_mode)
        file_handler = FileHandler(arguments)
        file_handler.file_extraction(arguments)
        file_handler.locate_file(arguments)
        data = CalculatingData(file_handler)
        report = ReportGenerator(data)

        if calc_mode == 'e':
            data.yearly_analysis()
            report.generate_yearly_report(data)

        elif calc_mode == 'b':
            data.monthly_bonus()

        elif calc_mode == 'a':
            data.monthly_analysis()
            report.generate_monthly_report(data)

        if total_arguments > 4:
            calc_mode = args.multiple_options[multiple_counter]
            date = str(args.multiple_options[multiple_counter + 1])
            total_arguments -= 2
            multiple_counter += 2
        else:
            loop_iterator = 0

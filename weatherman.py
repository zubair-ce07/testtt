from config.parser import Parser
from core.calculator import Calculator
from core.report_generator import ReportGenerator
import sys


def main():
    try:
        parser = Parser(sys.argv[1])
        parser.read()
        # command and argument given to calculator
        Calculator(sys.argv[2:])
        # initializing report generator and print report
        # calculated by Calculator
        report_generator = ReportGenerator()
        report_generator.print_report()
    except IndexError as ie:
        print('Arguments have not passed or maybe {0}'.format(str(ie).upper()))


if __name__ == "__main__":
    main()

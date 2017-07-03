import argparse
from datetime import datetime


class ArgumentValidator:
    def __init__(self):
        pass

    @staticmethod
    def validate_arguments_year(arg_report):
        try:
            datetime.strptime(arg_report, '%Y')
            return arg_report
        except:
            raise argparse.ArgumentTypeError('Please enter the valid year e.g. 2009')

    @staticmethod
    def validate_arguments_month_year(arg_report):
        try:
            datetime.strptime(arg_report, '%Y/%m')
            return arg_report
        except:
            raise argparse.ArgumentTypeError('Please enter the valid year/month e.g. 2009/2')

    @staticmethod
    def check_number_arguments(args, parser):
        result = {key: value for key, value in vars(args).items() if value != None}

        if len(result) <= 1:
            parser.error('Please enter atleast one argument e.g -e [year]')

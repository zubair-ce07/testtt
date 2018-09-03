import argparse
from datetime import datetime


class ArgumentValidator:

    @staticmethod
    def validate_year(argument):
        try:
            datetime.strptime(argument, '%Y')
            return argument
        except:
            raise argparse.ArgumentTypeError(
                'Please enter the valid year e.g. 2006')

    @staticmethod
    def validate_month_year(argument):
        try:
            datetime.strptime(argument, '%Y/%m')
            return argument
        except:
            raise argparse.ArgumentTypeError(
                'Please enter the valid year/month e.g. 2006/7')

    @staticmethod
    def valid_number_of_arguments(args, parser):
        arg_list = {arg: arg_value for arg, arg_value in vars(args).items() if
                    arg_value != None}
        if len(arg_list) <= 1:
            parser.error('Please enter atleast two arguments')

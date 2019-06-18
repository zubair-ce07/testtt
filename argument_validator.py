import argparse
from datetime import datetime


class ArgumentValidator:

    @staticmethod
    def validate_year(arg_report):
        try:
            datetime.strptime(arg_report, '%Y')
        except AttributeError:
            raise argparse.ArgumentTypeError(
                'Please enter the valid year e.g. 2006')
        return arg_report

    @staticmethod
    def validate_month_year(arg_report):
        try:
            date = datetime.strptime(arg_report, '%Y/%m')
        except AttributeError:
            raise argparse.ArgumentTypeError(
                'Please enter the valid year/month e.g. 2006/7')
        return date

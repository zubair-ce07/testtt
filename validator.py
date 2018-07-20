import os
import argparse
import datetime


class Validator:
    def validate_path(path):
        if not os.path.exists(path):
            msg = 'Error :  Check your directory path.'
            raise argparse.ArgumentTypeError(msg)
        return path

    def validate_year(year_value):
        try:
            date = datetime.datetime.strptime(year_value, '%Y')
        except ValueError:
            msg = 'Error : Date is not valid'
            raise argparse.ArgumentTypeError(msg)

        return Validator.validate_current_date(date)

    def validate_current_date(date):
        if date.year > datetime.datetime.today().year:
            msg = 'Error : Date is not valid'
            raise argparse.ArgumentTypeError(msg)
        return date

    def validate_date(date_value):
        try:
            date = datetime.datetime.strptime(date_value, '%Y/%m')

        except ValueError:
            msg = 'Error : Date is not valid'
            raise argparse.ArgumentTypeError(msg)

        return Validator.validate_current_date(date)

    def validate_parameter(func):
        def validate(parameter):
            if not parameter:
                print("Error:: No result found for query")
                return
            func(parameter)

        return validate

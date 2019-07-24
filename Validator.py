import logging
import os


class Validator:
    @staticmethod
    def argument_validation(arg):
        if len(arg) < 4 or len(arg) % 2 != 0:
            logging.error(f"Invalid command format : {str(arg)}\n"
                          f"Proper format is /path [-e] year [-a] year/month [-c] year/month")
            return False
        if not os.path.exists(arg[1]):
            logging.error('File path does not exists')
            return False
        return True

    @staticmethod
    def year_validator(year, files_path):
        text_files = [f for f in os.listdir(files_path) if f.endswith('.txt')]
        text_files.sort()
        year_start = int(min(text_files, key=lambda x: int(x.split('_')[-2])).split('_')[-2])
        year_end = int(max(text_files, key=lambda x: int(x.split('_')[-2])).split('_')[-2])
        try:
            if int(year) not in range(year_start, year_end + 1):
                logging.error(f'Data for this year is not available, Year must between {year_start} - {year_end}')
                return False
        except ValueError:
            logging.ERROR('Invalid command format : Proper format is Year/Month')
            exit()
        return True

    @staticmethod
    def month_validation(month):
        try:
            if int(month) not in range(1, 13):
                logging.ERROR('Month must between 1 - 12')
                return False
        except ValueError:
            logging.ERROR('Invalid command format : Proper format is Year/Month')
            return False
        return True

import csv


class ReadCsv:
    """
    This class read the csv file and return result
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv_file(self):
        with open(self.file_path) as csvfile:
            read_csv = csv.DictReader(csvfile, delimiter=',')
            ret_value = list(read_csv)
            # print(type(ret_value))
        return ret_value
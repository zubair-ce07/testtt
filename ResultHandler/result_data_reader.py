import csv
from result_data import ResultData


class ResultDataReader:
    """
    This class reads data from the data.csv file and
    returns a list of ResultData objects
    """
    data_path = "data.csv"
    # defining constants to be used as score field,
    # if the student registered but not came in the test
    ABSENT = -300
    CANCELLED = -200

    def __init__(self, path):
        """
        Read the data from given path,
        populate ResultData objects
        and return a list of all objects
        """
        self.data_path = path

    def read_data(self):
        """
        Read the data from given path and
        store in a list of ResultData objects
        :return: list of ResultData objects
        """
        result_data = []
        with open(self.data_path, 'r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                result_item = ResultData()
                result_item.roll_no = row['roll_no']
                result_item.name = row['name']
                result_item.father_name = row['father_name']
                if row['score'] == "Absent":
                    result_item.score = self.ABSENT
                elif row['score'] == "CANCELLED":
                    result_item.score = self.CANCELLED
                else:
                    result_item.score = int(row['score'])
                result_data.append(result_item)
        return result_data

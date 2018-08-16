import csv
from result_data import ResultData


class ResultDataReader:
    """
    This class reads data from the data.csv file and
    returns a list of ResultData objects
    """
    data_path = "data.csv"

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
        required_columns = ["roll_no", "name", "father_name", "score"]
        result_data = []
        with open(self.data_path, 'r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                data_object = ResultData()
                for (k, v) in row.items():
                    if k in required_columns:
                        if k == "name":
                            data_object.name = v
                        elif k == "father_name":
                            data_object.father_name = v
                        elif k == "roll_no":
                            data_object.roll_no = v
                        elif k == "score":
                            if v == "Absent":
                                data_object.score = -300
                            elif v == "CANCELLED":
                                data_object.score = -200
                            else:
                                data_object.score = int(v)
                result_data.append(data_object)
        return result_data

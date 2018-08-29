import csv
from result_data import Student

# defining constants to be used as score field,
# if the student registered but not came in the test
default_path = "data.csv"
ABSENT = -300
CANCELLED = -200


def read_data(data_path=default_path):
    """
    Read the data from given path and
    store in a list of ResultData objects
    :param data_path: path to data file
    :return: list of ResultData objects
    """
    result_data = []
    with open(data_path, 'r') as infile:
        students = csv.DictReader(infile)
        for student in students:
            result_item = Student()
            result_item.roll_no = student['roll_no']
            result_item.name = student['name']
            result_item.father_name = student['father_name']
            if student['score'] == "Absent":
                result_item.score = ABSENT
            elif student['score'] == "CANCELLED":
                result_item.score = CANCELLED
            else:
                result_item.score = int(student['score'])
            result_data.append(result_item)
    return result_data

import csv
from result_data import Student


# defining constants to be used as score field,
# if the student registered but not came in the test
# for sorting the student list, absent students should
# be given any value less than zero
default_path = "data.csv"
ABSENT = -1
CANCELLED = -2


def read_data(data_path=default_path):
    """
    Read the data from given path and
    store in a list of ResultData objects
    :param data_path: path to data file
    :return: list of ResultData objects
    """
    result_data = []
    states = {'Absent': ABSENT, 'CANCELLED': CANCELLED}
    with open(data_path, 'r') as student_data_file:
        students = csv.DictReader(student_data_file)
        for student in students:

            score = student['score']
            score_val = score in list(states.keys()) and states.get(score) or int(score)

            result_item = Student(student['roll_no'],
                                  student['name'],
                                  student['father_name'],
                                  score_val)
            result_data.append(result_item)
    return result_data

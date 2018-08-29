import csv
from result_data import Student
from termcolor import colored


def show_percentage(per, threshold=None, scale=None):
    message = "Present Students "
    if threshold:
        message += "(Threshold " + colored(str(threshold), 'blue') + ") "
    if scale:
        message += "(Scale " + colored(str(scale), 'blue') + ") "
    message += ": "
    print(message
          + colored(str(format(per, '.2f')), 'green')
          + "%"
          )


def generate_merit_list_files(merit_lists):
    """
    It takes as input a list of lists and
    generates csv files of respective classes
    according to merit.
    :param merit_lists: dict of ResultData objects
    :return: None
    """
    fields = Student.get_fields()
    for file_name in merit_lists:
        with open(file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for student in merit_lists[file_name]:
                writer.writerow(
                    {fields[0]: student.roll_no,
                     fields[1]: student.name,
                     fields[2]: student.father_name,
                     fields[3]: student.score})
    print("Merit Files generated")

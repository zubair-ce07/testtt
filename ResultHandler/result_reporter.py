import csv
from termcolor import colored


def show_percentage(per, threshold=None, scale=None):
    message = "Present Students "
    if threshold:
        threshold_value = colored(str(threshold), 'blue')
        message += "(Threshold {}) ".format(threshold_value)
    if scale:
        scale_value = colored(str(scale), 'blue')
        message += "(Scale {}) ".format(scale_value)
    percentage_value = colored(str(format(per, '.2f')), 'green')
    message += ": {}%".format(percentage_value)
    print(message)


def generate_merit_list_files(merit_lists):
    """
    It takes as input a list of lists and
    generates csv files of respective classes
    according to merit.
    :param merit_lists: dict of ResultData objects
    :return: None
    """
    for file_name in merit_lists:
        with open(file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for student in merit_lists[file_name]:
                fields = list(vars(student).keys())
                writer.writerow(
                    {fields[0]: student.roll_no,
                     fields[1]: student.name,
                     fields[2]: student.father_name,
                     fields[3]: student.score})
    print("Merit Files generated")

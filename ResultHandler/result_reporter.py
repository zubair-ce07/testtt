import csv
from result_data import ResultData
from termcolor import colored


class ResultReporter:
    """
    This class performs all the output operations on the results
    """
    @staticmethod
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

    @staticmethod
    def generate_merit_list_files(groups):
        """
        It takes as input a list of lists and
        generates csv files of respective classes
        according to merit.
        :param groups: List of Lists of ResultData objects
        :return: None
        """
        files = ["BSSEM_old.csv", "BSSEA_old.csv",
                 "BSCSM_old.csv", "BSCSA_old.csv",
                 "BSITM_old.csv", "BSITA_old.csv",
                 "BSSEM_new.csv", "BSSEA_new.csv",
                 "BSCSM_new.csv", "BSCSA_new.csv",
                 "BSITM_new.csv", "BSITA_new.csv",
                 ]
        fields = ResultData.get_fields()

        for index, group in enumerate(groups):
            with open(files[index], 'w') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for student in group:
                    writer.writerow(
                        {fields[0]: student.roll_no,
                         fields[1]: student.name,
                         fields[2]: student.father_name,
                         fields[3]: student.score})
        print("Merit Files generated")

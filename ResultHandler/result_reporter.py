import csv


class ResultReporter:
    """
    This class performs all the output operations on the results
    """
    @staticmethod
    def show_present_percentage(per):
        """
        It shows the percentage of students who attempted the exam.
        :param per: percentage of present students
        :return: None
        """
        print(
            "Present Students: "
            + str(format(per, '.2f'))
            + "%"
        )

    @staticmethod
    def show_passed_percentage(per, threshold):
        """
        It shows the percentage of students who attempted the exam
        and scored more than given threshold.
        :param per: percentage of present students
        :param threshold: passing criteria
        :return: None
        """
        print(
            "Passed Students (with Threshold: "
            + str(threshold)
            + "): "
            + str(format(per, '.2f'))
            + "%"
        )

    @staticmethod
    def show_scaled_percentage(per, threshold, scale):
        """
        It shows the percentage of students who attempted the exam
        and scored more than given threshold after scaling the score.
        :param per: percentage of students who passed
        :param threshold: passing criteria
        :param scale: scaling value
        :return: None
        """
        print(
            "Passed Students (with Threshold: "
            + str(threshold)
            + " Scale: "
            + str(scale)
            + "): "
            + str(format(per, '.2f'))
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
        fields = ['roll_no', 'name', 'father_name', 'score']

        for index, group in enumerate(groups):
            with open(files[index], 'w') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for student in group:
                    writer.writerow(
                        {'roll_no': student.roll_no,
                         'name': student.name,
                         'father_name': student.father_name,
                         'score': student.score})
        print("Merit Files generated")

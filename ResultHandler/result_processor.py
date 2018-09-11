
def percentage(part, total):
    """
    helper function to find percentage of two values
    :param part: value whose percentage is required
    :param total: total value
    :return: percentage ratio
    """
    return part/total * 100


def get_percentage(students, threshold=0, scale=0):
    """
    :param students: list of ResultData objects i.e. student records
    :param threshold: the passing criteria for students
    :param scale: scale ratio for result
    :return:percentage of students present in the test
    """
    passed_students = [student for student in students
                       if student.score + scale > threshold]
    return percentage(len(passed_students), len(students))


def create_merit_list(students, threshold):
    """
    :param students: list of ResultData objects i.e. student records
    :param threshold: passing criteria
    :return:list of sub-lists where each sublist contains
    passed students sorted by the score.
    """
    passed_students = [student for student in students
                       if student.score >= threshold]
    sorted_list = sorted(passed_students,
                         key=lambda student: student.score,
                         reverse=True)
    groups = [sorted_list[score:score + 50] for score in range(0, 600, 50)]
    files = ["BSSEM_old.csv", "BSSEA_old.csv",
             "BSCSM_old.csv", "BSCSA_old.csv",
             "BSITM_old.csv", "BSITA_old.csv",
             "BSSEM_new.csv", "BSSEA_new.csv",
             "BSCSM_new.csv", "BSCSA_new.csv",
             "BSITM_new.csv", "BSITA_new.csv",
             ]
    merit_lists = dict(zip(files, groups))
    return merit_lists

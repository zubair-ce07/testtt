

class ResultProcessor:
    """
    This class provides basic functions to process the data
    according to the required task
    """
    @staticmethod
    def get_present_percentage(users):
        """
        :param users: list of ResultData objects i.e. student records
        :return:percentage of students present in the test
        """
        present_students = [x for x in users if x.score > 0]
        return len(present_students)/len(users) * 100

    @staticmethod
    def get_passed_percentage(users, threshold):
        """
        :param users: list of ResultData objects i.e. student records
        :param threshold: passing criteria
        :return:percentage of students passed by given threshold
        """
        passed_students = [x for x in users if x.score >= threshold]
        return len(passed_students)/len(users) * 100

    @staticmethod
    def get_scaled_percentage(users, threshold, scale):
        """
        :param users: list of ResultData objects i.e. student records
        :param threshold: passing criteria
        :param scale: scale ratio for result
        :return: percentage of students passed by given threshold
        after scaling
        """
        passed_students = [x for x in users if x.score + scale >= threshold]
        return len(passed_students)/len(users) * 100

    @staticmethod
    def make_merit_list(users, threshold):
        """
        :param users: list of ResultData objects i.e. student records
        :param threshold: passing criteria
        :return:list of sub-lists where each sublist contains
        passed students sorted by the score.
        """
        passed_students = [x for x in users if x.score >= threshold]
        sorted_list = sorted(passed_students, key=lambda x: x.score, reverse=True)
        groups = [sorted_list[x:x + 50] for x in range(0, 600, 50)]
        return groups



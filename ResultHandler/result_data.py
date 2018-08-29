

class Student:
    roll_no = None
    name = None
    father_name = None
    score = None

    @staticmethod
    def get_fields():
        """
        creates and returns a list of the object fields
        :return: list containing all fields of object
        """
        return [
            'roll_no',
            'name',
            'father_name',
            'score']



class ResultData:
    roll_no = None
    name = None
    father_name = None
    score = None

    def to_string(self):
        """
        creates and returns a comma separated
        representation of the object fields
        :return: string containing all fields of object
        """
        data = str(self.roll_no)\
               + ", " + str(self.name)\
               + ", " + str(self.father_name)\
               + ", " + str(self.score)
        return data


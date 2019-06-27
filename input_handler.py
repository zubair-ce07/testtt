import sys


class ArgumentExtractor:
    """This class is responsible for handling all the arguments provided at the
    command line"""
    total_arguments = len(sys.argv)

    def __init__(self):
        self.file_directory = ''
        self.date = 0
        self.year = 0
        self.month = 0
        self.mode = ''

    def initialization(self, date, mode):
        """This method checks and then saves the argument passed by  the
        main controller. Same module also handles multiple arguments"""

        if ArgumentExtractor.total_arguments < 4:
            print("The number of arguments provided is invalid. Exiting")
            sys.exit()
        else:
            self.file_directory = sys.argv[1]
            self.date = str(sys.argv[3])
            self.year = self.date[:4]
            self.month = self.date[5:]
            self.mode = sys.argv[2]

            if self.month is '':
                self.month = 0
            else:
                if int(self.month) < 1 or int(self.month) > 12:
                    print("The month provided is out of bound. Exiting")
                    sys.exit()

        if date == 0:
            sys.exit()
        else:
            self.year = date[:4]
            self.month = date[5:]
            self.mode = mode
            if self.month is '':
                self.month = 0

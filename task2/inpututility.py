class InputUtility:
    """ Utility to interact with user and handle input """
    @staticmethod
    def prompt_user():
        year = ''
        while year == '':
            year = input("Enter year : ")
        month = input("Enter month : ")
        return month, year

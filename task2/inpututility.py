class InputUtility:

    @staticmethod
    def prompt_user():
        year = ''
        while year == '':
            year = input("Enter year : ")
        month = input("Enter month : ")
        return (month, year)
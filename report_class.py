class ReportPrinting:
    def __init__(self, results, flag):
        self.results = results
        self.flag = flag

    def print(self):
        print('\n')
        if isinstance(self.results, str):
            print(self.results)
        else:
            if self.flag == '-e':
                print("Highest:", self.results.year[0])
                print("Lowest:", self.results.year[1])
                print("Humidity:", self.results.year[2])
            elif self.flag == '-a':
                print("Highest Average:", self.results.month[0])
                print("Lowest Average:", self.results.month[1])
                print("Average Mean Humidity:", self.results.month[2])
            else:
                for string in self.results.month:
                    print(string)

                print('\033[0m')

                for string in self.results.bonus:
                    print(string)

                print('\033[0m')




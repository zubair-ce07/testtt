import csv


class Table:

    def __init__(self, headings=None):
        self.rows = []
        self.headings = []
        self.set_headings(headings)

    def add_row(self, row):
        self.rows.append(row)

    def set_headings(self, headings):
        self.headings = headings

    def print_table(self):
        print(self.headings)
        for row in self.rows:
            print(row)


class Parser:
    file_name = ""

    def __init__(self, file_name):
        self.weather_reading = Table()
        self.file_name = file_name
        if(not(self.file_name.endswith(".txt"))):
            self.file_name = self.file_name + ".txt"
        self.set_weather_reading()

    def type_converstion(self, data):
        data_type = ['string', 'int', 'int', 'int', 'int', 'int', 'int',
                     'int', 'int', 'int', 'float', 'float', 'int', 'float',
                     'float', 'float', 'int', 'int', 'int', 'float',
                     'int', 'string', 'int']

        type_map = {'string': str, 'int': int, 'float': float}
        results = [type_map[t](d or 0) for t, d in zip(data_type, data)]
        return results

    def set_weather_reading(self):

        with open(self.file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                row = [elem.strip() for elem in row]
                if line_count == 0:
                    self.weather_reading.set_headings(row)
                    line_count += 1
                else:
                    self.weather_reading.add_row(self.type_converstion(row))
                    line_count += 1

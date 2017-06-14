from matrixreader import MatrixReader

class Controller(object):

    _column_indexes = [0, 1, 3, 7]
    _year = None
    _month = None
    _chart = None
    _single_chart = None

    def __init__(self, dir, yearly='', monthly='', chart=False, single_line=False):
        self._year = yearly
        self._month = monthly
        self._chart = chart
        self._single_chart = single_line
        self.martix = MatrixReader(dir, [].extend(yearly) + [].extend(monthly), self._column_indexes).retrieve()
        self.martix = self.filter_data()


    def calculate(self):
        if self._month == '':
            print(self.yearly())

    def filter_data(self):
        return [row for row in self.martix if '' not in row]


    def yearly(self):
        return max(self.martix, key=lambda item: int(item[1])), \
               min(self.martix, key=lambda item: int(item[2])), \
               max(self.martix, key=lambda item: int(item[3]))

    def monthly(self):
        pass


c = Controller('./weatherfiles', '2005')
c.calculate()
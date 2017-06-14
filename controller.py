from matrixreader import MatrixReader

class Controller(object):

    _column_indexes = [0, 1, 3, 7]
    _year = None
    _month = None
    _chart = None
    _single_chart = None

    def __init__(self, dir, yearly=[], monthly=[], chart=False, single_line=False):
        self._year = yearly
        self._month = monthly
        self._chart = chart
        self._single_chart = single_line
        self.martix = MatrixReader(dir, list(yearly) + list(monthly), self._column_indexes).retrieve()


    def calculate(self):
        pass

    def yearly(self):
        return max(result_set, key=lambda item: int(item[1])), min(result_set, key=lambda item: int(item[2])), \
               max(result_set, key=lambda item: int(item[3]))

    def monthly(self):
        pass
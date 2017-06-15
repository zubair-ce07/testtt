from matrixreader import MatrixReader
from printer import CPrinter

class Controller(object):

    _column_indexes = [0, 1, 3, 7]
    c_printer = CPrinter()

    def __init__(self, args):
        self.paras = args
        self.year = None
        self.month = None
        self.year_month = None
        self.bonus = None
        self.fixtures = []
        if args.c != '':
            self.fixtures.append(args.c)
            self.year_month = True
        if args.a != '':
            self.fixtures.append(args.a)
            self.month = True
        if args.e != '':
            self.fixtures.append(args.e)
            self.year = True
        if args.b != '':
            self.fixtures.append(args.b)
            self.bonus = True

        self.martix = MatrixReader(args.dir, self.fixtures, self._column_indexes).retrieve()
        self.martix = self.__filter_data()

    def calculate(self):
        if self.year:
            self.c_printer.yprint(self.__yearly())
        if self.month:
            self.c_printer.mprint(self.__monthly())
        if self.year_month:
            self.c_printer.cprint(self.__year_monthly())
        if self.bonus:
            self.c_printer.csprint(self.__year_monthly())

    def mean(self, l):
        return sum(map(int, l)) / len(l)


    def __filter_data(self):
        return [row for row in self.martix if '' not in row]


    def __yearly(self):
        return max(self.martix, key=lambda item: int(item[1])), \
               min(self.martix, key=lambda item: int(item[2])), \
               max(self.martix, key=lambda item: int(item[3]))

    def __monthly(self):
        records = []
        for record in self.martix:
            records.append(record[1:])
        return map(self.mean, zip(*records))

    def __year_monthly(self):
        if self.paras.c != '':
            year, month = self.paras.c.split('/')
        else:
            year, month = self.paras.b.split('/')
        records = [record for record in self.martix if year + '-' + month in record[0]]
        return records

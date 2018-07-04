class MonthData:
    """Data structure for storing data for a month weather conditions"""

    def __init__(self):
        self.days = []
        self.titles = []
        self.MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec')

    def load_month(self, directory='none', year='none', month='none'):
        """Loads a given months data in the data structure"""
        if year == 'none' or month == 'none' or directory == 'none':
            print('Cannot load without year.')
            return
        try:
            file_path = directory + '/Murree_weather_' + year + "_" + self.MONTHS[int(month)] + '.txt'
            file = open(file_path, 'r')
            title_line = file.readline()
            title_line = title_line.rstrip('\n')
            self.titles = title_line.split(',')
            for line in file:
                day = DayData()
                day.add_reading(line)
                self.days.append(day)
        except FileNotFoundError:
            print('No file found for current year')


class DayData:
    def __init__(self):
        self.readings = []

    def add_reading(self, data):
        data = data.rstrip('\n')
        self.readings = data.split(',')

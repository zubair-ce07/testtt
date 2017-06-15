

class WeatherFilesReader(object):

    retrieved_records = None

    def __init__(self, dir):
        self.dir = dir

    def read_by_year(self, year):
        if not any(key.startswith(year) for key in self.retrieved_records):
            pass

    def read_by_years(self, years):
        pass
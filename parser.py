from datetime import date
import re
import calendar

from weather import Weather

EOF_LINE = re.compile('<!--.*-->')


class WeatherParser:
    def __init__(self, directory_path, year, month):
        if not directory_path.endswith('/'):
            directory_path += '/'

        file_path = '{}lahore_weather_{}_{}.txt'.format(
            directory_path, year, calendar.month_abbr[month])

        self._file = open(file_path, 'r')
        self._file.readline()
        headers = self._file.readline().split(',')

        if len(headers) != 23:
            self.close()
            raise ValueError('invalid file format')

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.next()
        except EOFError:
            raise StopIteration

    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, '_file') and not self._file.closed:
            self._file.close()

    def next(self):
        if self._file.closed:
            raise EOFError('reached at end of file')

        data = self._file.readline()

        if EOF_LINE.match(data):
            self.close()
            raise EOFError('reached at end of file')

        fields = data.split(',')

        date_parameters = fields[0].split('-')
        weather_date = date(int(date_parameters[0]), int(
            date_parameters[1]), int(date_parameters[2]))

        try:
            return Weather(weather_date, int(fields[3]), int(fields[1]),
                           int(fields[2]), int(fields[9]), int(fields[7]),
                           int(fields[8]))
        except ValueError:
            return None

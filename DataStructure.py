from Parser import parse_reading as psr


class Year:
    def __init__(self):
        self.__year = {
            'Jan': None,
            'Feb': None,
            'Mar': None,
            'Apr': None,
            'May': None,
            'Jun': None,
            'Jul': None,
            'Aug': None,
            'Sep': None,
            'Oct': None,
            'Nov': None,
            'Dec': None,
        }

    def __getitem__(self, index):
        return self.__year[index]

    def __setitem__(self, index, value):
        self.__year[index] = value

    def items(self):
        return self.__year.items()


class Month:
    def __init__(self, data):
        self.__month = {
            'PKT': [],
            'Max TemperatureC': [],
            'Mean TemperatureC': [],
            'Min TemperatureC': [],
            'Dew PointC': [],
            'MeanDew PointC': [],
            'Min DewpointC': [],
            'Max Humidity': [],
            'Mean Humidity': [],
            'Min Humidity': [],
            'Max Sea Level PressurehPa': [],
            'Mean Sea Level PressurehPa': [],
            'Min Sea Level PressurehPa': [],
            'Max VisibilityKm': [],
            'Mean VisibilityKm': [],
            'Min VisibilitykM': [],
            'Max Wind SpeedKm/h': [],
            'Mean Wind SpeedKm/h': [],
            'Max Gust SpeedKm/h': [],
            'Precipitationmm': [],
            'CloudCover': [],
            'Events': [],
            'WindDirDegrees': []
        }
        for line in data:
            values = str.split(line, ',')
            i = 0
            for k, v in self.__month.items():
                self.__month[k].append(psr(values[i]))
                i += 1

    def __getitem__(self, index):
        return self.__month[index]

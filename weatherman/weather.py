
class Weather:

    def __init__(self, day, month, year, max_temp,
                 min_temp, mean_temp, max_humidity, min_humidity,
                 mean_humidity):

        self.day = day
        self.month = month
        self.year = year
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.mean_temp = mean_temp
        self.max_humidity = max_humidity
        self.min_humidity = min_humidity
        self.mean_humidity = mean_humidity
        self.MONTH_NAMES_MAP = {
                    '1': 'January', '2': 'February', '3': 'March',
                    '4': 'April', '5': 'May', '6': 'June',
                    '7': 'July', '8': 'August', '9': 'September',
                    '10': 'October', '11': 'November', '12': 'December'
                    }

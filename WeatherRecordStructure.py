"""This Module contains DataStructure for each record from the files"""


class WeatherRecord:

    def __init__(
            self,
            date_pkt=None,
            max_temperature_c=None,
            mean_temperature_c=None,
            min_temperature_c=None,
            max_humidity=None,
            mean_humidity=None,
            min_humidity=None,

    ):
        self.date_pkt = date_pkt

        # Temperatures
        if max_temperature_c[0] == '':
            self.max_temperature_c = None
        else:
            self.max_temperature_c = int(max_temperature_c[0])

        if mean_temperature_c[0] == '':
            self.mean_temperature_c = None
        else:
            self.mean_temperature_c = int(mean_temperature_c[0])

        if min_temperature_c[0] == '':
            self.min_temperature_c = None
        else:
            self.min_temperature_c = int(min_temperature_c[0])

        # Humidity
        if max_humidity[0] == '':
            self.max_humidity = None
        else:
            self.max_humidity = float(max_humidity[0])

        if mean_humidity[0] == '':
            self.mean_humidity = None
        else:
            self.mean_humidity = float(mean_humidity[0])

        if min_humidity[0] == '':
            self.min_humidity = None
        else:
            self.min_humidity = float(min_humidity[0])



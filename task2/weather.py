class Weather:
    """ Weather Model - logical representation of weather file """
    def __init__(self):
        self.month = '',
        self.year = '',
        self.readings = []

    def add_reading(self, reading):
        a = reading.pkt.split('-')
        self.year, self.month = a[0], a[1]
        self.readings.append(reading)

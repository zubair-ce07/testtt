class WeatherAnalyzer:
    """Extracts aggregate information from WeatherReading objects"""

    def _filter(self, readings, key):
        "Filter readings by given attribute"
        return [r for r in readings if getattr(r, key) is not None]

    def get_average_of_attributes(self, readings, key):
        """Returns average of values for given key"""
        readings = self._filter(readings, key)
        total = sum((getattr(r, key) for r in readings))
        count = len(readings)
        return round(total/count) if count != 0 else 0

    def get_maximum_reading(self, readings, key):
        """Returns reading with maximum value for key"""
        readings = self._filter(readings, key)
        return max(readings, key=lambda r: getattr(r, key))

    def get_minimum_reading(self, readings, key):
        """Returns reading with minimum value for key"""
        readings = self._filter(readings, key)
        return min(readings, key=lambda r: getattr(r, key))

    def get_attribute_list(self, readings, key):
        """Returns a list of attributes ordered by date"""
        readings = sorted(readings, key=lambda w: w.date.day)
        return [getattr(r, key) for r in readings]

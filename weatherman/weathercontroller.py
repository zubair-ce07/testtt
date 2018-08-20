"""This module computes and finds the weather records having the optimum
weather entries.
"""
import logging


class WeatherController:
    """This class does the computations on weather entries and
    finds the results.
    """

    def __init__(self):
        pass

    def find_yearly_extremes(self, entries):
        """Find and return the maximum and minimum temperatures and
        maximum humidity in a year's entries.
        """
        try:
            valid_entries = [row for row in entries if row.min_temperature is not None]
            min_temp_entry = min(valid_entries, key=lambda x: x.min_temperature)
            valid_entries = [row for row in entries if row.max_temperature is not None]
            max_temp_entry = max(valid_entries, key=lambda x: x.max_temperature)
            valid_entries = [row for row in entries if row.max_humidity is not None]
            max_humidity_entry = max(valid_entries, key=lambda x: x.max_humidity)
            result = {
                "min_temp_date": min_temp_entry.pkt,
                "min_temp": min_temp_entry.min_temperature,
                "max_temp_date": max_temp_entry.pkt,
                "max_temp": max_temp_entry.max_temperature,
                "max_humidity_date": max_humidity_entry.pkt,
                "max_humidity": max_humidity_entry.max_humidity
            }
            return result
        except ValueError as err:
            logging.error("Error while finding extremes in the year entries"
                          "of a file.\nDetail : %s", str(err))
            return None

    def find_month_average(self, entries):
        """Find and return the average maximum and minimum temperatures and
        average humidity in a year's entries.
        """
        try:
            valid_entries = [row.min_temperature for row in entries
                             if row.min_temperature is not None]
            highest_temperature_average = sum(valid_entries) // len(valid_entries)

            valid_entries = [row.max_temperature for row in entries
                             if row.max_temperature is not None]
            lowest_temperature_average = sum(valid_entries) // len(valid_entries)

            valid_entries = [row.mean_humidity for row in entries
                             if row.mean_humidity is not None]
            mean_humidity_average = sum(valid_entries) // len(valid_entries)

            result = {
                "min_temp_average": lowest_temperature_average,
                "max_temp_average": highest_temperature_average,
                "humidity_average": mean_humidity_average
            }
            return result
        except ValueError as err:
            logging.error("Error while finding averages in the month entries"
                          "of a file.\nDetail : %s", str(err))

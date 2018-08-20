"""Model class for weather record ,
 stores the required attributes of each record
 """
from datetime import datetime
import logging


class WeatherReading:
    """WeatherReading stores the required values read from reach record."""

    @staticmethod
    def __convert_int(value):
        """Convert the string value to int if its a number,
         else return None
         """
        try:
            return int(value)
        except ValueError as err:
            if value == "":  # empty value in file
                return None
            else:
                logging.error("Invalid value read from file."
                              "value is supposed to be 'int' type "
                              "but found : %s\nDetail : %s", value, str(err))

    @staticmethod
    def __convert_to_date(date_str):
        """Convert the string value to int if its a number,
         else return None
         """
        try:
            date_value = datetime.strptime(date_str, "%Y-%m-%d").date()
            return date_value
        except ValueError as err:
            logging.error("Invalid Date format in the file : %s.\n %s",
                          date_str,
                          str(err))
            return None

    def __init__(self,
                 pkt=None,
                 min_temperature=None,
                 max_temperature=None,
                 min_humidity=None,
                 max_humidity=None,
                 mean_humidity=None):
        self.pkt = self.__convert_to_date(pkt)
        self.min_temperature = self.__convert_int(min_temperature)
        self.max_temperature = self.__convert_int(max_temperature)
        self.min_humidity = self.__convert_int(min_humidity)
        self.max_humidity = self.__convert_int(max_humidity)
        self.mean_humidity = self.__convert_int(mean_humidity)

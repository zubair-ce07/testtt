from datetime import date
from column_attribute_association import associations


class WeatherReading:
    """Structure to store weather readings data"""

    def __init__(self, **kwargs):
        """
           Dynamically creates class attributes from the passed dictionary
           Uses column types specified in associations file to to type cast values accordingly
        """

        attributes = {}

        for key in kwargs:
            attribute_name = associations[key]["attribute_name"]
            data_type = associations[key]["type"]

            value = kwargs[key]

            if data_type == "number":
                try:
                    value = int(value)
                except ValueError:
                    value = None
            elif data_type == "date":
                y, m, d = value.split('-')
                value = date(int(y), int(m), int(d))
            elif data_type == "string":
                pass

            attributes[attribute_name] = value

        self.__dict__.update(attributes)

from datetime import date


class WeatherReading:
    """Structure to store weather readings data"""

    def __init__(self, **kwargs):
        """
           Dynamically creates class attributes from the passed dictionary
           Uses column types specified in associations file to to type cast values accordingly
        """

        for key in kwargs.copy().keys():
            try:
                kwargs[key] = int(kwargs[key])
            except ValueError:
                pass

        y, m, d = kwargs["PKT"].split('-')
        kwargs["PKT"] = date(int(y), int(m), int(d))

        self.__dict__.update(kwargs)
    
    def __getitem__(self, key):
        return self.__dict__[key]

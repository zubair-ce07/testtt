class WeatherData:
    __data = {}
    __years_added = set()

    def __init__(self, entry):
        WeatherData.__add_weather_data(entry)

    @staticmethod
    def __add_weather_data(entry):
        # add year in master data structure and if already added do nothing
        if WeatherData.__data == {}:
            WeatherData.__data[entry] = {}
        elif entry not in WeatherData.__data.keys():
            WeatherData.__data[entry] = {}
        if entry not in WeatherData.__years_added:
            WeatherData.__years_added.add(entry)

    @staticmethod
    def get_data(key=None):
        if key is None:
            return WeatherData.__data
        else:
            if key in WeatherData.__data:
                return WeatherData.__data[key]
        return None

    @staticmethod
    def get_years():
        return list(WeatherData.__years_added)

    @staticmethod
    def add_array_to_key(arr, key, entry, weather_entity_data):
        # add data in month of year
        if key not in WeatherData.__data[entry].keys():
            arr[list(arr.keys())[0]] = weather_entity_data
            WeatherData.__data[entry] = dict(list(WeatherData.__data[entry].items()) + list(arr.items()))

    @staticmethod
    def print_specific_key(key):
        if key in WeatherData.__data:
            print(WeatherData.__data[key])

    @staticmethod
    def print_():
        print(WeatherData.__data)
        for k, v in sorted(WeatherData.__data.items()):
            print(k)
            for month_k, month_v in v.items():
                print("\t", end='')
                print(month_k, month_v)

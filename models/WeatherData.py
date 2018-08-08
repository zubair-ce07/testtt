class WeatherData:
    __data = {}

    def __init__(self, entry):
        WeatherData.__add_weather_data(entry)

    @staticmethod
    def __add_weather_data(entry):
        # add year in master data structure and if already added do nothing
        if WeatherData.__data == {}:
            WeatherData.__data[entry] = {}
        elif entry not in WeatherData.__data.keys():
            WeatherData.__data[entry] = {}

    @staticmethod
    def get_data():
        return WeatherData.__data

    @staticmethod
    def add_array_to_key(arr, key, entry, weather_entity_data):
        # add data in month of year
        if key not in WeatherData.__data[entry].keys():
            arr[list(arr.keys())[0]] = weather_entity_data
            WeatherData.__data[entry] = dict(list(WeatherData.__data[entry].items()) + list(arr.items()))

    @staticmethod
    def print_():
        print(WeatherData.__data)
        for k, v in sorted(WeatherData.__data.items()):
            print(k)
            for month_k, month_v in sorted(v.items()):
                print("\t", end='')
                print(month_k, month_v)

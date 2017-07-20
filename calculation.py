import collections


class Calculation:
    def __init__(self):
        self.__yearly_cal = collections.defaultdict(lambda: 0)
        self.__monthly_cal = collections.defaultdict(lambda: 0)
        self.__monthly_barchart_cal = collections.defaultdict(lambda: 0)

    def yearly_calculation(self, data_set):
        str_max_temp = data_set["Max TemperatureC"]
        str_min_temp = data_set["Min TemperatureC"]
        str_humidity = data_set["Max Humidity"]

        max_temp_list = []
        for x in str_max_temp:
            max_temp_list.append(float(x) if x else -100)
        min_temp_list = []
        for x in str_min_temp:
            min_temp_list.append(float(x)  if x else 10000)

        humidity_list = []
        for x in str_humidity:
            humidity_list.append(float(x) if x else -100)


        max_temp = max(max_temp_list)
        max_index = max_temp_list.index(max_temp)
        min_temp = min(min_temp_list)
        min_index = min_temp_list.index(min_temp)
        max_humidity = max(humidity_list)
        humid_index = humidity_list.index(max_humidity)

        self.__yearly_cal["max_temp"] = str(max_temp)
        self.__yearly_cal["max_temp_date"] = str(data_set["PKT"][max_index])

        self.__yearly_cal["min_temp"] = str(min_temp)
        self.__yearly_cal["min_temp_date"] = str(data_set["PKT"][min_index])

        self.__yearly_cal["max_humidity"] = str(max_humidity)
        self.__yearly_cal["max_humidity_date"] = str(data_set["PKT"][humid_index])
        return self.__yearly_cal

    def monthly_report_calculation(self, data_set):

        str_max_temp = data_set["Max TemperatureC"]
        str_min_temp = data_set["Min TemperatureC"]
        str_humidity = data_set[" Mean Humidity"]

        max_temp_list = [float(x) for x in str_max_temp if x]
        min_temp_list = [float(x) for x in str_min_temp if x]
        humidity_list = [float(x) for x in str_humidity if x]

        avg_max_temp = int(sum(max_temp_list) / len(max_temp_list))
        avg_min_temp = int(sum(min_temp_list) / len(min_temp_list))
        avg_mean_humidity = int(sum(humidity_list) / float(len(humidity_list)))

        self.__monthly_cal["age_max_temp"] = avg_max_temp
        self.__monthly_cal["age_min_temp"] = avg_min_temp
        self.__monthly_cal["age_mean_humidity"] = avg_mean_humidity
        return self.__monthly_cal

    def monthly_barchart_calculation(self, data_set):

        str_max_temp = data_set["Max TemperatureC"]
        str_min_temp = data_set["Min TemperatureC"]
        max_temp_list = []
        for x in str_max_temp:
            max_temp_list.append(int(x) if x else 0)
        min_temp_list = []
        for x in str_min_temp:
            min_temp_list.append(int(x) if x else 0)

        self.__monthly_barchart_cal["max_temp"] = max_temp_list
        self.__monthly_barchart_cal["min_temp"] = min_temp_list
        return self.__monthly_barchart_cal

import constants


class Calculateresult:
    """class takes list of of weather data, and type specifier
    and make calculation and provide result object"""
    def __init__(self, weatherlist, arg_type):
        self.arg_type = arg_type
        self.weatherlist = weatherlist
        self.resultdict = {}

    def calculate(self):
        if self.arg_type == constants.YEAR:
            self.year_calculation()
        elif self.arg_type == constants.MONTH:
            self.month_calculation()
        elif self.arg_type == constants.MONTHCHART:
            self.month_chart_calculation()

    def year_calculation(self):
        max_temp_list = []
        min_temp_list = []
        most_humidity_list = []
        for row in self.weatherlist:
            if row[constants.MAX_TEMPRATURE_C]:
                max_temp_list.append(row)
            if row[constants.MIN_TEMPERATURE_C]:
                min_temp_list.append(row)
            if row[constants.MAX_HUMIDITY]:
                most_humidity_list.append(row)
        if max_temp_list:
            max_temp_dict = max(max_temp_list, key=lambda d: int(d[constants.MAX_TEMPRATURE_C]))
            # print("max temp  ",max_temp_dict)
            self.resultdict['max_temp'] = max_temp_dict
        if min_temp_list:
            min_temp_dict = min(min_temp_list, key=lambda d: int(d[constants.MIN_TEMPERATURE_C]))
            # print("min temp  ", min_temp_dict)
            self.resultdict['min_temp'] = min_temp_dict
        if most_humidity_list:
            most_humidit_dict = max(most_humidity_list, key=lambda d: int(d[constants.MAX_HUMIDITY]))
            print(most_humidit_dict[constants.MAX_HUMIDITY])
            self.resultdict['most_humidity'] = most_humidit_dict

    def month_calculation(self):
        max_temp_list = []
        min_temp_list = []
        mean_humidity_list = []
        for row in self.weatherlist:
            if row[constants.MAX_TEMPRATURE_C]:
                max_temp_list.append(int(row[constants.MAX_TEMPRATURE_C]))
            if row[constants.MIN_TEMPERATURE_C]:
                min_temp_list.append(int(row[constants.MIN_TEMPERATURE_C]))
            if row[constants.MEAN_HUMIDITY]:
                mean_humidity_list.append(int(row[constants.MEAN_HUMIDITY]))
        if max_temp_list:
            avg_max_temp = int(sum(max_temp_list)/len(max_temp_list))
            self.resultdict['avg_max_temp'] = avg_max_temp
        if min_temp_list:
            avg_min_temp = int(sum(min_temp_list)/len(min_temp_list))
            self.resultdict['avg_min_temp'] = avg_min_temp
        if mean_humidity_list:
            avg_mean_humidity = int(sum(mean_humidity_list)/len(mean_humidity_list))
            self.resultdict['avg_mean_humidity'] = avg_mean_humidity
            print("month calculate")

    def month_chart_calculation(self):
        max_temp_list = []
        min_temp_list = []
        for row in self.weatherlist:
            if row[constants.MAX_TEMPRATURE_C]:
                max_temp_list.append(row)
            if row[constants.MIN_TEMPERATURE_C]:
                min_temp_list.append(row)
        if max_temp_list:
            self.resultdict["max_temp_list"] = max_temp_list
        if min_temp_list:
            self.resultdict["min_temp_list"] = min_temp_list
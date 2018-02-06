import constants


class CalculateResult:
    """class takes list of of weather data, and type specifier
    and make calculation and provide result object"""
    def __init__(self, weather_data_record, arg_type):
        self.arg_type = arg_type
        self.weather_data_record = weather_data_record
        self.result_record = {}

    # funtion to call calculation method according to argument specified
    def calculate(self):
        if self.arg_type == constants.YEAR:
            self.year_calculation()
        elif self.arg_type == constants.MONTH:
            self.month_calculation()
        elif self.arg_type == constants.MONTHCHART:
            self.month_chart_calculation()

    # funtion for year result calculation
    def year_calculation(self):
        max_temp_data = []
        min_temp_data = []
        most_humidity_data = []
        for row in self.weather_data_record:
            if row[constants.MAX_TEMPERATURE_C]:
                max_temp_data.append(row)
            if row[constants.MIN_TEMPERATURE_C]:
                min_temp_data.append(row)
            if row[constants.MAX_HUMIDITY]:
                most_humidity_data.append(row)
        if max_temp_data:
            max_temp_dict = max(max_temp_data, key=lambda d: int(d[constants.MAX_TEMPERATURE_C]))
            self.result_record['max_temp'] = max_temp_dict
        if min_temp_data:
            min_temp_dict = min(min_temp_data, key=lambda d: int(d[constants.MIN_TEMPERATURE_C]))
            self.result_record['min_temp'] = min_temp_dict
        if most_humidity_data:
            most_humidit_dict = max(most_humidity_data, key=lambda d: int(d[constants.MAX_HUMIDITY]))
            self.result_record['most_humidity'] = most_humidit_dict

    # funtion for month result calculation
    def month_calculation(self):
        max_temp_data = []
        min_temp_data = []
        mean_humidity_data = []
        for row in self.weather_data_record:
            if row[constants.MAX_TEMPERATURE_C]:
                max_temp_data.append(int(row[constants.MAX_TEMPERATURE_C]))
            if row[constants.MIN_TEMPERATURE_C]:
                min_temp_data.append(int(row[constants.MIN_TEMPERATURE_C]))
            if row[constants.MEAN_HUMIDITY]:
                mean_humidity_data.append(int(row[constants.MEAN_HUMIDITY]))
        if max_temp_data:
            avg_max_temp = int(sum(max_temp_data)/len(max_temp_data))
            self.result_record['avg_max_temp'] = avg_max_temp
        if min_temp_data:
            avg_min_temp = int(sum(min_temp_data)/len(min_temp_data))
            self.result_record['avg_min_temp'] = avg_min_temp
        if mean_humidity_data:
            avg_mean_humidity = int(sum(mean_humidity_data)/len(mean_humidity_data))
            self.result_record['avg_mean_humidity'] = avg_mean_humidity

    # funtion to result calculation for month chart
    def month_chart_calculation(self):
        max_temp_data = []
        min_temp_data = []
        for row in self.weather_data_record:
            if row[constants.MAX_TEMPERATURE_C]:
                max_temp_data.append(row)
            if row[constants.MIN_TEMPERATURE_C]:
                min_temp_data.append(row)
        if max_temp_data:
            self.result_record["max_temp_data"] = max_temp_data
        if min_temp_data:
            self.result_record["min_temp_data"] = min_temp_data

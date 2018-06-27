from AnnualReportGenerator import AnnualReportGenerator


class AnnualResultCalculator:

    def __init__(self):
        self.month_wise_max_list = []
        self.month_wise_min_list = []
        self.month_wise_humid = []
        self.year_wise_list = []

    def do_year_wise_calculation(self, weather_list, year):
        for weather in weather_list:
            if year in str(weather.pkt):
                self.year_wise_list.append(weather)

        if len(self.year_wise_list) > 0:
            AnnualReport = AnnualReportGenerator()
            AnnualReport.generate_yealy_report( self.calculate_max_temp_for_year(),
                                                self.calculate_min_temp_for_year(),
                                                self.calculate_most_humid_day_for_year())
        else:
            print("No data available against this input")

    def calculate_max_temp_for_year(self):
        for month in self.year_wise_list:
            month_max_temp_index = month['max_temperature_c'].idxmax()
            max_temp_date = [int(month.max_temperature_c[month_max_temp_index]), month.pkt[month_max_temp_index]]
            self.month_wise_max_list.append(max_temp_date)

        return max(self.month_wise_max_list[0:])

    def calculate_min_temp_for_year(self):
        for month in self.year_wise_list:
            month_min_temp = month['min_temperature_c'].idxmin()
            min_temp_date = [month.min_temperature_c[month_min_temp], month.pkt[month_min_temp]]
            self.month_wise_min_list.append(min_temp_date)

        return min(self.month_wise_min_list[0:])

    def calculate_most_humid_day_for_year(self):
        for month in self.year_wise_list:
            month_max_humid = month['max_humidity'].idxmax()
            max_humid_date = [month.max_humidity[month_max_humid], month.pkt[month_max_humid]]
            self.month_wise_humid.append(max_humid_date)

        return max(self.month_wise_humid[0:])

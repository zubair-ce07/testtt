class WeatherReport:
    """
    Weather Report Class
    This class will calculate all type of max/min of temperature/humidity
    This class will also print the reports
    """

    def __init__(self, data):
        self.data = data
        self.annual_data = {}

    def get_report_function(self, reporttype):
        report_functions = {
            1: self.get_yearly_weather_report,
            2: self.get_hotest_day_of_year
        }
        return report_functions.get(reporttype)

    def get_print_function(self, reporttype):
        report_functions = {
            1: self.print_annualy,
            2: self.print_hotest_day_of_year
        }
        return report_functions.get(reporttype)

    def calculate(self, reporttype):
        """This module will call the calculate function according reporttype"""
        available_data_of_years = set([elem.year for elem in self.data])

        get_report = self.get_report_function(reporttype)
        get_report(available_data_of_years)

        print_report = self.get_print_function(reporttype)
        print_report()

        return self.annual_data

    def get_yearly_weather_report(self, available_data_of_years):
        """This module will calculate annual max/min of temperature/humidity"""
        for year in available_data_of_years:
            max_annual_temperatures = set()
            min_annual_temperatues = set()
            max_annual_humidities = set()
            min_annual_humidities = set()
            for item in self.data:
                if item.year == year:
                    if self.data[item]['Max TemperatureC']:
                        max_annual_temperatures.add(
                            int(self.data[item]['Max TemperatureC'])
                        )
                    if self.data[item]['Min TemperatureC']:
                        min_annual_temperatues.add(
                            int(self.data[item]['Min TemperatureC'])
                        )
                    if self.data[item]['Max Humidity']:
                        max_annual_humidities.add(
                            int(self.data[item]['Max Humidity'])
                        )
                    if self.data[item]['Min Humidity']:
                        min_annual_humidities.add(
                            int(self.data[item]['Min Humidity'])
                        )

            yearly_calculated_data = {
                'Max TemperatureC': max(max_annual_temperatures),
                'Min TemperatureC': min(min_annual_temperatues),
                'Max Humidity': max(max_annual_humidities),
                'Min Humidity': min(min_annual_humidities)
            }
            self.annual_data[year] = yearly_calculated_data

    def get_hotest_day_of_year(self, available_data_of_years):
        """This module will calculate Hotest Day of each year"""
        for year in available_data_of_years:
            monthly_max_temperature = 0
            for item in self.data:
                if item.year == year:
                    if self.data[item]['Max TemperatureC']:
                        max_temp = int(self.data[item]['Max TemperatureC'])
                        if max_temp > monthly_max_temperature:
                            day = item.day
                            month = item.month
                            monthly_max_temperature = max_temp

            hotest_day_of_year = {
                'Max TemperatureC': monthly_max_temperature,
                'Day': day,
                'Month': month
            }

            self.annual_data[year] = hotest_day_of_year

    def print_annualy(self):
        """This Module will print annual report"""
        print("Year    MaxTemp    MinTemp    MaxHumidity    MinHumidity")
        print("--------------------------------------------------------")
        for year in self.annual_data:
            print(
                year, "    ", self.annual_data[year]["Max TemperatureC"],
                "       ",
                self.annual_data[year]["Min TemperatureC"],
                "       ",
                self.annual_data[year]["Max Humidity"],
                "            ",
                self.annual_data[year]["Min Humidity"]
            )

    def print_hotest_day_of_year(self):
        """This module will print hotest day of each year"""
        print("Year    Date             Temp")
        print("-----------------------------")
        for year in self.annual_data:
            print(year, "    ", self.annual_data[year]["Day"], "/",
                  self.annual_data[year]["Month"], "/",
                  year, "    ",
                  self.annual_data[year]["Max TemperatureC"])

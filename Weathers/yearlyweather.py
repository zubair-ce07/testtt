class YearlyWeather:

    def __init__(self, year):
        self.year = year
        self.monthly_weathers = list()

    def get_hottest_day_information(self):
        hottest_month = None
        for weather in self.monthly_weathers:

            if hottest_month is None:
                hottest_month = weather
            else:
                highest_temperature = hottest_month.get_highest_temperature()
                new_temperature = weather.get_highest_temperature()
                if highest_temperature < new_temperature:
                    hottest_month = weather

        return dict(temp=hottest_month.get_highest_temperature(),
                    month=hottest_month.get_month_name(),
                    day=hottest_month.get_hottest_day())

    def get_coolest_day_information(self):
        coolest_month = None
        for weather in self.monthly_weathers:

            if coolest_month is None:
                coolest_month = weather
            else:
                lowest_temperature = coolest_month.get_lowest_temperature()
                new_temperature = weather.get_lowest_temperature()
                if lowest_temperature > new_temperature:
                    CoolestMonth = weather

        return dict(temp=coolest_month.get_lowest_temperature(),
                    month=coolest_month.get_month_name(),
                    day=coolest_month.get_coolest_day())

    def get_most_humid_day_information(self):
        most_humid_month = None
        for weather in self.monthly_weathers:

            if most_humid_month is None:
                most_humid_month = weather
            else:
                highest_humidity = most_humid_month.get_max_humidity()
                new_humidity = weather.get_max_humidity()
                if highest_humidity < new_humidity:
                    most_humid_month = weather

        return dict(humidity=most_humid_month.get_max_humidity
                    (), month=most_humid_month.get_month_name(),
                    day=most_humid_month.get_most_humid_day())

    def get_month(self, index):
        return [weather for weather in self.monthly_weathers
                if weather.month == index]

    def is_complete(self):
        return len(self.monthly_weathers) == 12

class YearlyReport:

    def print(self, yearly_weather):
        template = "Highest: {max_temp}C on {max_month} {max_date}\n"
        template += "Lowest: {min_temp}C on {min_month} {min_date}\n"
        template += "Humidity: {humidity}% on {humid_month} {humid_date}\n"

        hottest_day_information = yearly_weather.get_hottest_day_information()
        coolest_day_information = yearly_weather.get_coolest_day_information()
        humid_day_information = yearly_weather.get_most_humid_day_information()
        report = template.format(
            max_temp=hottest_day_information["temp"],
            max_month=hottest_day_information["month"],
            max_date=hottest_day_information["day"],
            min_temp=coolest_day_information["temp"],
            min_month=coolest_day_information["month"],
            min_date=coolest_day_information["day"],
            humidity=humid_day_information["humidity"],
            humid_month=coolest_day_information["month"],
            humid_date=coolest_day_information["day"],
        )

        print(report)

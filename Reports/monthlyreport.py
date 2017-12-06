class MonthlyReport:

    def print(self, monthly_weather):
        report_template = "Highest Average: {max_temp:{prec}}C\n"
        report_template += "Lowest Average: {min_temp:{prec}}C\n"
        report_template += "Average Mean Humidity: {humidity:{prec}}%\n"

        max_average = monthly_weather.get_highest_average_temperature()
        min_average = monthly_weather.get_lowest_average_temperature()
        humidity = monthly_weather.get_average_mean_humidity()
        report = report_template.format(
            max_temp=max_average,
            min_temp=min_average,
            humidity=humidity,
            prec='.3'
        )
        print(report)

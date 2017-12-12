import datetime


class Presentation:
    @staticmethod
    def maximum_temperature(report):
        template = "Highest: {max_temp}C on {max_date}\n"
        template += "Lowest: {min_temp}C on {min_date}\n"
        template += "Humidity: {humidity}% on {hum_date}\n"
        maximum_temperature = report.maximum_temperature
        max_date = report.maximum_temperature_date
        minimum_temperature = report.minimum_temperature
        min_date = report.minimum_temperature_date
        maximum_humidity = report.maximum_humidity
        hum_date = report.maximum_humidity_date
        mydate_max = datetime.datetime.strptime(max_date, '%Y-%m-%d')
        mydate_min = datetime.datetime.strptime(min_date, '%Y-%m-%d')
        mydate_hum = datetime.datetime.strptime(hum_date, '%Y-%m-%d')
        final_report = template.format(
            max_temp=maximum_temperature,
            max_date=mydate_max.strftime('%B %d'),
            min_temp=minimum_temperature,
            min_date=mydate_min.strftime('%B %d'),
            humidity=maximum_humidity,
            hum_date=mydate_hum.strftime('%B %d'),
        )
        print(final_report)

    @staticmethod
    def average_report(report):
        template = "Highest Average: {max_temp:}C\n"
        template += "Lowest Average: {min_temp}C\n"
        template += "Average Mean Humidity: {humidity}%\n"
        final_report = template.format(
            max_temp=int(report.maximum_temperature_mean),
            min_temp=int(report.minimum_temperature_mean),
            humidity=int(report.average_humidity),
        )
        print(final_report)

    @staticmethod
    def barchart(report):
        red = '\033[31m'
        blue = '\033[34m'
        black = '\033[30m'
        for bar in report.barchart:
            day_num = str(bar.chart_date)
            day = day_num.split('-')
            day = day[2].zfill(2)
            print(day + " " + red + bar.bar_max + " " + black + str(bar.max_temp) + 'C')
            print(day + " " + blue + bar.bar_min + " " + black + str(bar.min_temp) + 'C')

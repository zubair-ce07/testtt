import calendar


class WeatherReportGenerator:
    def generate_yearly_report(self, yearly_result):
        print(f"Highest: {yearly_result[0].high_temperature}C on {calendar.month_name[yearly_result[0].date.month]} "
              f"{yearly_result[0].date.day}")
        print(f"Lowest: {yearly_result[1].low_temperature}C on {calendar.month_name[yearly_result[1].date.month]} "
              f"{yearly_result[1].date.day}")
        print(f"Humidity: {yearly_result[2].humidity}% on {calendar.month_name[yearly_result[2].date.month]} "
              f"{yearly_result[2].date.day}")


    def generate_monthly_avg_report(self, result_avgs):
        print(f"Highest Average: {result_avgs[0]}C")
        print(f"Lowest Average: {result_avgs[1]}C")
        print(f"Average Mean Humidity: {result_avgs[2]}%")

    def generate_monthly_temperatures_report(self, readings, bonus):
        for day in readings:
            if bonus and day.high_temperature and day.low_temperature:
                high_temperature = '\033[31m' + "+" * int(day.high_temperature) + '\033[30m'
                low_temperature = '\033[34m' + '+' * int(day.low_temperature) + '\033[30m'
                print(f"{day.date.day} {high_temperature}"f"{low_temperature}"
                      f"{day.high_temperature}C - {day.low_temperature}C ")
            else:
                if day.high_temperature and day.low_temperature:
                    high_temperature = '\033[31m' + "+" * int(day.high_temperature) + '\033[30m'
                    low_temperature = '\033[34m' + '+' * int(day.low_temperature) + '\033[30m'
                    print(f"{day.date.day} {high_temperature}{day.high_temperature}C")
                    print(f"{day.date.day} {low_temperature}{day.low_temperature}C")

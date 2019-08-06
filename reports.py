from termcolor import colored
from calculations import Calculations


class WeatherReports:
    def __init__(self, record, year, month=0):
        self.cal = Calculations()
        self.year = year
        self.month = month
        self.record = []

        if month == 0:
            for rows in record.files_data:
                if rows.date.year == self.year:
                    self.record.append(rows)
        else:
            for rows in record.files_data:
                if rows.date.year == self.year and rows.date.month == self.month:
                    self.record.append(rows)

    def monthly_report(self):
        max_temp, min_temp, mean_hum = self.cal.cal_monthly(self.record)
        print(f'\nHighest Average : {max_temp}C')
        print(f'Lowest Average  : {min_temp}C')
        print(f'Average Mean Humidity : {mean_hum}%')

    def monthly_report_chart(self):
        print('\n')
        for row in self.record:
            print(f'{row.date.day} {colored("+" * row.max_temp, "red")} {row.max_temp}C')
            print(f'{row.date.day} {colored("+" * row.min_temp, "blue")} {row.min_temp}C')

    def yearly_report(self):
        max_t, min_t, max_hum = self.cal.cal_yearly(self.record)
        print(f"\nHighest  : {max_t.max_temp}C on {max_t.date.strftime('%B %-d')}")
        print(f"Lowest   : {min_t.min_temp}C on {min_t.date.strftime('%B %-d')}")
        print(f"Humidity : {max_hum.max_humidity}% on {max_hum.date.strftime('%B %-d')}")

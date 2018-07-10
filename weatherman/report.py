class Colors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    END_COLOR = '\033[0m'


class Report():
    """class for creating the reports given the results data structure."""
    def __init__(self):
        self.color = Colors()

    def year_report(self, max_temp, min_temp, max_humidity):
        print("Highest: {}C on {} {}".format(max_temp['Value'], max_temp['Month'], max_temp['Day']))
        print("Lowest: {}C on {} {}".format(min_temp['Value'], min_temp['Month'], min_temp['Day']))
        print("Humidity: {}% on {} {}".format(max_humidity['Value'], max_humidity['Month'], max_humidity['Day']))

    def month_report(self, avg_highest_temp, avg_lowest_temp, avg_mean_humidity):
        print("Highest Average: {}C".format(avg_highest_temp))
        print("Lowest Average: {}C".format(avg_lowest_temp))
        print("Average Mean Humidity: {}%".format(avg_mean_humidity))

    def day_report(self, max_temp, min_temp):
        day = 1
        for max_, min_ in zip(max_temp, min_temp):
            if max_:  # Check if temperature was recorded for that day
                print(day, self.color.RED, "+" * int(max_), self.color.END_COLOR, end=" + ")
            if min_:
                print(self.color.BLUE, "+" * abs(int(min_)), self.color.END_COLOR, "{}C  {}C".format(max_, min_))
            day += 1

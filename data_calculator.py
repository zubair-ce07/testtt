import operator

from statistics import mean


class DataCalculator:

    def __init__(self):
        self.average_high_temp = 0
        self.average_min_temp = 0
        self.average_mean_humidity = 0
        self.yearly_highest_temp = 0
        self.yearly_highest_temp_date = 0
        self.yearly_lowest_temp = 0
        self.yearly_lowest_temp_date = 0
        self.yearly_most_humid_day = 0
        self.yearly_most_humid_value = 0

    def monthly_analysis(self, weather_files, date):
        total_max_temp = {}
        total_min_temp = {}
        total_avg_humidity = {}
        record_count = 1
        for entry in weather_files:
            if entry.date.year == date.year and \
                    entry.date.month == date.month:
                total_max_temp[record_count] = entry.maximum_temp
                total_min_temp[record_count] = entry.minimum_temp
                total_avg_humidity[record_count] = entry.average_humidity
                record_count += 1
        self.average_high_temp = mean(total_max_temp.values())
        self.average_min_temp = mean(total_min_temp.values())
        self.average_mean_humidity = mean(total_avg_humidity.values())

    def yearly_analysis(self, weatherfiles, date):
        highest_temp = {}
        lowest_temp = {}
        most_humid = {}
        for entry in weatherfiles:
            if entry.date.year == date.year:
                highest_temp.update({entry.date: entry.maximum_temp})
                lowest_temp.update({entry.date: entry.minimum_temp})
                most_humid.update({entry.date: entry.maximum_humidity})

        """Using itemgetter to extract date for max values from dictionary"""
        self.yearly_highest_temp_date = max(
            highest_temp.items(), key=operator.itemgetter(1))[0]
        self.yearly_lowest_temp_date = min(
            lowest_temp.items(), key=operator.itemgetter(1))[0]
        self.yearly_most_humid_day = max(
            most_humid.items(), key=operator.itemgetter(1))[0]
        self.yearly_highest_temp = max(highest_temp.values())
        self.yearly_lowest_temp = min(lowest_temp.values())
        self.yearly_most_humid_value = max(most_humid.values())

from statistics import mean


class DataCalculator:

    def monthly_analysis(self, weather_files, date):
        total_max_temp = []
        total_min_temp = []
        total_avg_humidity = []
        for entry in weather_files:
            if entry.date.year == date.year and \
                    entry.date.month == date.month:

                total_max_temp.append(entry.maximum_temp)
                total_min_temp.append(entry.minimum_temp)
                total_avg_humidity.append(entry.average_humidity)

        average_high_temp = mean(total_max_temp)
        average_min_temp = mean(total_min_temp)
        average_mean_humidity = mean(total_avg_humidity)

        return average_high_temp, average_min_temp, average_mean_humidity

    def yearly_analysis(self, weatherfiles, date):
        highest_temp = {}
        lowest_temp = {}
        most_humid = {}
        for entry in weatherfiles:
            if entry.date.year == date.year:
                highest_temp.update({entry.date: entry.maximum_temp})
                lowest_temp.update({entry.date: entry.minimum_temp})
                most_humid.update({entry.date: entry.maximum_humidity})

        maximum_temp = max(highest_temp, key=highest_temp.get)
        yearly_highest_temp_date = maximum_temp
        yearly_highest_temp = highest_temp[maximum_temp]

        minimum_temp = min(lowest_temp, key=lowest_temp.get)
        yearly_lowest_temp_date = minimum_temp
        yearly_lowest_temp = lowest_temp[minimum_temp]

        maximum_humidity = max(most_humid, key=most_humid.get)
        yearly_most_humid_day = maximum_humidity
        yearly_most_humid_value = most_humid[maximum_humidity]

        return yearly_highest_temp_date, yearly_highest_temp,\
               yearly_lowest_temp_date, yearly_lowest_temp,\
               yearly_most_humid_day, yearly_most_humid_value

import math
import statistics


class weather_calculator:
    def __init__(self, years, months):
        self.years = years
        self.months = months

    def total(self, list_):

        count = 0
        for element in list_:
            if element is not None:
                count += 1

        return count

    def max_(self, list_):

        m = -math.inf
        for element in list_:
            if element is not None and element > m:
                m = element
        return m

    def min_(self, list_):

        m = math.inf
        for element in list_:
            if element is not None and element < m:
                m = element
        return m

    def avg(self, list_):

        sum_ = 0
        count = 0
        for element in list_:
            if element is not None:
                sum_ += element
                count += 1
        return (sum_/count)

    def max_temp_stats(self, year, month, data):

        max_temps = data[year + '_' + month]['MaxTemperatureC']

        max_temp_month = self.max_(max_temps)
        avg_max_temp = self.avg(max_temps)
        max_temp_day = max_temps.index(max_temp_month) + 1
        max_temps = [
            -math.inf if mt is None else mt for mt in max_temps
            ]

        return (max_temp_month, avg_max_temp, max_temp_day, max_temps)

    def min_temp_stats(self, year, month, data):

        min_temps = data[year + '_' + month]['MinTemperatureC']

        min_temp_month = self.min_(min_temps)
        avg_min_temp = self.avg(min_temps)
        min_temp_day = min_temps.index(min_temp_month) + 1
        min_temps = [
            math.inf if mt is None else mt for mt in min_temps
            ]

        return (min_temp_month, avg_min_temp, min_temp_day, min_temps)

    def humidity_stats(self, year, month, data):

        max_humids = data[year + '_' + month]['MaxHumidity']

        max_humid_month = self.max_(max_humids)
        max_humid_day = max_humids.index(max_humid_month) + 1

        mean_humids = data[year + '_' + month]['MeanHumidity']
        avg_mean_humid = self.avg(mean_humids)

        return (max_humid_month, max_humid_day, avg_mean_humid)

    def weather_calculations(self, data):
        """This function will perform all the calculations
        on the weather data
        """

        all_years_data = []
        for year in self.years:
            yearly = [year]
            for month in self.months:
                if (year + '_' + month) in data.keys():

                    monthly = [month]

                    # Find max temperature stats
                    (max_temp_month, avg_max_temp,
                        max_temp_day, max_temps) = self.max_temp_stats(
                        year, month, data
                        )
                    monthly.extend(
                        [
                            max_temp_month, avg_max_temp,
                            max_temp_day, max_temps
                        ]
                        )

                    # Min temperature stats
                    (min_temp_month, avg_min_temp,
                        min_temp_day, min_temps) = self.min_temp_stats(
                        year, month, data
                        )
                    monthly.extend(
                        [
                            min_temp_month, avg_min_temp,
                            min_temp_day, min_temps
                        ]
                        )

                    # Humidity stats
                    (max_humid_month, max_humid_day,
                        avg_mean_humid) = self.humidity_stats(
                            year, month, data
                            )

                    monthly.extend(
                        [max_humid_month, max_humid_day, avg_mean_humid]
                        )
                    yearly.append(monthly)

            all_years_data.append(yearly)
        return all_years_data

    def max_temp_of_year(self, year_data):

        max_temp = -math.inf
        max_temp_day = -1
        for month in year_data[1:]:
            if month[1] > max_temp:

                max_temp = month[1]
                max_temp_day = month[0] + ' ' + str(month[3])

        return (max_temp, max_temp_day)

    def max_humidity_of_year(self, year_data):

        max_humid = -math.inf
        max_humid_day = -1
        for month in year_data[1:]:
            if month[9] > max_humid:
                max_humid = month[9]
                max_humid_day = month[0] + ' ' + str(month[10])

        return (max_humid, max_humid_day)

    def min_temp_of_year(self, year_data):

        min_temp = math.inf
        min_temp_day = -1
        for month in year_data[1:]:
            if month[5] < min_temp:
                min_temp = month[5]
                min_temp_day = month[0] + ' ' + str(month[7])

        return (min_temp, min_temp_day)

    def calculate_yearly(self, years_monthly_records):
        """This calculates yearly maximums and minimums."""

        yearly_record = {}

        for year in self.years:
            for year_rec in years_monthly_records:
                if year_rec[0] == year:

                    (max_temp, max_temp_day) = self.max_temp_of_year(year_rec)
                    (max_humid, max_humid_day) = self.max_humidity_of_year(
                        year_rec
                        )
                    (min_temp, min_temp_day) = self.min_temp_of_year(year_rec)

                    yearly_record[year] = {
                        "Highest: ": str(max_temp) + 'C ' + str(max_temp_day),
                        "Lowest: ": str(min_temp) + 'C ' + str(min_temp_day),
                        "Humidity: ": (str(max_humid)
                                       + "% " + str(max_humid_day))
                        }

        return yearly_record

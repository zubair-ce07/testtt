import calendar
import result_container


class WeatherSummary:
    """This class serves as the tool for making all the required
    calculations depending upon what command is provided by user"""
    date_key = "PKT"

    def __init__(self):
        self.result = result_container.ResultContainer(
            "NA", "NA", "NA", "NA",
            "NA", "NA", "NA"
        )

    def get_result_for_e(self, year, data):
        """The function calculates result for command -e"""
        for daily_data in data:
            # Loop through whole data and filter data for requested year
            if daily_data[WeatherSummary.date_key].year == year:
                # The conditions ensure the use of data when value is not 'NA'
                if (daily_data["Max TemperatureC"] != "NA"
                    and self.result.highest_temperature == "NA") \
                        or (daily_data["Max TemperatureC"] != "NA"
                            and daily_data["Max TemperatureC"]
                            > self.result.highest_temperature):
                    # If the above condition is true
                    self.result.highest_temperature \
                        = daily_data["Max TemperatureC"]

                    self.result.highest_temperature_day \
                        = str(calendar.month_name[
                                daily_data[WeatherSummary.date_key].month]) \
                        + " " + str(daily_data[WeatherSummary.date_key].day)

                if (daily_data["Min TemperatureC"] != "NA"
                    and self.result.lowest_temperature == "NA") \
                        or (daily_data["Min TemperatureC"] != "NA"
                            and daily_data["Min TemperatureC"]
                            < self.result.lowest_temperature):
                    # If the above condition is true
                    self.result.lowest_temperature \
                        = daily_data["Min TemperatureC"]

                    self.result.lowest_temperature_day \
                        = str(calendar.month_name[
                                daily_data[WeatherSummary.date_key].month])\
                        + " " + str(daily_data[WeatherSummary.date_key].day)

                if (daily_data["Max Humidity"] != "NA"
                    and self.result.highest_humidity == "NA") \
                        or (daily_data["Max Humidity"] != "NA"
                            and daily_data["Max Humidity"]
                            > self.result.highest_humidity):
                    # If the above condition is true
                    self.result.highest_humidity = daily_data["Max Humidity"]

                    self.result.most_humid_day = \
                        str(calendar.month_name[
                                daily_data[WeatherSummary.date_key].month]) \
                        + " " + str(daily_data[WeatherSummary.date_key].day)


        return self.result

    def get_result_for_a(self, year, month, data):
        """The function calculates results for command -a"""
        total_avg_humidity_entries = 0
        sum_avg_humidity_entries = 0

        for daily_data in data:
            # Loop through all the data and filter only for
            # the requested Month and Year
            if daily_data[WeatherSummary.date_key].year == year \
                    and daily_data[WeatherSummary.date_key].month == month:
                # The conditions make sure that data with 'NA'
                # values is not considered
                if (daily_data["Mean TemperatureC"] != "NA"
                    and self.result.highest_temperature == "NA") \
                        or (daily_data["Mean TemperatureC"] != "NA"
                            and daily_data["Mean TemperatureC"]
                            > self.result.highest_temperature):
                    # If the above condition is true
                    self.result.highest_temperature \
                        = daily_data["Mean TemperatureC"]

                if (daily_data["Mean TemperatureC"] != "NA"
                    and self.result.lowest_temperature == "NA") \
                        or (daily_data["Mean TemperatureC"] != "NA"
                            and daily_data["Mean TemperatureC"]
                            < self.result.lowest_temperature):
                    # If the above condition is true
                    self.result.lowest_temperature \
                        = daily_data["Mean TemperatureC"]

                if daily_data["Mean Humidity"] != "NA":
                    # If the above condition is true
                    sum_avg_humidity_entries = sum_avg_humidity_entries \
                                               + daily_data["Mean Humidity"]
                    total_avg_humidity_entries += 1

        # The condition checks for the case where all the entries were 'NA'
        if total_avg_humidity_entries > 0:
            # If the above condition is true
            self.result.highest_humidity = \
                int(sum_avg_humidity_entries/total_avg_humidity_entries)

        else:
            self.result.highest_humidity = "NA"
        return self.result

    def get_result_for_c(self, year, month, data):
        """The function calculates the result for command -c"""
        for daily_data in data:
            # Loop through all the data and filter only for
            # the requested Month and Year
            if daily_data[WeatherSummary.date_key].year == year \
                    and daily_data[WeatherSummary.date_key].month == month:
                # If the above condition is true
                self.result.temperature_list.\
                    append((daily_data["Max TemperatureC"],
                            daily_data["Min TemperatureC"]))

        return self.result

import calendar
import result_container


class Calculator:
    """This class serves as the tool for making all the required
    calculations depending upon what command is provided by user"""
    date_key = "PKT"

    def __init__(self):
        self.result = result_container.ResultContainer("NA", "NA", "NA",
                                                       "NA", "NA", "NA", "NA")

    def compute(self, command, data):
        """This function gets the command and makes a call to respective
        function which calculates the results for the given command"""
        if command[0] == "-e":
            result = Calculator._get_result_for_e(self, int(command[1]), data)
        elif command[0] == "-a":
            year, month = command[1].split("/")
            result = Calculator._get_result_for_a(self, int(year), int(month), data)
        elif command[0] == "-c" or command[0] == "-cb":
            year, month = command[1].split("/")
            result = Calculator._get_result_for_c(self, int(year), int(month), data)

        # Storing the command type generating report specific to it.
        self.result.set_result_type(command[0])
        return self.result

    def _get_result_for_e(self, year, data):
        """The function calculates result for command -e"""
        for daily_data in data:
            # Loop through whole data and filter data for requested year
            if daily_data[Calculator.date_key].year == year:
                # The conditions ensure the use of data when value is not 'NA'
                if (daily_data["Max TemperatureC"] != "NA" and self.result.get_highest_temperature() == "NA") \
                        or (daily_data["Max TemperatureC"] != "NA"
                            and daily_data["Max TemperatureC"] > self.result.get_highest_temperature()):
                    self.result.set_highest_temperature(daily_data["Max TemperatureC"])
                    self.result.set_highest_temperature_day(str(calendar.month_name[daily_data[Calculator.date_key]
                                                                .month])+" "+str(daily_data[Calculator.date_key].day))

                if (daily_data["Min TemperatureC"] != "NA" and self.result.get_lowest_temperature() == "NA") \
                        or (daily_data["Min TemperatureC"] != "NA"
                            and daily_data["Min TemperatureC"] < self.result.get_lowest_temperature()):
                    self.result.set_lowest_temperature(daily_data["Min TemperatureC"])
                    self.result.set_lowest_temperature_day(str(calendar.month_name[daily_data[Calculator.date_key].
                                                               month])+" "+str(daily_data[Calculator.date_key].day))

                if (daily_data["Max Humidity"] != "NA" and self.result.get_highest_humidity() == "NA") \
                        or (daily_data["Max Humidity"] != "NA"
                            and daily_data["Max Humidity"] > self.result.get_highest_humidity()):
                    self.result.set_highest_humidity(daily_data["Max Humidity"])
                    self.result.set_most_humid_day(str(calendar.month_name[daily_data[Calculator.date_key].
                                                       month])+" "+str(daily_data[Calculator.date_key].day))

        return self.result

    def _get_result_for_a(self, year, month, data):
        """The function calculates results for command -a"""
        total_avg_humidity_entries = 0
        sum_avg_humidity_entries = 0

        for daily_data in data:
            # Loop through all the data and filter only for the requested Month and Year
            if daily_data[Calculator.date_key].year == year \
                    and daily_data[Calculator.date_key].month == month:
                # The conditions make sure that data with 'NA' values is not considered
                if (daily_data["Mean TemperatureC"] != "NA" and self.result.get_highest_temperature() == "NA") \
                        or (daily_data["Mean TemperatureC"] != "NA"
                            and daily_data["Mean TemperatureC"] > self.result.get_highest_temperature()):
                    self.result.set_highest_temperature(daily_data["Mean TemperatureC"])

                if (daily_data["Mean TemperatureC"] != "NA" and self.result.get_lowest_temperature() == "NA") \
                        or (daily_data["Mean TemperatureC"] != "NA"
                            and daily_data["Mean TemperatureC"] < self.result.get_lowest_temperature()):
                    self.result.set_lowest_temperature(daily_data["Mean TemperatureC"])

                if daily_data["Mean Humidity"] != "NA":
                    sum_avg_humidity_entries = sum_avg_humidity_entries + daily_data["Mean Humidity"]
                    total_avg_humidity_entries += 1

        # The condition checks for the case where all the entries were 'NA'
        if total_avg_humidity_entries > 0:
            self.result.set_highest_humidity(int(sum_avg_humidity_entries/total_avg_humidity_entries))
        else:
            self.result.set_highest_humidity("NA")
        return self.result

    def _get_result_for_c(self, year, month, data):
        """The function calculates the result for command -c"""
        for daily_data in data:
            # Loop through all the data and filter only for the requested Month and Year
            if daily_data[Calculator.date_key].year == year \
                    and daily_data[Calculator.date_key].month == month:
                self.result.temperature_list.append((daily_data["Max TemperatureC"],
                                                     daily_data["Min TemperatureC"]))

        return self.result

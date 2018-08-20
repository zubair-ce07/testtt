"""This module is to generate and display reports in appropriate pattern."""
import logging
import constants


class ReportGenerator:
    """ReportGenerator class is responsible for display result reports"""

    def __init__(self):
        pass

    @staticmethod
    def __generate_marks(value):
        """Generate '+' marks for positive temperatures and
        '-' marks for negative temperatures.
        """
        if value < 0:
            return "-" * (-value)
        return "+" * value

    @staticmethod
    def __yearly_result_row_formatter(result, key, unit):
        """Return a appropriate report string for a year's
         optimum reading.
         """
        date_month = result["{}_date".format(key)].strftime("%B")
        date_day = result["{}_date".format(key)].day
        result_message = "{}{} on {} {}".format(result[key],
                                                unit,
                                                date_month,
                                                date_day)
        return result_message

    def display_yearly_result(self, result):
        """Display findings for a year's highest, lowest temperatures and
        Humidity.
        """
        if not result:
            logging.error("None value passed in display_yearly_result")
            return
        highest_temp_message = self.__yearly_result_row_formatter(result,
                                                                  "max_temp",
                                                                  "C")
        lowest_temp_message = self.__yearly_result_row_formatter(result,
                                                                 "min_temp",
                                                                 "C")
        highest_humidity_message = self.__yearly_result_row_formatter(result,
                                                                      "max_humidity",
                                                                      "%")
        print("Highest: {}".format(highest_temp_message))
        print("Lowest: {}".format(lowest_temp_message))
        print(("Humidity: {}".format(highest_humidity_message)))

    @staticmethod
    def __monthly_average_row_formatter(result, key, unit):
        """Return a appropriate report string for a month's
         average readings.
         """
        if result:
            return "{}{}".format(result[key], unit)
        else:
            return "No appropriate data found. Result cannot be generated"

    def display_monthly_average(self, result):
        """Display findings for a month's average lowest, highest temperatures and
        Humidity.
        """
        if not result:
            logging.error("None value passed in display_monthly_average")
            return
        lowest_average_message = self.__monthly_average_row_formatter(result,
                                                                      "min_temp_average",
                                                                      "C")
        highest_average_message = self.__monthly_average_row_formatter(result,
                                                                       "max_temp_average",
                                                                       "C")
        humidity_average_message = self.__monthly_average_row_formatter(result,
                                                                        "humidity_average",
                                                                        "%")

        print("Highest Average : {}".format(lowest_average_message))
        print("Lowest Average : {}".format(highest_average_message))
        print("Average Humidity : {}".format(humidity_average_message))

    def __one_line_chart(self, index, low_value, low_color,
                         high_value, high_color, unit):
        """Return a formatted string for a one line chart """
        if not (high_value or low_value):
            return "{} : Missing Data!".format(index)

        low_marks = self.__generate_marks(low_value)
        high_marks = self.__generate_marks(high_value)
        result_string = "{index:02d} : {low_color}{low_marks}{high_color}{high_marks}" \
                        "{color_reset}{color_reset} {low_value}{unit} " \
                        "- {high_value}{unit}".format(index=index,
                                                      low_color=low_color,
                                                      low_marks=low_marks,
                                                      high_color=high_color,
                                                      high_marks=high_marks,
                                                      color_reset=constants.COLOR_RESET,
                                                      low_value=low_value,
                                                      high_value=high_value,
                                                      unit=unit)
        return result_string

    def __two_line_chart(self, index, low_value, low_color, high_value, high_color, unit):
        """Return a formatted string for a one line chart """
        if not (high_value or low_value):
            return "{} : Missing Data!".format(index)

        low_marks = self.__generate_marks(low_value)
        high_marks = self.__generate_marks(high_value)
        result_1 = "{index:02d} : {low_color}{low_marks}" \
                   " {color_reset} {low_value}" \
                   "{unit}".format(index=index,
                                   low_color=low_color,
                                   low_marks=low_marks,
                                   color_reset=constants.COLOR_RESET,
                                   low_value=low_value,
                                   unit=unit)
        result_2 = "{index:02d} : {high_color}{high_marks}" \
                   "{color_reset} {high_value}" \
                   "{unit}".format(index=index,
                                   high_color=high_color,
                                   high_marks=high_marks,
                                   color_reset=constants.COLOR_RESET,
                                   high_value=high_value,
                                   unit=unit)
        result_string = "{}\n{}".format(result_1, result_2)

        return result_string

    def display_daily_temperature_chart(self, result, report_type):
        """Display row by row chart for daily minimum and maximum temperatures."""
        if not result:
            logging.error("None value passed in display_daily_temperature_chart")
            return
        if report_type == constants.ONE_LINE_CHART:
            get_chart = self.__one_line_chart
        else:
            get_chart = self.__two_line_chart
        for entry in result:
            if entry:
                day = entry.pkt.day
                chart = get_chart(day,
                                  entry.min_temperature,
                                  constants.COLOR_BLUE,
                                  entry.max_temperature,
                                  constants.COLOR_RED,
                                  "C")
                print(chart)

    def display_report(self, result, report_type):
        """A main method for deciding which methon to call on the base
        of given report_type"""
        if not result:
            logging.error("No Data could be found for the given date.")
        else:
            if report_type == constants.YEARLY_TEMPERATURE:
                self.display_yearly_result(result)
            elif report_type == constants.AVERAGE_TEMPERATURE:
                self.display_monthly_average(result)
            else:
                self.display_daily_temperature_chart(result, report_type)

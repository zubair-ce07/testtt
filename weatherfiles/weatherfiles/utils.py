"""
Utils Module.

This module has the get methods for max,
min temperatures and max humidity.
"""
class Utils:
    """Utils class."""

    def get_max_temperature(self):
        """
        To get maximum temperature for input files.

        This method returns the maximum of the maximum
        temperatures list.
        """
        maximum_temp = max(self)
        return maximum_temp

    def get_min_temperature(self):
        """
        To get minimum temperature for input files.

        This method returns the minimum of the minimum
        temperatures list.
        """
        minimum_temp = min(self)
        return minimum_temp

    def get_max_humidity(self):
        """
        To get maximum humity for input files.

        This method returns the maximum of the
        maximum humidity list.
        """
        maximum_humidity = max(self)
        return maximum_humidity

    @staticmethod
    def get_average(data_list):
        """
        To get average for temperature and humidity lists.

        This method returns the average
        values for the input list.
        """
        length = len(data_list)
        sum_of_values = 0
        for _ in range(len(data_list)):
            sum_of_values = sum_of_values + data_list[_]
        return str(sum_of_values // length)

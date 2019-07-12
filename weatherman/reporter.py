import math


class Reporter:

    months = [
        "Jan", "Feb", "Mar",
        "Apr", "May", "Jun",
        "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec",
    ]
    CRED = '\033[91m'
    CEND = '\033[0m'
    CBLUE = '\33[34m'

    def yearly_report(self, per_year_records, input_data):
        """This function will print max temperature, max humidity
        and minimum temperature in
        in the year details.
        """

        try:
            print("\nIn Year: ", input_data)
            print("Highest: " + per_year_records[input_data]['Highest: '])
            print("Lowest: " + per_year_records[input_data]['Lowest: '])
            print("Humidity: " + per_year_records[input_data]['Humidity: '])
        except KeyError:
            print("Invalid Input....")
        return

    def monthly_report(self, years_monthly_records, input_data):
        """This will report highest average temperature, lowest average
        temperature and average mean humidity.
        """

        input_data = input_data.split('/')
        month = self.months[int(input_data[1])-1]

        for year in years_monthly_records:
            if year[0] == input_data[0]:
                for month_ in year:
                    if month_[0] == month:

                        print("\nMonth to report: ", month)
                        print(
                            "Highest Average: "
                            + str(int(month_[2])) + "C")
                        print(
                            "Lowest Average: "
                            + str(int(month_[6])) + "C")
                        print(
                            "Average Mean Humidity: "
                            + str(int(month_[11])) + "%\n")
        return

    def monthly_bar_chart(self, years_monthly_records, input_data):
        """This will print the bar chart."""

        input_data = input_data.split('/')
        month = self.months[int(input_data[1])-1]

        for year in years_monthly_records:
            if year[0] == input_data[0]:
                for month_ in year:
                    if month_[0] == month:

                        highest_temps = month_[4]
                        lowest_temps = month_[8]
                        print("\nMonth to Plot: ", month, ' ', input_data[0])

                        for a, b in zip(
                                range(len(highest_temps)),
                                range(len(lowest_temps))):

                            if highest_temps[a] != -math.inf:

                                s = highest_temps[a] * "+"
                                print(
                                    str(a+1) + ' ' + self.CRED
                                    + s + self.CEND + " "
                                    + str(highest_temps[a]) + 'C')

                            if lowest_temps[b] != math.inf:

                                s = lowest_temps[b] * "+"
                                print(
                                    str(b+1) + ' ' + self.CBLUE + s + self.CEND
                                    + ' ' + str(lowest_temps[b]) + 'C')
                        break
        return

    def horizontal_barchart(self, years_monthly_records, input_data):
        """This will print horizontal bar chart."""

        input_data = input_data.split('/')
        month = self.months[int(input_data[1])-1]

        for year in years_monthly_records:
            if year[0] == input_data[0]:
                for month_ in year:
                    if month_[0] == month:

                        highest_temps = month_[4]
                        lowest_temps = month_[8]
                        print("Month to plot: ", month, ' ', input_data[0])

                        for a, b in zip(
                                range(len(highest_temps)),
                                range(len(lowest_temps))):

                            if ((highest_temps[a] != -math.inf)
                                    and (lowest_temps[b] != math.inf)):

                                s = highest_temps[a] * "+"
                                s2 = lowest_temps[b] * '+'
                                print(
                                    str(a+1) + ' ' + self.CBLUE
                                    + s2 + self.CEND + self.CRED + s
                                    + self.CEND + " " + str(lowest_temps[b])
                                    + 'C-' + str(highest_temps[a]) + 'C')
                        break
        return

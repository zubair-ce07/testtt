class MonthlyReportGenerator:


    def generate_monthly_report(self, avg_max_temp, avg_min_temp, avg_mean_humid_temp):

        print("\nFollowing is your required monthly report")
        print("Highest Average: " + str(avg_max_temp) + "C")
        print("Lowest Average: " + str(avg_min_temp) + "C")
        print("Average Mean Humid Temperature: " + str(avg_mean_humid_temp) + "C")

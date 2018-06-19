import datetime
import calendar


class AnnualReportGenerator:

    def generate_yealy_report(self, month_wise_max, month_wise_min, month_wise_humid):
        print("\nFollowing is your required Annual report")

        DateSplit = datetime.datetime.strptime(month_wise_max[1], "%Y-%m-%d")
        print("Highest: " + str(month_wise_max[0]) + str("C on ") + calendar.month_abbr[DateSplit.month] + " " + str(
            DateSplit.day))

        DateSplit = datetime.datetime.strptime(month_wise_min[1], "%Y-%m-%d")
        print("Lowest: " + str(month_wise_min[0]) + str("C on ") + calendar.month_abbr[DateSplit.month] + " " + str(
            DateSplit.day))

        DateSplit = datetime.datetime.strptime(month_wise_humid[1], "%Y-%m-%d")
        print("Lowest: " + str(month_wise_humid[0]) + str("% on ") + calendar.month_abbr[DateSplit.month] + " " + str(
            DateSplit.day))
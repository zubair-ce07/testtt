import datetime
import calendar


class AnnualReportGenerator:

    def generate_yealy_report(self, month_wise_max, month_wise_min, month_wise_humid):
        print("\nFollowing is your required Annual report")

        date_split = datetime.datetime.strptime(month_wise_max[1], "%Y-%m-%d")
        report = "Highest : {0} C on {1} {2}".format(month_wise_max[0],calendar.month_abbr[date_split.month], date_split.day )
        print(report)

        date_split = datetime.datetime.strptime(month_wise_min[1], "%Y-%m-%d")
        report = "Lowest : {0} C on {1} {2}".format(month_wise_min[0],calendar.month_abbr[date_split.month], date_split.day )
        print(report)

        date_split = datetime.datetime.strptime(month_wise_humid[1], "%Y-%m-%d")
        report = "Lowest : {0} C on {1} {2}".format(month_wise_humid[0],calendar.month_abbr[date_split.month], date_split.day )
        print(report)

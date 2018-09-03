""" Print all reports and graphs """
from model_classes import DayRecord
from constants import CRED, CBLUE, CEND


class PrintReports:
    """Generate month reports: graph or Avg Report"""
    def print_report(self, avg_report):
        """ print month or year report """
        if avg_report:
            print("")
            avg_report.display()
        else:
            print("\n<< Data is not available")

    def print_month_graph(self, month_list, month_str):
        """ print month graph """
        print("")
        print(month_str)
        for day_record in month_list:
            print((day_record.date).strftime('%d'), end=" ")
            if day_record.max_temperature:
                for _ in range(int(day_record.max_temperature)):
                    print(CRED+"+"+CEND, end="")
                print(" "+CRED+str(day_record.max_temperature)+"C"+CEND)

            print((day_record.date).strftime('%d'), end=" ")
            if day_record.min_temperature:
                for _ in range(int(day_record.min_temperature)):
                    print(CBLUE+"+"+CEND, end="")
                print(" "+CBLUE+str(day_record.min_temperature) + "C" + CEND)
        print("")

    def print_year_graph(self, year_dict, year):
        """ print year graph """
        print("\n", year)
        for key in year_dict:
            print(str(key).zfill(2), end=" ")
            if year_dict[key]:
                readings = list(year_dict[key])
                max_temperature = readings[0]
                min_temperature = readings[1]
                if max_temperature and min_temperature:
                    for _ in range(int(max_temperature)):
                        print(CRED + "*" + CEND, end="")
                    for _ in range(int(min_temperature)):
                        print(CBLUE + "*" + CEND, end="")
                    print(f" {max_temperature}C - {min_temperature}C")
                else:
                    print(" - ")
            else:
                print(" - ")
        print("")

import Weather as t
import argparse


def main():
    data = t.parse_file()
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help="""Year/Month to find weather's
                         calculations""")
    parser.add_argument("-e", "--yearly", help="""Display yearly weather
                         statistics""", action="store_true")
    parser.add_argument("-a", "--monthly", help="""Display yearly weather
                         statistics""", action="store_true")
    parser.add_argument("-c", "--graphically", help="""Plot the bar chart of
                         weather stats of a month""", action="store_true")
    args = parser.parse_args()
    date = args.date

    if args.yearly:
        year_data = t.year_reading(data, date)
        max_temp_data = year_data[0]
        min_temp_data = year_data[1]
        max_humidity_data = year_data[2]
        max_temp = max_temp_data["data"]
        max_temp_date = max_temp_data["date"]
        min_temp = min_temp_data["data"]
        min_temp_date = min_temp_data["date"]
        max_humidity = max_humidity_data["data"]
        max_humidity_date = max_humidity_data["date"]
        resultPrint = t.PrintResult()
        resultPrint.print_year_result(max_temp, max_temp_date, min_temp,
                                      min_temp_date, max_humidity,
                                      max_humidity_date)

    if args.monthly:
        month_data = t.month_reading(data, date)
        avg_max_temp = month_data[0]
        avg_min_temp = month_data[1]
        avg_mean_humidity = month_data[2]
        resultPrint = t.PrintResult()
        resultPrint.print_month_result(avg_max_temp, avg_min_temp,
                                       avg_mean_humidity)

    if args.graphically:
        t.month_graph(data, date)


if __name__ == '__main__':
    main()

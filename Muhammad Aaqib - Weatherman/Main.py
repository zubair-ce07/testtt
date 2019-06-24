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
        year_data = t.get_year_reading(data, date)
        max_temp_data = year_data.get("max temp")
        min_temp_data = year_data.get("min temp")
        max_humidity_data = year_data.get("max humidity")
        max_temp = max_temp_data.get("value")
        max_temp_date = max_temp_data.get("date")
        min_temp = min_temp_data.get("value")
        min_temp_date = min_temp_data["date"]
        max_humidity = max_humidity_data.get("value")
        max_humidity_date = max_humidity_data.get("date")
        result_print = t.ResultPrinter()
        result_print.print_year_result(max_temp, max_temp_date, min_temp,
                                       min_temp_date, max_humidity,
                                       max_humidity_date)

    if args.monthly:
        month_data = t.get_month_reading(data, date)
        avg_max_temp = month_data.get("avg max temp")
        avg_min_temp = month_data.get("avg min temp")
        avg_mean_humidity = month_data.get("avg mean humidity")
        result_print = t.ResultPrinter()
        result_print.print_month_result(avg_max_temp, avg_min_temp,
                                        avg_mean_humidity)

    if args.graphically:
        chart_data = t.get_month_graph(data, date)
        year_index = chart_data.get("year index")
        month_index = chart_data.get("month index")
        result_print = t.ResultPrinter()
        result_print.plot_month_barchart(data, year_index, month_index)


if __name__ == '__main__':
    main()

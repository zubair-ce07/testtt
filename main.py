import argparse

from calculation import Calculation
from extract_data import ExtractData
from report import Report


def main():
    datareader = ExtractData()
    calculator = Calculation()
    reporter = Report()
    DATA_READING_FUNCTION_MAP = {'yearlyreport': datareader.get_file_names_yearly,
                                 'monthlyreport': datareader.get_file_names_monthly,
                                 'monthlybarchart': datareader.get_file_names_monthly}

    CALCULATION_FUNCTION_MAP = {'yearlyreport': calculator.yearly_calculation,
                                'monthlyreport': calculator.monthly_report_calculation,
                                'monthlybarchart': calculator.monthly_barchart_calculation}

    REPORTING_FUNCTION_MAP = {'yearlyreport': reporter.yearly_report,
                              'monthlyreport': reporter.monthly_report,
                              'monthlybarchart': reporter.monthly_bar_chart}

    parser = argparse.ArgumentParser(
        description='Script retrieves Commands from User')

    parser.add_argument(
        '-f', '--filesdir', type=str, help='files directory', required=True)

    parser.add_argument('-c', '--command', choices=DATA_READING_FUNCTION_MAP.keys(), required=True)

    parser.add_argument(
        '-d', '--date', type=str, help='Summary of date', required=True)

    parser.add_argument('-exc1', '--command1', choices=DATA_READING_FUNCTION_MAP.keys(), required=False)

    parser.add_argument(
        '-exd1', '--date1', type=str, help='Summary of date', required=False)

    parser.add_argument('-exc2', '--command2', choices=DATA_READING_FUNCTION_MAP.keys(), required=False)

    parser.add_argument(
        '-exd2', '--date2', type=str, help='Summary of date', required=False)

    args = parser.parse_args()

    func = DATA_READING_FUNCTION_MAP[args.command]
    func(args.filesdir, args.date)

    data_set = datareader.read_data()

    func = CALCULATION_FUNCTION_MAP[args.command]
    result = func(data_set)

    func = REPORTING_FUNCTION_MAP[args.command]
    func(result)

    if args.command1:
        func = DATA_READING_FUNCTION_MAP[args.command1]
        func(args.filesdir, args.date1)

        data_set = datareader.read_data()

        func = CALCULATION_FUNCTION_MAP[args.command1]
        result = func(data_set)

        func = REPORTING_FUNCTION_MAP[args.command1]
        func(result)
    if args.command2:
        func = DATA_READING_FUNCTION_MAP[args.command2]
        func(args.filesdir, args.date2)

        data_set = datareader.read_data()

        func = CALCULATION_FUNCTION_MAP[args.command2]
        result = func(data_set)

        func = REPORTING_FUNCTION_MAP[args.command2]
        func(result)


if __name__ == "__main__":
    main()

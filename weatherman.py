from os.path import isdir
from datetime import datetime

import click

from report import Report

REQUIRED_DATE_FORMAT = "%Y-%m"


def validate_date(input_date):
    try:
        datetime.strptime(input_date, REQUIRED_DATE_FORMAT)
    except ValueError:
        return False

    return True


def get_month_and_year(input_date):
    """
        input_date format is %Y-%m
    """
    input_date_obj = datetime.strptime(input_date, REQUIRED_DATE_FORMAT)

    return str(input_date_obj.year), input_date_obj.strftime("%b")


@click.command()
@click.option(
    '-year',
    nargs=1,
    help="gets an year in format yyyy. Prints the stats for most humdity, "
    "lowest temparature, and "
    "highest temparture for the given year."


)
@click.option(
    '-month',
    nargs=1,
    help="provide date in format yyyy-mm. Prints the average stats for humdity, "
    "lowest temparature, and highest temparture for the given month of "
    "the year."
)
@click.option(
    '-chart',
    nargs=1,
    help="provide date in format yyyy-mm. Prints a horizontal bar chart of each"
    " day for lowest temparature, and highest temparture"
)
@click.argument('path_to_files')
@click.option(
    '-multiple',
    default="1",
    nargs=0,
    help="displays a single line horizontal bar chart. Use this tag with -c.\n"
    "specify -multiple for multiple line"
)
def main(year, month, chart, path_to_files, multiple):
    if not isdir(path_to_files):
        print("File path of data directory is invalid.")
        return

    if year:
        report = Report(path_to_files)
        report.yearly_report(year)
        return

    if month:
        validated = validate_date(month)
        if not validated:
            print("Provided date is invalid. use --help for more details.")
            return

        year, month = get_month_and_year(month)
        report = Report(path_to_files)
        report.monthly_report(year, month)
        return

    if chart:
        year, month = get_month_and_year(chart)
        report = Report(path_to_files)

        if not multiple:
            report.monthly_horizontal_chart(year, month, single_line=False)
        else:
            report.monthly_horizontal_chart(year, month, single_line=True)

        return


if __name__ == "__main__":
    main()

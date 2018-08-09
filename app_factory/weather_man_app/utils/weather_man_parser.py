# -*- coding: utf-8 -*-
"""
Parser for weathe man application
"""
from app_factory.parser.args_parser import BaseArgsParser

parser = BaseArgsParser(
    description="The program is design to generate Murree Weather Data reporting. (Use -h for help)"
)
parser.add_argument(
    "file_path",
    help="Path to the directory containing weather data.",
    type=str
)
parser.add_argument(
    "-e",
    "--year",
    help="Pass year as argument about which results are required. (Like: -e 2010)"
)
parser.add_argument(
    "-a",
    "--year_with_month",
    help="Pass year with month as argument about which results are required. (Like: -a 2010/1)"
)
parser.add_argument(
    "-c",
    "--month_bar_chart",
    help="input year and month for chart in format of year/month e.g 2014/8"
)

parser.add_argument(
    "-m",
    "--month_bar_chart_in_one_line",
    help="input year and month for chart in format of year/month e.g 2014/8"
)

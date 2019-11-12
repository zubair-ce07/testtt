"""
Main program file where execution will originate
"""
import os
from os.path import exists
import argparse
import re
import weather_data_report_generator
from weatherman_parser import Parse

# Parssing arguments
parser = argparse.ArgumentParser(description="""Generate weather
 report""")
parser.add_argument("path", type=str, help="""to get the path of
 weather directory""")
parser.add_argument("-e", "--e", help="""Flag to generate
yearly report""", type=str)
parser.add_argument("-a", "--a", help="""Flag to generate
monthly report""", type=str)
parser.add_argument("-c", "--c", help="""Flag to generate
horizontal bar chat for highest and lowest temprature individually""", type=str)
parser.add_argument("-d", "--d", help="""Flag to generate
horizontal bar chat for highest and lowest temprature in same line""", type=str)
args = parser.parse_args()
# Regex for year argument
regex_year_pattern = re.compile("([0-9]{4}$)")
# Regex for month argument
regex_month_pattern = re.compile("([0-9]{4}[/](1[0-2]|[1-9])$)")

# checking arguments format
if args.e and not regex_year_pattern.match(args.e):
    print("Provided year is not in correct format it should be like 2000")
    exit()
if (((args.a) and not regex_month_pattern.match(args.a)) or
    ((args.c) and not regex_month_pattern.match(args.c)) or
    ((args.d) and not regex_month_pattern.match(args.d))):
    print("Provided month is not in correct format it should be like 2000/12")
    exit()

if args.e:
    date = args.e
    info_type = '-e'
elif args.a:
    date = args.a
    info_type = '-a'
elif args.c:
    date = args.c
    info_type = '-c'
elif args.d:
    date = args.d
    info_type = '-d'

if exists(args.path):
    data_files_list = [x for x in os.listdir(args.path)]
    # Passing files to parse engine to get list of weather
    parsed_list = Parse(date, data_files_list, args.path, info_type).data
    # Passing files to parse engine to get list of weather
    # by passing filter data list and information type
    if parsed_list:
        weather_data_report_generator.generate_report(parsed_list, info_type)
    else:
        print("No data found")
else:
    print("Directory does not exists at provided path")
    exit()

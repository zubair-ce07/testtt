"""
this module act as the main module or entry point of program
"""
import argparse
import os.path
from utils import validate_date_str
from weather_master import WeatherMaster

def create_arguments_parser():
    """
    this function creates the commandline arguments required
    for our program
    :return:
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--yearly",
                       help="For a given year display the highest "
                            "temperature and day, lowest temperature "
                            "and day, most humid day and humidity.",
                       action="store_true")
    group.add_argument("-a", "--monthly",
                       help="For a given month display the average"
                            " highest temperature, average lowest "
                            "temperature, average humidity.",
                       action="store_true")
    group.add_argument("-c", "--monthly_chart",
                       help="For a given month draw two horizontal "
                            "bar charts on the console for the highest "
                            "and lowest temperature on each day. Highest"
                            "in red and lowest in blue.",
                       action="store_true")
    # '-b' is for bar chart
    group.add_argument("-b", "--monthly_chart_one",
                       help="For a given month draw one horizontal "
                            "bar charts on the console for the highest "
                            "and lowest temperature on each day. Highest"
                            "in red and lowest in blue.",
                       action="store_true")
    parser.add_argument("date_string",
                        help="Date must be in the form 'YYYY' OR 'YYYY/MM'",
                        type=str)
    parser.add_argument("dir_path",
                        help="Path of Data Directory",
                        type=str)
    return parser.parse_args()

cmd_line_args = create_arguments_parser()

if not validate_date_str(cmd_line_args.date_string, 0):
    print("Date must be in the form 'YYYY' OR 'YYYY/MM'")
    exit(-1)
if not os.path.exists(cmd_line_args.dir_path):
    print("Please provide Valid path of Data Directory")
    exit(-1)
weather_master_obj = WeatherMaster(cmd_line_args)
weather_master_obj.show_weather()

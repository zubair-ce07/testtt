"""
this module act as the main module or entry point of program
"""
import utilities
from weather_master import WeatherMaster

cmd_line_args = utilities.create_arguments_parser()

if utilities.validate_date_str(cmd_line_args.date_string, 0) is False:
    print("Date must be in the form 'YYYY' OR 'YYYY/MM'")
    exit(-1)
if utilities.validate_path(cmd_line_args.dir_path) is False:
    print("Please provide Valid path of Data Directory")
    exit(-1)
weather_master_obj = WeatherMaster(cmd_line_args)
weather_master_obj.show_weather()

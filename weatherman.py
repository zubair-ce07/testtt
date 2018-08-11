import os.path
import  utilities
from weather_master import WeatherMaster


args = utilities.create_arguments_parser()

if utilities.validate_date_str(args.date_string, 0) is False:
    print("Date must be in the form 'YYYY' OR 'YYYY/MM'")
    exit(-1)
if os.path.exists(args.file_path) is False:
    print("Please provide Valid path of Data Directory")
    exit(-1)
weather_master = WeatherMaster(args)
weather_master.do_work()

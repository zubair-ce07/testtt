import argparse
from report_genarator import WeatherEvaluator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="to get the path of weather file")
    parser.add_argument("-e", "--e", help="to Show Yearly report",type=str)
    parser.add_argument("-a", "--a", help="to Show Monthly report",type=str)
    parser.add_argument("-c", "--c", help="to Show bar chart",type=str)
    
    arg_for_filepath = parser.parse_args()
    filepath = arg_for_filepath.path
    filepath = filepath[1:]     #Eliminate '/'
    args = parser.parse_args()
    
    if args.e:
        Date = args.e
        fpath = filepath + "/Murree_weather_" + Date
        yearly_report = WeatherEvaluator(fpath)
        yearly_report.yearly_report()

    if args.a:
        Date = args.a
        Date = Date.split('/')
        fpath = filepath + "/Murree_weather_" + Date[0]     #Spearate year and month
        monthly_report = WeatherEvaluator(fpath, int(Date[1])-1)
        monthly_report.monthly_average()
   
    if args.c:
        Date = args.c
        Date = Date.split('/')
        fpath = filepath + "/Murree_weather_" + Date[0]     #Spearate year and month
        horizontal_bar_report = WeatherEvaluator(fpath, int(Date[1])-1)
        horizontal_bar_report.horizontal_bar()
        
if(__name__ == "__main__"):
    main()
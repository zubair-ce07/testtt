import weatherman as weatherman
import argparse
import datetime

def validate_year(argument_string): 
    if len(argument_string) == 4 and argument_string.isdigit(): 
        return argument_string
    raise ValueError('Not a valid year format')

def validate_month(argument_string): 
    date_arg = argument_string.split('/')
    year_arg = date_arg[0] 
    month_arg = date_arg[1]
    if len(year_arg) == 4 and len(month_arg) > 0 and year_arg.isdigit() and month_arg.isdigit(): 
        return argument_string
    raise ValueError('Not a valid year or month format')

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("-a", help="Format should be like yyyy/m", type=validate_month)
    parser.add_argument("-c", help="Format should be like yyyy/m", type=validate_month)
    parser.add_argument("-e", help="Format should be like yyyy", type=validate_year)
    args = parser.parse_args()
    if not (args.a or args.c or args.e):
        parser.error('No arguments provided!')
    return args

def generate_reports(args):
    report = weatherman.WeatherAnalyze()
    if args.a:
        file_names = report.get_file_name("a", args.a, args.path)
        if file_names:
            file_data = report.reading_file(file_names)
            report.display_monthly_report(file_data)
        else:
            print("File may not be available against -a argument!")
    if args.c:
        file_names = report.get_file_name("c", args.c, args.path)
        if file_names:
            file_data = report.reading_file(file_names)
            report.display_month_chart_report(file_data)
            report.display_month_bar_chart(file_data)
        else:
            print("File may not be available against -c argument!")
    if args.e:
        file_names = report.get_file_name("e", args.e, args.path)
        if file_names:
            file_data = report.reading_file(file_names)
            report.display_yearly_report(file_data)
        else:
            print("File may not be available against -e argument!")
    
def main():
    arguments = get_arguments()
    generate_reports(arguments)
if __name__ == "__main__":
    main()

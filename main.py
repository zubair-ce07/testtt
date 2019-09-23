import weatherman as weatherman
import argparse
import datetime


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("-a",required=False)
    print(parser.add_argument("-c",required=False))
    parser.add_argument("-e",required=False)
    args = parser.parse_args()
    if not (args.a or args.c or args.e):
        parser.error('No arguments provided.')
    return args

def generate_reports(args):
    report = weatherman.WeatherReport()
    file_info = weatherman.FileData()
    if args.a:
        
        if datetime.datetime.strptime(args.a, '%Y/%m'):
            file_names = file_info.get_file_name("a", args.a, args.path)
            if file_names:
                data = file_info.reading_file(file_names)
                report.monthly_report(data)
            else:
                print("File may not be available against -a argument!")
        else:
            print('Not a valid date')

    if args.c:
        if datetime.datetime.strptime(args.c, '%Y/%m'):
            file_names = file_info.get_file_name("c", args.c, args.path)
            if file_names:
                data = file_info.reading_file(file_names)
                report.chart_report(data)
                report.chart_report_bonus(data)
            else:
                print("File may not be available against -c argument!")
        else:
            print('Not a valid date')

    if args.e:
        if datetime.datetime.strptime(args.e, '%Y'):
            file_names = file_info.get_file_name("e", args.e, args.path)
            if file_names:
                data = file_info.reading_file(file_names)
                report.yearly_report(data)
            else:
                print("File may not be available against -e argument!")
        else:
            print('Not a valid date')


def main():
    args = get_arguments()
    generate_reports(args)
    

if __name__ == "__main__":
    main()
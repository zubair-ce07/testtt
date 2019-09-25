import weatherman as weatherman
import argparse
import datetime

class ArgumentsValidation:
    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("path", type=str)
        parser.add_argument("-a",required=False, help="Format should be like yyyy/m")
        parser.add_argument("-c",required=False, help="Format should be like yyyy/m")
        parser.add_argument("-e",required=False, help="Format should be like yyyy")
        args = parser.parse_args()
        if not (args.a or args.c or args.e):
            parser.error('No arguments provided.')
        return args

    def generate_reports(self,args):
        report = weatherman.WeatherReport()
        file_info = weatherman.FileData()
        if args.a:
        
            if datetime.datetime.strptime(args.a, '%Y/%m'):
                file_names = file_info.get_file_name("a", args.a, args.path)
                if file_names:
                    file_data = file_info.reading_file(file_names)
                    report.display_monthly_report(file_data)
                else:
                    print("File may not be available against -a argument!")
            else:
                print('Not a valid date fomat')

        if args.c:
            if datetime.datetime.strptime(args.c, '%Y/%m'):
                file_names = file_info.get_file_name("c", args.c, args.path)
                if file_names:
                    file_data = file_info.reading_file(file_names)
                    report.display_month_chart_report(file_data)
                    report.display_month_bar_chart(file_data)
                else:
                    print("File may not be available against -c argument!")
            else:
                print('Not a valid date format')

        if args.e:
            if datetime.datetime.strptime(args.e, '%Y'):
                file_names = file_info.get_file_name("e", args.e, args.path)
                if file_names:
                    file_data = file_info.reading_file(file_names)
                    report.display_yearly_report(file_data)
                else:
                    print("File may not be available against -e argument!")
            else:
                print('Not a valid year format')


def main():
    arguments = ArgumentsValidation()
    args = arguments.get_arguments()
    arguments.generate_reports(args)
    

if __name__ == "__main__":
    main()

import argparse
from datetime import datetime

from read_weather_record import Record_File

from calculate_result import monthly_computing_results
from calculate_result import yearly_computing_results

from report import monthly_report
from report import monthly_bonus_report


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', type=lambda date: datetime.strptime(date, '%Y'))
    parser.add_argument('-a', type=lambda date: datetime.strptime(date, '%Y/%m'))
    parser.add_argument('-c', type=lambda date: datetime.strptime(date, '%Y/%m'))

    return  parser.parse_args()

def main():
    arguments = parse_arguments()
    
    record = Record_File()
    weather_records = record.read_file()
    
    if arguments.a:
        argument_a_year = str(arguments.a.year)
        argument_a_month = str(arguments.a.month)

        results = monthly_computing_results()

        get_objects = results.getting_monthly_objects(weather_records,argument_a_year,argument_a_month)
        results.getmaximumaverage(get_objects)
        results.getminimumaverage(get_objects)
        results.gethumidityaverage(get_objects)
    if arguments.e:
        argument_e_year = str(arguments.e.year)

        results = yearly_computing_results()

        get_objects = results.getting_yearly_objects(weather_records,argument_e_year)
        results.gethighesttemperature(get_objects)
        results.getlowesttemperature(get_objects)
        results.gethighesthumidity(get_objects)  
    if arguments.c:
        argument_c_year = str(arguments.c.year)
        argument_c_month = str(arguments.c.month)

        monthly_report_chart = monthly_report()

        getting_objects = monthly_report_chart.getting_monthly_objects(weather_records,argument_c_year,argument_c_month)
        print(arguments.c.strftime("%B %Y"))
        monthly_report_chart.monthly_chart(getting_objects)
        
        print("Bonus Task")

        bonus_report = monthly_bonus_report()

        report = bonus_report.getting_monthly_objects(weather_records,argument_c_year,argument_c_month)
        print(arguments.c.strftime("%B %Y"))
        bonus_report.bonus_chart(report)
    
     
if __name__ == '__main__':
    main()

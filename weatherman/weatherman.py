import datetime
import argparse
from report_generation import Printer
from files_reading import file_reader
from calculations import Calculator

printer = Printer()
reader = file_reader()
calculator = Calculator()


def find_max_values(all_data, input_date):
    max_temp, min_temp, max_humidity = calculator.getting_temperatures(all_data, input_date)
    printer.print_max(max_temp, min_temp, max_humidity)


def find_avge_values(all_data, input_date):
    max_avg, min_avg, mean_humdity = calculator.calculating_averages(all_data, input_date)
    printer.print_averges(max_avg, min_avg, mean_humdity)


def design_graph(all_data, input_date):
    final_values = calculator.getting_min_max(all_data, input_date)
    printer.print_graph(final_values, input_date)
    

def main():        
    parser = argparse.ArgumentParser()
    parser.add_argument("basepath", help="directory path",
                        type=str)
    parser.add_argument("-e", "--max_temp", help="year to get max teprature",
                        type=lambda d: datetime.datetime.strptime(d, '%Y').date())
    parser.add_argument("-a", "--avg_temp", help="Year and month to get average temprature",
                        type=lambda d: datetime.datetime.strptime(d, '%Y/%m').date())
    parser.add_argument("-c", "--graph", help="Year and month to Draw graphs",
                        type=lambda d: datetime.datetime.strptime(d, '%Y/%m').date())
    
    args = parser.parse_args()  
    
    all_data = reader.read_files(args.basepath)
    
    if args.max_temp:
        find_max_values(all_data, args.max_temp)   
    
    if args.avg_temp:
        find_avge_values(all_data, args.avg_temp)
    
    if args.graph:
        design_graph(all_data, args.graph)
    
if __name__ == '__main__':
    main()

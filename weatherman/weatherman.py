import datetime
import argparse
from report_generation import Printer
from Files_reading import Reader

p=Printer()


def find_max_values(all_data, inputt):
    p.print_max(all_data, inputt)


def find_avge_values(all_data, input_date):
    
    p.print_averges(all_data, input_date)


def design_graph(all_data, input_date):
    
    p.print_graph(all_data, input_date)
    

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
    
    r = Reader(args.basepath)
    all_data = r.read_files()

    if args.max_temp:
        find_max_values(all_data, args.max_temp)   
    
    if args.avg_temp:
        find_avge_values(all_data, args.avg_temp)
    
    if args.graph:
        design_graph(all_data, args.graph)
    

main()

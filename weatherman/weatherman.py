import datetime
import report_generation as generator
import calculations as cal
import argparse


def find_max_values(basepath, year):
    max_temp = {'MaxTemp': 0, 'date': ''}
    min_temp = {'MinTemp': 200, 'date': ''}
    max_humd = {'MaxHumd': 0, 'date': ''}
   
    files = cal.get_files(basepath)
    for file in files:
        (max_temp, min_temp, max_humd) = cal.getting_max(str(file), max_temp, min_temp, max_humd, year)
   
    generator.print_max(max_temp, min_temp, max_humd)
   

def find_avge_values(basepath, year_month):
    max_temp = []
    min_temp = []
    max_humd = []

    files = cal.get_files(basepath) 
    for file in files:
        (max_temp, min_temp, max_humd) = cal.calculating_averages(str(file), year_month, max_temp, min_temp, max_humd)

    generator.print_averges(max_temp, min_temp, max_humd) 


def design_graph(basepath, year_month):
    max_temp = {}
    min_temp = {}
    files = cal.get_files(basepath) 
    for file in files:
        (max_temp, min_temp) = cal.getting_temperatures(str(file), year_month, max_temp, min_temp)
    generator.print_graph(max_temp, min_temp)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("basepath", help="directory path",
                        type=str)
    parser.add_argument("-e", "--max_temp", help="year to get max teprature",
                        type=lambda d: datetime.datetime.strptime(d, '%Y').year)
    parser.add_argument("-a", "--avg_temp", help="Year and month to get average temprature",
                        type=lambda d: datetime.datetime.strptime(d, '%Y/%m').date())
    parser.add_argument("-c", "--graph", help="Year and month to Draw graphs",
                        type=lambda d: datetime.datetime.strptime(d, '%Y/%m').date())

    args = parser.parse_args()    
    if args.max_temp:
            find_max_values(args.basepath, args.max_temp)   
    if args.avg_temp:
            find_avge_values(args.basepath, args.avg_temp)
    
    if args.graph:
            design_graph(args.basepath, args.graph)
main()

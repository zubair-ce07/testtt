import argparse
import os

import ReportGenerator


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="to get the path of weather file")
    parser.add_argument("-e", "--report1", help="to Show report1",type=str)
    parser.add_argument("-a", "--report2", help="to Show report2",type=str)
    parser.add_argument("-c", "--report3", help="to Show report3",type=str)
    

    argForFilepath = parser.parse_args()
    filepath = argForFilepath.path
    filepath = filepath[1:]     #Eliminate '/'
    args = parser.parse_args()
    
    if args.report1:
        Date = args.report1
        fpath = filepath + "/Murree_weather_" + Date
        yearly_report = ReportGenerator.YearlyReport(fpath)

    if args.report2:
        Date = args.report2
        Date = Date.split('/')
        fpath = filepath + "/Murree_weather_" + Date[0]     #Spearate year and month
        monthly_report = ReportGenerator.MonthlyReport(fpath, int(Date[1])-1)
        
    if args.report3:
        Date = args.report3
        Date = Date.split('/')
        fpath = filepath + "/Murree_weather_" + Date[0]     #Spearate year and month
        horizontal_bar_report = ReportGenerator.HorizontalBarReport(fpath, int(Date[1])-1)
        
    print("***PDF Report is Also generated***")

main()


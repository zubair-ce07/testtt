import argparse
import os

import report1
import report2
import report3


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
        report1.Report(fpath)

    if args.report2:
        Date = args.report2
        Date = Date.split('/')
        fpath = filepath + "/Murree_weather_" + Date[0]     #Spearate year and month
        report2.Report(fpath, int(Date[1])-1)
        
    if args.report3:
        Date = args.report3
        Date = Date.split('/')
        fpath = filepath + "/Murree_weather_" + Date[0]     #Spearate year and month
        report3.Report(fpath, int(Date[1])-1)
       
    print("***PDF Report is Also generated***")

main()


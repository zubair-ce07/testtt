"""Weather insights"""

import sys
import math
import parser
import calculations
import reporter

# Command Line arguments.
data_path = sys.argv[1]
task = sys.argv[2]

# Following years are present in the data.
years = [
    "2004", "2005", "2006",
    "2007", "2008", "2009",
    "2010", "2011", "2012",
    "2013", "2014", "2015", "2016"
]
months = [
    "Jan", "Feb", "Mar",
    "Apr", "May", "Jun",
    "Jul", "Aug", "Sep",
    "Oct", "Nov", "Dec", 
]

# Read data by using the parser.
data = parser.read_files(years, months, data_path)

# Do calculations using the data.
years_monthly_records = calculations.weather_calculations(
    years, months, data)
per_year_records = calculations.calculate_yearly(
    years, months, 
    years_monthly_records)

# For Multiple reports
i = 2
while i < len(sys.argv):
    
    task = sys.argv[i]
    input_data = sys.argv[i+1]
    i += 2

    # Report as the user commanded.
    if task == '-e':
        reporter.yearly_report(per_year_records, input_data)
    elif task == '-a':
        reporter.monthly_report(years_monthly_records, input_data, months)
    elif task == '-c':
        reporter.monthly_bar_chart(years_monthly_records, input_data, months)
        reporter.horizontal_barchart(years_monthly_records, input_data, months)
    else:
        print ("Sorry... There is no such report....")

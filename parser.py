import os
from collections import defaultdict


def read_files(years, months, data_path):
    """This function will read all the weather data."""

    # Dictionary to store all the data
    data_for_all_months = {}

    # Read all files
    for year in years:
        for month in months:

            file = data_path + "Murree_weather_" + year + "_" + month + ".txt"

            if os.path.exists(file):

                monthly_readings = file_parser(file)
                data_for_all_months[year + "_" + month] = monthly_readings
    
    return data_for_all_months

# 


def file_parser(month):
    """This function will read a File in a dictionary object."""

    
    monthly_readings = defaultdict(lambda: [])
    f = open(month)
    data_header = f.readline().replace('\n', '').split(',')

    for reading in f:

        reading = reading.replace("\n", '').split(',')

        for header_val, value in zip(data_header, reading):

            if value:
                if header_val in ['PKST', 'PKT', ' Events']:

                    monthly_readings[header_val].append(value)

                elif header_val in [
                    ' Max VisibilityKm', ' Mean VisibilityKm',
                    ' Min VisibilitykM', 'Precipitationmm',
                    ' Mean Sea Level PressurehPa'
                    ]:

                    monthly_readings[header_val].append(float(value))

                else:

                    try:
                        monthly_readings[header_val].append(int(value))
                    except:
                        print (header_val, "    ", value)
            else:

                monthly_readings[header_val].append(None)
    f.close()
    
    return monthly_readings
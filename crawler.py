import requests
from bs4 import BeautifulSoup
import re
import os
import csv
import datetime

# The function will recieve city code and return the years for which weather history is availble 
def get_year_range_from_dropdown(city_code):
    url = f"https://www.wunderground.com/history/airport/{city_code}/1996/1/1/MonthlyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="
    code = requests.get(url)
    html_data = BeautifulSoup(code.text, "html.parser")
    year_drop_down = html_data.find('select', {'class':'year form-select'})
    year_list = []
    for option in year_drop_down.findAll('option'):
        year_list.append(option.getText())

    return year_list

# The function will get years and city code and generate a list of possible URLs
def get_dynamic_url_list(years_range, city_code):
    url_list = []
    for year in years_range:
        for month in range(1, 13):
            url = f"https://www.wunderground.com/history/airport/{city_code}/{year}/{month}/1/MonthlyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="
            url_list.append(url)
    return url_list

#This function will recieve list of data, header of file and file name to write
def file_writer(file_name, fields_name, data_list):
    with open(file_name, "w") as file:
        writer = csv.DictWriter(file , fieldnames=fields_name)
        writer.writeheader()
        writer.writerows(data_list)

if __name__ == '__main__':

    # City code, change this code to get data from other cities
    city_code = 'OPLA'
    years_range = get_year_range_from_dropdown(city_code)
    url_list = get_dynamic_url_list(years_range, city_code)
    fields_name = ['PKT','High TempC','Average TempC','Low TempC','High Dew Point','Average Dew Point','Low Dew Point','High Humidity','Average Humidity','Low Humidity','High Sea Level Pressure','Average Sea Level Pressure','Low Sea Level Pressure','High VisibilityKM','Average VisibilityKM','Low VisibilityKM','High WindKMH','Average WindKMH','Low WindKMH','Precipitaion mm','Events']

    for url in url_list:
        code = requests.get(url)
        html_data = BeautifulSoup(code.text, "html.parser")
        table_data = html_data.find('table', {'id':'obsTable'})

        # Month and year for file name and PKT format
        month = html_data.find('select', {'class':'month form-select'}).find('option', {'selected':'selected'}).getText()
        year = html_data.find('select', {'class':'year form-select'}).find('option', {'selected':'selected'}).getText()

        if table_data:
            table_body = table_data.findAll('tbody')
            data_list = []

            for body in table_body[1:]:
                for row in body.select('tr'):
                    row_list = []
                    for td in row.findAll('td'):
                        if (td.find('span' , {'class':'wx-value'})):
                            row_list.append(td.find('span' , {'class':'wx-value'}).getText())
                        else:
                            row_list.append(td.getText().strip().replace('\n','').replace('\t', ''))

                    #first index will have date, format the date properly.
                    date_string = f"{year}/{month}/{row_list[0]}"
                    date = datetime.datetime.strptime(date_string, "%Y/%B/%d").strftime("%Y-%m-%d")
                    row_list[0] = date

                    # Convert the appended list to dictionary to use DictWriter
                    dictionary = {}
                    if len(row_list) != 0:
                        for index in range(0, len(fields_name)):
                            dictionary[fields_name[index]] = row_list[index]
                
                    data_list.append(dictionary)
            
            # File name in specified format
            file_month = datetime.datetime.strptime(date_string, "%Y/%B/%d").strftime("%Y_%b")
            file_name = f"WeatherFiles/Lahore_Weather_{file_month}.txt"

            file_writer(file_name, fields_name, data_list)
        else:
            print(f"Data not found for {month} {year}")
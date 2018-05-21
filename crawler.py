import requests
from bs4 import BeautifulSoup
import datetime
from file_handler import FileHandler
from url_generator import UrlGenerator
import parsel

class WeatherCrawler:

    #This function formats data in proper dictionary format
    def data_formatter(year, month, row_list, fields_name):
        #first index will have date, format the date properly.
        date_string = f"{year}/{month}/{row_list[0]}"
        date = datetime.datetime.strptime(date_string, "%Y/%B/%d").strftime("%Y-%m-%d")
        row_list[0] = date
        
        #Convert the list to dictionary to use with csv DictWriter
        dictionary = {}
        for index in range(0, len(fields_name)):
            dictionary[fields_name[index]] = row_list[index]
        return dictionary

    # This function accepts month and year
    # and returns file name for that month in a specified format
    def file_name_formatter(year, month):
        file_month = datetime.datetime.strptime(f"{year}/{month}", "%Y/%B").strftime("%Y_%b")
        file_name = f"WeatherFiles/Lahore_Weather_{file_month}.txt"
        return file_name


    if __name__ == '__main__':
        # City code, change this code to get data for other cities
        city_code = 'OPLA'
        
        url_list = UrlGenerator.get_dynamic_url_list(city_code)
        fields_name = ['PKT','High TempC','Average TempC','Low TempC','High Dew Point','Average Dew Point','Low Dew Point','High Humidity','Average Humidity','Low Humidity','High Sea Level Pressure','Average Sea Level Pressure','Low Sea Level Pressure','High VisibilityKM','Average VisibilityKM','Low VisibilityKM','High WindKMH','Average WindKMH','Low WindKMH','Precipitaion mm','Events']

        for url in url_list:
            code = requests.get(url)
            parser = parsel.Selector(code.text)
            
            # Month and year for file name and PKT format
            month = parser.css('select.month').css('option[selected=selected]::text').extract_first()
            year = parser.css('select.year').css('option[selected=selected]::text').extract_first()
            
            table = parser.css('table.obs-table')

            if table:
                tableBody = table.css('tbody')
                data_list = []
            
                for tbody in tableBody[1:]:
                    row_list = []
                    for value in tbody.css('tr').css('td'):
                        if (value.css('span.wx-value::text').extract_first()):
                            row_list.append(value.css('span.wx-value::text').extract_first())
                        else:
                            row_list.append(value.xpath('.//text()').extract_first().strip().replace('\n','').replace('\t', ''))
                    
                    if row_list:
                        dictionary = data_formatter(year, month, row_list, fields_name)
                    
                    data_list.append(dictionary)
                    file_name = file_name_formatter(year, month)
                    FileHandler.file_writer(file_name, fields_name, data_list)
            else:
                print(f"Data not found for {month} {year}")

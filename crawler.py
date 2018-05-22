import requests
import datetime
from file_handler import FileHandler
from url_generator import UrlGenerator
import parsel

class WeatherCrawler:

    #This function formats data in proper dictionary format
    @staticmethod
    def data_formatter(year, month, row_list, fields_name):
        #first index will have date, format the date properly.
        date_string = f"{year}/{month}/{row_list[0]}"
        date = datetime.datetime.strptime(date_string, "%Y/%B/%d").strftime("%Y-%m-%d")
        row_list[0] = date
        
        #Convert the list to dictionary to use with csv DictWriter
        return dict(zip(fields_name, row_list))

    # This function accepts month and year
    # and returns file name for that month in a specified format
    @staticmethod
    def file_name_formatter(year, month):
        file_month = datetime.datetime.strptime(f"{year}/{month}", "%Y/%B").strftime("%Y_%b")
        file_name = f"WeatherFiles/Lahore_Weather_{file_month}.txt"
        return file_name


    @staticmethod
    def weather_crawler() :
        # City code, change this code to get data for other cities
        city_code = 'OPLA'
        
        url_list = UrlGenerator.get_dynamic_url_list(city_code)
        fields_name = ['PKT','High TempC','Average TempC','Low TempC','High Dew Point','Average Dew Point','Low Dew Point','High Humidity','Average Humidity','Low Humidity','High Sea Level Pressure','Average Sea Level Pressure','Low Sea Level Pressure','High VisibilityKM','Average VisibilityKM','Low VisibilityKM','High WindKMH','Average WindKMH','Low WindKMH','Precipitaion mm','Events']

        for url in url_list:
            code = requests.get(url)
            parser = parsel.Selector(code.text)
            # Month and year for file name and PKT format
            month = parser.css('select.month > option[selected=selected]::text').extract_first()
            year = parser.css('select.year > option[selected=selected]::text').extract_first()
            
            table = parser.css('table.obs-table > tbody')[1:]
            data_list = []
            
            for row in table.css('tr'):
                row_list = []
                for value in row.css('td'):
                    span_text = value.css('span.wx-value::text').extract_first()
                    if (span_text):
                        row_list.append(span_text)
                    else:
                        row_list.append(value.xpath('.//text()').extract_first().strip().replace('\n','').replace('\t', ''))
                        
                if row_list:
                    dictionary = WeatherCrawler.data_formatter(year, month, row_list, fields_name)
                    data_list.append(dictionary)

            file_name = WeatherCrawler.file_name_formatter(year, month)
            FileHandler.file_writer(file_name, fields_name, data_list)
        
if __name__ == '__main__':
    WeatherCrawler.weather_crawler()

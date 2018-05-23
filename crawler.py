import requests
import datetime
import parsel
from file_handler import FileHandler
from url_generator import UrlGenerator


class WeatherCrawler:
    # City code, change this code to get data for other cities
    CITY_CODE = "OPLA"
    FIELD_NAMES = ['PKT','High TempC','Average TempC','Low TempC','High Dew Point','Average Dew Point','Low Dew Point','High Humidity','Average Humidity','Low Humidity','High Sea Level Pressure','Average Sea Level Pressure','Low Sea Level Pressure','High VisibilityKM','Average VisibilityKM','Low VisibilityKM','High WindKMH','Average WindKMH','Low WindKMH','Precipitaion mm','Events']

    #This function formats data in proper dictionary format    
    def data_formatter(year, month, row_list):
        #first index will have date, format the date properly.
        date_string = f"{year}/{month}/{row_list[0]}"
        date = datetime.datetime.strptime(date_string, "%Y/%B/%d").strftime("%Y-%m-%d")
        row_list[0] = date
        
        #Convert the list to dictionary to use with csv DictWriter
        return dict(zip(WeatherCrawler.FIELD_NAMES, row_list))

    # This function accepts month and year
    # and returns file name for that month in a specified format
    def file_name_formatter(year, month):
        file_month = datetime.datetime.strptime(f"{year}/{month}", "%Y/%B").strftime("%Y_%b")
        file_name = f"WeatherFiles/Lahore_Weather_{file_month}.txt"
        return file_name

    def weather_crawler() :
        url_list = UrlGenerator.get_dynamic_url_list(WeatherCrawler.CITY_CODE)
        
        for url in url_list:
            response = requests.get(url)
            parser_s = parsel.Selector(response.text)
            # Month and year for file name and PKT format
            month = parser_s.css('select.month > option[selected=selected]::text').extract_first()
            year = parser_s.css('select.year > option[selected=selected]::text').extract_first()
            
            tablebody_s = parser_s.css('table.obs-table > tbody')[1:]
            data_list = []
            
            for row_s in tablebody_s:
                row_list = []
                for td_s in row_s.css('tr > td'):
                    span_text = td_s.css('span.wx-value::text').extract_first()
                    if (span_text):
                        row_list.append(span_text)
                    else:
                        row_list.append(td_s.xpath('.//text()').extract_first()
                                .strip().replace('\n','').replace('\t', ''))
                        
                if row_list:
                    dictionary = WeatherCrawler.data_formatter(year, month, row_list)
                    data_list.append(dictionary)

            file_name = WeatherCrawler.file_name_formatter(year, month)
            FileHandler.file_writer(file_name, WeatherCrawler.FIELD_NAMES, data_list)
        
if __name__ == '__main__':
    WeatherCrawler.weather_crawler()

import requests
from bs4 import BeautifulSoup

class UrlGenerator:

    # This method accepts city code and
    # returns then list of years for which weather hisory is available
    @staticmethod
    def get_year_range_from_dropdown(city_code):
        url = f"https://www.wunderground.com/history/airport/{city_code}/1996/1/1/MonthlyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="
        code = requests.get(url)
        html_data = BeautifulSoup(code.text, "html.parser")
        year_drop_down = html_data.find('select', {'class':'year form-select'})
        year_list = []
        for option in year_drop_down.findAll('option'):
            year_list.append(option.getText())

        return year_list

    # The function accepts list of years with city code and returns a list of all URLs
    @staticmethod
    def get_dynamic_url_list(city_code):
        years_range = UrlGenerator.get_year_range_from_dropdown(city_code)
        url_list = []
        for year in years_range:
            for month in range(1, 13):
                url = f"https://www.wunderground.com/history/airport/{city_code}/{year}/{month}/1/MonthlyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="
                url_list.append(url)
        return url_list

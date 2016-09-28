import scrapy
from itertools import product
import re
from scrapy import Request
from ..items import WeatherItem
import calendar


class WundergroundSpider(scrapy.Spider):
    name = "wunderground"
    allowed_domains = ["wunderground.com"]
    start_urls = (
        'https://www.wunderground.com/history/airport/OPLA/2016/09/28/DailyHistory.html?req_city=Lahore'
        '&req_statename=Pakistan&reqdb.zip=00000&reqdb.magic=1&reqdb.wmo=41641',
    )

    def parse(self, response):
        years = response.css(".year.form-select > option::text").extract()
        months = response.css(".month.form-select > option::attr(value)").extract()
        for year, month in product(years, months):
            request = Request(self.create_url(response, year, month), callback=self.parse_weather)
            request.meta['current_date'] = year, month
            yield request

    def parse_weather(self, response):
        year, month = response.meta['current_date']
        item = WeatherItem()
        item['year'] = year
        item['month'] = calendar.month_abbr[int(month)]
        item['city'] = self.city(response)
        item['weather_rows'] = response.css("::text").extract()
        if len(item['weather_rows']) > 1:
            return item

    def city(self, response):
        return re.findall("req_city=(\w*)", response.url)[0]

    def create_url(self, response, year, month):
        url_parts = re.split("[0-9]{4}\/[0-9]{0,2}\/[0-9]{0,2}", response.url)
        csv_url = "{}/{}/1".format(year, month).join(url_parts)
        csv_url = csv_url.replace("DailyHistory", "MonthlyHistory")
        return csv_url if "format=1" in csv_url else csv_url + "&format=1"

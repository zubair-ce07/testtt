import requests
import re
from parsel import Selector


class Crawler:
    '''This class take care of all the crawling & parsing html doc'''

    def crawl_url(self, url):
        response = requests.get(url)
        return self.parse_response(response)

    def parse_response(self, response):
        sel = Selector(response.text)
        return sel.xpath("//body//text()").re('\w+')

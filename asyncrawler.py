import asyncio
import requests
import time
import argparse

from parsel import Selector
from urllib.parse import urljoin


class AsynCrawler:

    def __init__(self, url, concurrent_requests=1,
                 download_delay=0, total_visits=0):

        self.url = url
        self.html = self.download_html()
        self.concurrent_request = concurrent_requests
        self.download_delay = download_delay
        self.total_visits = total_visits
        self.total_requests = 0

    def get_page_size(self, url):
        self.total_requests += 1
        with requests.get(url) as response:
            time.sleep(self.download_delay)
            return len(response.content)

    def download_html(self):
        with requests.get(self.url) as response:
            return response.text

    def get_anchor_urls(self):
        sel = Selector(text=self.html)
        return [urljoin(self.url, url) for url in sel.css('html').xpath('.//a/@href').getall()]


def main():
    con_requests = int(input("Enter no of concurrent requests"))
    delay = int(input("Enter delay in secs"))
    visits = int(input("Enter total urls to visit"))

    web_crawler = AsynCrawler('http://google.com/', con_requests,
                              delay, visits)

    anchor_urls = web_crawler.get_anchor_urls()
    print(anchor_urls)


if __name__ == '__main__':
    main()

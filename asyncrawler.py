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


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("website", help="website url for crawling", type=str)
    parser.add_argument("concurrent_requests", help="Concurrent request that can be made", type=int)
    parser.add_argument("download_delay", help="Download delay for each worker", type=int)
    parser.add_argument("total_visits", help="Total urls to visits", type=int)
    return parser.parse_args()


def main():
    args = parse_arguments()

    web_crawler = AsynCrawler(args.website, args.concurrent_requests,
                              args.download_delay, args.total_visits)

    anchor_urls = web_crawler.get_anchor_urls()
    print(anchor_urls)


if __name__ == '__main__':
    main()

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

    def generate_report(self, anchor_urls, total_bytes, size):
        if self.total_visits <= len(anchor_urls):
            print(f'\nTotal request: {self.total_requests}')
            print(f'Total bytes downloaded: {total_bytes}')
            print(f'Average page size: {int(total_bytes / size)}\n')

    async def get_total_bytes(self, anchor_urls, async_loop):
        if self.total_visits <= len(anchor_urls):
            futures = []
            for index in range(self.total_visits):
                futures += [async_loop.run_in_executor(None, self.get_page_size, anchor_urls[index])
                            for request in range(self.concurrent_request)]
            return sum(stat for stat in await asyncio.gather(*futures))

        print("Number of visited urls exceeded total urls\n")


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

    t0 = time.time()
    loop = asyncio.get_event_loop()
    total_bytes = loop.run_until_complete(web_crawler.get_total_bytes(anchor_urls, loop))
    t1 = time.time()

    web_crawler.generate_report(anchor_urls, total_bytes, args.total_visits)
    print(f'Total Time {t1-t0}')


if __name__ == '__main__':
    main()

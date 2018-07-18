import asyncio
import requests
import argparse
import urllib.request as url_checker

from parsel import Selector
from urllib.parse import urljoin
from time import sleep


class AsyncCrawler:

    def __init__(self, url, concurrent_requests=1,
                 download_delay=0, total_visits=0):
        self.url = url
        self.concurrent_request = concurrent_requests
        self.download_delay = download_delay
        self.total_visits = total_visits
        self.total_requests = 0

    def get_html(self):
        with requests.get(self.url) as response:
            return response.text

    def get_anchor_urls(self):
        sel = Selector(text=self.get_html())
        return list(map(lambda url: urljoin(self.url, url), sel.css('a::attr(href)').getall()))

    def get_page_size(self, url):
        self.total_requests += 1
        with requests.get(url) as response:
            sleep(self.download_delay)
            return len(response.content)

    def generate_report(self, anchor_urls, total_bytes):
        if self.total_visits <= len(anchor_urls):
            print(f'\nTotal request: {self.total_requests}')
            print(f'Total bytes downloaded: {total_bytes}')
            print(f'Average page size: {int(total_bytes / self.total_visits)}\n')

    async def get_total_bytes(self, anchor_urls, async_loop):
        if self.total_visits <= len(anchor_urls):
            futures = []
            for index in range(self.total_visits):
                futures += [async_loop.run_in_executor(None, self.get_page_size, anchor_urls[index])
                            for request in range(self.concurrent_request)]
            return sum(page_size for page_size in await asyncio.gather(*futures))

        print("Number of visited urls exceeded total urls\n")


def validate_requests(concurrent_requests):
    concurrent_requests = int(concurrent_requests)
    if concurrent_requests > 0:
        return concurrent_requests
    raise argparse.ArgumentTypeError("Value cannot be less than or equal to 0")


def validate_web_url(website):
    try:
        url_checker.urlopen(website)
        return website
    except url_checker.URLError:
        raise argparse.ArgumentTypeError(f"Invalid url {website}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("website", help="web address for crawling", type=validate_web_url)
    parser.add_argument("concurrent_requests", help="Concurrent request that can be made", type=validate_requests)
    parser.add_argument("download_delay", help="Download delay for each worker", type=int)
    parser.add_argument("total_visits", help="Total urls to visits", type=int)
    return parser.parse_args()


def main():
    args = parse_arguments()

    web_crawler = AsyncCrawler(args.website, args.concurrent_requests,
                               args.download_delay, args.total_visits)
    anchor_urls = web_crawler.get_anchor_urls()

    loop = asyncio.get_event_loop()
    total_bytes = loop.run_until_complete(web_crawler.get_total_bytes(anchor_urls, loop))

    web_crawler.generate_report(anchor_urls, total_bytes)


if __name__ == '__main__':
    main()

import asyncio
import requests
import argparse
import urllib.request as url_checker
import re

from parsel import Selector
from urllib.parse import urljoin


class AsyncCrawler:

    def __init__(self, parent_url, concurrent_requests=1,
                 download_delay=0.0, maximum_urls=0):
        self.parent_url = parent_url
        self.download_delay = download_delay
        self.maximum_urls = maximum_urls
        self.bounded_semaphore = asyncio.BoundedSemaphore(concurrent_requests)
        self.visited_urls = set()
        self.download_bytes = 0

    async def get_html(self, url, event_loop):
        async with self.bounded_semaphore:
            await asyncio.sleep(self.download_delay)
            future_response = event_loop.run_in_executor(None, requests.get, url)
            response = await future_response
            self.download_bytes += len(response.content)
            print(f"Visited url {url}")
            return response.text

    async def extract_anchor_urls(self, base_url, event_loop):
        sel = Selector(text=await self.get_html(base_url, event_loop))
        return set(map(lambda url: urljoin(base_url, url), sel.css('a::attr(href)').getall()))

    async def extract_multiple_anchor_urls(self, to_extract, event_loop):
        futures = []
        extracted_urls = []
        for web_url in to_extract:
            if len(self.visited_urls) < self.maximum_urls:
                if web_url in self.visited_urls:
                    continue

                self.visited_urls.add(web_url)
                futures.append(self.extract_anchor_urls(web_url, event_loop))

        for future in asyncio.as_completed(futures):
            try:
                extracted_urls.append(await future)
            except Exception as e:
                print(f'Entered exception {e}')
        return extracted_urls

    async def crawl(self, event_loop):
        anchor_urls = [self.parent_url]
        while len(self.visited_urls) < self.maximum_urls:
            results = await self.extract_multiple_anchor_urls(anchor_urls, event_loop)
            anchor_urls = []
            for extracted_urls in results:
                anchor_urls.extend(extracted_urls)

    def generate_report(self):
        print(f'\nTotal request: {self.maximum_urls}')
        print(f'Total bytes downloaded: {self.download_bytes}')
        print(f'Average page size: {int(self.download_bytes / len(self.visited_urls))}\n')

    def execute_crawler(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.crawl(loop))
        loop.close()
        print("Done crawling")


def validate_web_url(website):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, website):
        return website
    raise argparse.ArgumentTypeError(f"Invalid url {website}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("parent_url", help="url for crawling", type=validate_web_url)
    parser.add_argument("maximum_urls", help="Total urls to visits", type=int)
    parser.add_argument("download_delay", help="Download delay for each worker", type=float)
    parser.add_argument("number_of_concurrent_requests",
                        help="Requests that can be made concurrently",
                        type=lambda x: int(x) if int(x) is not 0 else 1)

    return parser.parse_args()


def main():
    args = parse_arguments()
    async_crawler = AsyncCrawler(args.parent_url, args.number_of_concurrent_requests,
                                 args.download_delay, args.maximum_urls)
    async_crawler.execute_crawler()
    async_crawler.generate_report()


if __name__ == '__main__':
    main()

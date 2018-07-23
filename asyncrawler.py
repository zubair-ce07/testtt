import asyncio
import requests
import argparse
import re

from parsel import Selector
from urllib.parse import urljoin


class AsyncCrawler:

    def __init__(self, start_url, concurrent_requests=1,
                 download_delay=0.0, maximum_urls=0):
        self.start_url = start_url
        self.download_delay = download_delay
        self.maximum_urls = maximum_urls
        self.bounded_semaphore = asyncio.BoundedSemaphore(concurrent_requests)
        self.visited_urls = set()
        self.downloaded_bytes = 0

    async def parse(self, url, event_loop):                                 # Downloads the page size and returns html
        async with self.bounded_semaphore:
            await asyncio.sleep(self.download_delay)
            future_response = event_loop.run_in_executor(None, requests.get, url)
            response = await future_response
            self.downloaded_bytes += len(response.content)
            return response.text

    async def extract_anchor_urls(self, base_url, event_loop):              # Returns a list of urls from the page
        sel = Selector(text=await self.parse(base_url, event_loop))
        return list(map(lambda url: urljoin(base_url, url), sel.css('a::attr(href)').getall()))

    async def extract_multiple_anchor_urls(self, anchor_urls, event_loop):   # Extracts multiple urls asynchronously
        futures = []
        for web_url in anchor_urls:
            if len(self.visited_urls) > self.maximum_urls:
                break
            if web_url not in self.visited_urls:
                self.visited_urls.add(web_url)
                futures.append(asyncio.ensure_future(self.extract_anchor_urls(web_url, event_loop)))

        extracted_urls = await asyncio.gather(*futures)
        return extracted_urls

    async def crawl(self, event_loop):                                      # Recursively calls the Async crawler
        anchor_urls = [self.start_url]
        while len(self.visited_urls) < self.maximum_urls:
            extracted_urls = await self.extract_multiple_anchor_urls(anchor_urls, event_loop)
            anchor_urls = []
            anchor_urls += sum(extracted_urls, [])

    def execute_crawler(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.crawl(loop))
        loop.close()

    def generate_report(self):
        print(f'\nTotal requests: {self.maximum_urls}')
        print(f'Total bytes downloaded: {self.downloaded_bytes}')
        print(f'Average page size: {int(self.downloaded_bytes / len(self.visited_urls))}\n')


def validate_web_url(url):
    regex = re.compile(r'(^https?:\/\/)((www)\.?[^\W]+(.\w+)+)(\/[^\W]*)*', re.IGNORECASE)
    if re.match(regex, url):
        return url
    raise argparse.ArgumentTypeError(f"Invalid url {url}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("start_url", help="url for crawling", type=validate_web_url)
    parser.add_argument("maximum_urls", help="Total urls to visits", type=int)
    parser.add_argument("download_delay", help="Download delay for each worker", type=float)
    parser.add_argument("number_of_concurrent_requests",
                        help="Requests that can be made concurrently",
                        type=lambda no_of_requests: int(no_of_requests) if int(no_of_requests) is not 0 else 1)

    return parser.parse_args()


def main():
    args = parse_arguments()
    async_crawler = AsyncCrawler(args.start_url, args.number_of_concurrent_requests,
                                 args.download_delay, args.maximum_urls)
    async_crawler.execute_crawler()
    async_crawler.generate_report()


if __name__ == '__main__':
    main()

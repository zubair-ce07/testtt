import argparse
import asyncio
import re
import requests

from parsel import Selector
from urllib.parse import urlparse, urljoin


class AsyncCrawler:

    def __init__(self, start_url, max_urls, concurrent_reqs, download_delay):
        self.start_url = start_url
        self.max_urls = max_urls
        self.concurrent_reqs = concurrent_reqs
        self.download_delay = download_delay
        self.bytes_downloaded = 0
        self.bounded_semaphore = asyncio.BoundedSemaphore(concurrent_reqs)
        self.visited_sites = set()

    async def download_page(self, url, loop):
        async with self.bounded_semaphore:
            downloaded_content = None
            try:
                await asyncio.sleep(self.download_delay)
                future_response = loop.run_in_executor(None, requests.get, url)
                downloaded_content = await future_response
            except Exception as error:
                print(error)
            if downloaded_content:
                self.bytes_downloaded += len(downloaded_content.text)
            return downloaded_content.text

    async def get_anchor_urls(self, url, loop):
        filtered_links = []
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        html_selector = Selector(text=await self.download_page(url, loop))
        filtered_links += map(lambda href_links: urljoin(base_url, href_links), html_selector.xpath('//a/@href').getall())
        return filtered_links

    async def extract_collective_urls(self, href_urls, loop):
        future_results = []
        for url in href_urls:
            if len(self.visited_sites) == self.max_urls:
                break
            elif url not in self.visited_sites:
                future_results.append(asyncio.ensure_future(self.get_anchor_urls(url, loop)))
                self.visited_sites.add(url)
        urls_extracted = await asyncio.gather(*future_results)
        return urls_extracted

    async def concurrent_processing(self, loop):
        href_urls = [self.start_url]
        while len(self.visited_sites) < self.max_urls:
            urls_extracted = await self.extract_collective_urls(href_urls, loop)
            for urls in urls_extracted:
                href_urls.extend(urls)

    def execute_async_spider(self):
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.concurrent_processing(event_loop))
        event_loop.close()

    def generate_report(self):
        print(f"Total number of website visits are: {len(self.visited_sites)}")
        print(f"Total bytes downloaded are: {self.bytes_downloaded} Bytes / {self.bytes_downloaded / 1000} Kilobytes")
        print(f"Average size of page is : {self.bytes_downloaded/len(self.visited_sites)} Bytes /"
              f"{(round(self.bytes_downloaded/len(self.visited_sites))/1000)} Kilobytes")


def is_valid_url(url):
    regex = re.compile(r'^(https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}()?(\/.*)?')
    if re.match(regex, url):
        return url
    else:
        raise argparse.ArgumentTypeError('Website is of incorrect format')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_url', type=is_valid_url, help='Enter the starting URL')
    parser.add_argument('max_urls', type=int, help='Enter the maximum number of URLs to be visited')
    parser.add_argument('concurrent_reqs',
                        type=lambda concurrent_reqs: int(concurrent_reqs) if int(concurrent_reqs) > 0 else 1,
                        help='Enter the maximum number of concurrent requests')
    parser.add_argument('download_delay', type=float, help='Enter the maximum download delay for each requests')
    return parser.parse_args()


if __name__ == "__main__":
    input_arguments = parse_arguments()
    async_processing = AsyncCrawler(input_arguments.start_url, input_arguments.max_urls,
                                    input_arguments.concurrent_reqs, input_arguments.download_delay)
    async_processing.execute_async_spider()
    async_processing.generate_report()

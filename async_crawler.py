import argparse
import asyncio
import re
import requests

from parsel import Selector
from statistics import mean
from urllib.parse import urlparse, urljoin


def is_valid_url(url):
    regex = re.compile(r'^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\(\)\*\+,;=.]+$')
    if re.match(regex, url):
        return url
    else:
        exit('Website of incorrect format')


def is_valid_concurrent_req(concurrent_reqs):
    if int(concurrent_reqs) > 0:
        return int(concurrent_reqs)
    else:
        return 1


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_url', type=is_valid_url, help='Enter the starting URL')
    parser.add_argument('max_urls', type=int, help='Enter the maximum number of URLs to be visited')
    parser.add_argument('concurrent_reqs', type=is_valid_concurrent_req,
                        help='Enter the maximum number of concurrent requests')
    parser.add_argument('download_delay', type=float, help='Enter the maximum download delay for each requests')
    return parser.parse_args()


class AsyncCrawler:

    def __init__(self, start_url, max_urls, concurrent_reqs, download_delay):
        self.start_url = start_url
        self.max_urls = max_urls
        self.concurrent_reqs = concurrent_reqs
        self.download_delay = download_delay
        self.site_sizes = []
        self.bounded_semaphore = asyncio.BoundedSemaphore(concurrent_reqs)
        self.visited_sites = set()

    async def download_page(self, url, loop):
        async with self.bounded_semaphore:
            downloaded_content = None
            print(f"Downloading the URL {url}")
            try:
                await asyncio.sleep(self.download_delay)
                future_response = loop.run_in_executor(None, requests.get, url)
                downloaded_content = await future_response
            except Exception as error:
                print(error)
            if downloaded_content:
                self.site_sizes.append(len(downloaded_content.content))
            return downloaded_content.text

    async def get_anchor_urls(self, url, loop):
        filtered_links = []
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        raw_html = await self.download_page(url, loop)
        html_selector = Selector(raw_html)
        href_links = html_selector.xpath('//a/@href').getall()
        for href in href_links:
            filtered_links.append(urljoin(base_url, href))
        return filtered_links

    async def extract_collective_urls(self, url_list, loop):
        future_results = []
        for url in url_list:
            if url not in self.visited_sites and len(self.visited_sites) < self.max_urls:
                future_results.append(asyncio.ensure_future(self.get_anchor_urls(url, loop)))
                self.visited_sites.add(url)
        urls_extracted = await asyncio.gather(*future_results)
        return urls_extracted

    async def concurrent_processing(self, loop):
        url_list = []
        url_list.append(self.start_url)
        while True:
            if len(self.visited_sites) < self.max_urls:
                urls_extracted = await self.extract_collective_urls(url_list, loop)
                for urls in urls_extracted:
                    url_list.extend(urls)
            else:
                break

    def execute_async_spider(self):
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.concurrent_processing(event_loop))
        event_loop.close()

    def generate_report(self):
        print(f"Total number of website visits are: {len(self.site_sizes)}")
        print(f"Total bytes downloaded are: {sum(self.site_sizes)} Bytes / {sum(self.site_sizes) / 1000} Kilobytes")
        print(f"Average size of page is :{round(mean(self.site_sizes), 2)} Bytes/ {round(mean(self.site_sizes) / 1000,2)} Kilobytes")


if __name__ == "__main__":
    input_arguments = parse_arguments()
    async_processing = AsyncCrawler(input_arguments.start_url, input_arguments.max_urls,
                                    input_arguments.concurrent_reqs, input_arguments.download_delay)
    async_processing.execute_async_spider()
    async_processing.generate_report()

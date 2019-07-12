import argparse
import asyncio
import re
import requests

from parsel import Selector
from statistics import mean
from urllib.parse import urlparse, urljoin


def is_valid_url(url):
    http_request = requests.head(url)
    if http_request.status_code == 200:
        return url
    else:
        exit('Website not accessible')


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_url', type=is_valid_url, help='Enter the starting URL')
    parser.add_argument('max_urls', type=int, help='Enter the maximum number of URLs to be visited')
    parser.add_argument('concurrent_reqs', type=int, help='Enter the maximum number of concurrent requests')
    parser.add_argument('download_delay', type=float, help='Enter the maximum download delay for each requests')
    return parser.parse_args()


class AsyncCrawler:

    def __init__(self, start_url, max_urls, concurrent_reqs, download_delay):
        self.start_url = start_url
        self.max_urls = max_urls
        self.concurrent_reqs = concurrent_reqs
        self.download_delay = download_delay
        self.site_sizes = []

    def get_anchor_urls(self, start_url, max_urls):
        parsed_url = urlparse(start_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        raw_html = requests.get(start_url)
        href_links = Selector(raw_html.text).xpath('//a/@href').getall()
        filtered_links = []
        for href in href_links:
            if len(filtered_links) == max_urls:
                break
            else:
                if re.match(r'http', href):
                    filtered_links.append(href)
                elif re.match(r'/', href):
                    filtered_links.append(urljoin(base_url, href))
                else:
                    continue
        return filtered_links

    async def page_download(self, url, download_delay, bounded_semaphore):
        async with bounded_semaphore:
            downloaded_content = None
            print(f"Downloading the URL {url}")
            try:
                downloaded_content = requests.get(url, timeout=1)
                await asyncio.sleep(download_delay)
            except Exception as error:
                print(error)
            if downloaded_content:
                self.site_sizes.append(len(downloaded_content.content))

    async def concurrent_processing(self):
        bounded_semaphore = asyncio.BoundedSemaphore(self.concurrent_reqs)
        url_list = self.get_anchor_urls(self.start_url, self.max_urls)
        futures = [self.page_download(url, self.download_delay, bounded_semaphore) for url in url_list]
        await asyncio.gather(*futures)
        filtered_sizes = [size for size in self.site_sizes if size is not None]
        return filtered_sizes

    def report_generator(self, site_sizes):
        print(f"Total number of website visits are: {len(site_sizes)}")
        print(f"Total bytes downloaded are: {sum(site_sizes)} Bytes / {sum(site_sizes)/1000} Kilobytes")
        print(f"Average size of page is :{round(mean(site_sizes),2)} Bytes/ {round(mean(site_sizes)/1000,2)} Kilobytes")


if __name__ == "__main__":
    input_arguments = arg_parser()
    async_processing = AsyncCrawler(input_arguments.start_url, input_arguments.max_urls,
                                    input_arguments.concurrent_reqs, input_arguments.download_delay)
    loop = asyncio.get_event_loop()
    site_sizes = loop.run_until_complete(async_processing.concurrent_processing())
    loop.close()
    async_processing.report_generator(site_sizes)

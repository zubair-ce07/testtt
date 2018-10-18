import argparse
import asyncio
import requests
import threading
import re
import urllib.request
from parsel import Selector
from urllib.parse import urljoin


class Crawler:
    def __init__(self, download_delay, concurrency, max_urls_limit, start_url):
        self._delay = download_delay
        self._max_urls_limit = max_urls_limit
        self._urls = [start_url]
        self._total_bytes = 0
        self._allowed_domain = start_url
        self._crawled_links = set()
        self.lock = threading.Semaphore(concurrency)

    def crawl(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.ensure_future(self.schedule_requests(loop)))
        self.display_stats()

    async def schedule_requests(self, loop):
        tasks = []
        while self._urls or tasks:
            if not self._urls:
                continue

            if len(self._crawled_links) >= self._max_urls_limit and tasks:
                continue

            if len(self._crawled_links) >= self._max_urls_limit:
                break

            url = self._urls.pop(0)
            if url in self._crawled_links:
                continue

            self._crawled_links.add(url)
            self.lock.acquire()

            task = loop.create_task(self.make_request(url))
            task.add_done_callback(lambda t: self.parse_response(t.result()))
            task.add_done_callback(lambda t: self.lock.release())
            task.add_done_callback(lambda t: tasks.remove(task))
            tasks.append(task)

            await asyncio.sleep(self._delay)

    async def make_request(self, start_url):
        try:
            response = requests.get(start_url)
            return response
        except:
            requests.exceptions.ConnectionError("Link is not responding")

    def parse_response(self, response):
        if response:
            raw_urls = self.extract_urls(response.text)
            urls = self.absolute_urls(response.url, raw_urls)
            filtered_urls = self.filter_urls(urls)
            self.enqueue_urls(filtered_urls)
            self.calculate_bytes(response.text)

    def extract_urls(self, html_text):
        sel = Selector(html_text)
        css = 'a::attr(href)'
        raw_urls = sel.css(css).extract()
        return raw_urls

    def absolute_urls(self, base_url, urls):
        return [urljoin(base_url, url) for url in urls]

    def filter_urls(self, urls):
        return [url for url in urls if self.is_allowed_url(url)]

    def is_allowed_url(self, url):
        return url.startswith(self._allowed_domain)

    def enqueue_urls(self, urls):
        [self._urls.append(url) for url in urls]

    def calculate_bytes(self, html_text):
        self._total_bytes = self._total_bytes + len(html_text)

    def display_stats(self):
        print(f"Total number of requests: {len(self._crawled_links)}")
        print(f"Total number of bytes downloaded: {self._total_bytes}")

        avg_page_size = self._total_bytes / len(self._crawled_links)
        print(f"Average size of a page: {avg_page_size}")


def validate_delay(delay):
    try:
        e = argparse.ArgumentTypeError("Invalid delay")
        delay = int(delay)
        if delay >= 0:
            return delay
        raise e
        
    except e:
        raise e

def validate_max_num(number):
    try:
        e = argparse.ArgumentTypeError("Invalid number")
        number = int(number)
        if number > 0:
            return number
        raise e

    except e:
        raise e

def validate_url(url):
    if re.match(r"^(http(s)?:\/\/)[\w.-]+$", url):
        return urljoin(url, "/")
    raise argparse.ArgumentTypeError("Invalid URL.")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--concurrency", help="Prompt the number of concurrent requests.",
                        type=validate_max_num, required=True)
    parser.add_argument("-d", "--delay", help="Prompt the DOWNLOAD_DELAY for each request.",
                        type=validate_delay, required=True)
    parser.add_argument("-m", "--max", help="Prompt number of maximum urls to visit.",
                        type=validate_max_num, required=True)
    parser.add_argument("-u", "--url", help="Prompt start url to crawl.", 
                        type=validate_url, required=True)
    args = parser.parse_args()

    return args.concurrency, args.delay, args.max, args.url

def main():
    delay, concurrency, max_url_limit, start_url = parse_arguments()
    crawler = Crawler(delay, concurrency, max_url_limit, start_url)
    crawler.crawl()


main()

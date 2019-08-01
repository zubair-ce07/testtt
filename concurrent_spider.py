import asyncio
from urllib.parse import urljoin, urlparse

import requests
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor


class ConcurrentSpider:

    def __init__(self, start_url, max_urls, download_delay, concurrent_requests):
        self.allowed_domain = urlparse(start_url).netloc
        self.urls_limit = max_urls
        self.download_delay = download_delay
        self.bounded_semaphore = asyncio.BoundedSemaphore(concurrent_requests)
        self.visited_urls = []
        self.queued_urls = {start_url}
        self.downloaded_bytes = 0
        self.event_loop = asyncio.get_event_loop()

    @staticmethod
    def extract_links(response):
        return Selector(response.text).css('a::attr(href)').extract()

    @staticmethod
    def make_link_absolute(base_url, url):
        return urljoin(base_url, url)

    def filter_links(self, links):
        return {link for link in links if self.validate_link(link)}

    def validate_link(self, link):
        return link not in self.visited_urls and self.allowed_domain == urlparse(link).netloc

    def parse_response(self, response):
        links = self.extract_links(response)
        absolute_links = [self.make_link_absolute(response.url, link) for link in links]
        self.queued_urls.update(self.filter_links(absolute_links))

    async def make_request(self, url):
        async with self.bounded_semaphore:
            self.parse_response(requests.get(url))
            html = requests.get(url).text
            length = len(html)
            self.downloaded_bytes += length

    async def schedule_requests(self):
        while self.queued_urls:
            print(f'VISITED-> {self.visited_urls}')
            if len(self.visited_urls) == self.urls_limit:
                break
            if not self.queued_urls:
                continue
            url = self.queued_urls.pop()
            if url in self.visited_urls:
                continue
            self.visited_urls.append(url)
            await self.make_request(url)
            await asyncio.sleep(self.download_delay)

    def crawl(self):
        try:
            self.event_loop.run_until_complete(self.schedule_requests())
        finally:
            self.event_loop.close()

    def print_results(self):
        print(f'Number of Requests Made: {len(self.visited_urls)}')
        print(f'Total Downloaded Bytes: {self.downloaded_bytes}')
        print(f'Average Page Size: {self.downloaded_bytes//len(self.visited_urls)}')

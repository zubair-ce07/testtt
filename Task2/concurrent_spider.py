import concurrent.futures
import asyncio
import time

from urllib.parse import urljoin, urlparse
from parsel import Selector
import requests


class ConcurrentSpider:
    def __init__(self, site_url, download_delay, concurrency):
        self.download_delay = download_delay
        self.allowed_domain = urlparse(site_url).netloc
        self.__tasks_limiting_semaphore = asyncio.BoundedSemaphore(concurrency)

        self.start_time = None
        self.bytes_downloaded = 0
        self.visited_urls = []
        self.__loop = asyncio.get_event_loop()
        self.__executor = concurrent.futures.ThreadPoolExecutor()

    def run(self, urls_limit, url):
        self.start_time = time.time()
        self.__loop.run_until_complete(self.schedule_requests([self.normalize_url(url)], urls_limit))

    async def schedule_requests(self, urls, limit):
        if len(self.visited_urls) < limit and urls:
            urls = urls[:limit-len(self.visited_urls)] if len(urls) > limit-len(self.visited_urls) else urls
            self.visited_urls.extend(urls)

            for request in await self.visit_urls(urls):
                response = await request
                await self.schedule_requests(self.parse_response(response), limit)

    async def visit_urls(self, urls):
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(self.make_request(url)))
            await asyncio.sleep(self.download_delay)
        return asyncio.as_completed(tasks)

    async def make_request(self, url):
        async with self.__tasks_limiting_semaphore:
            task = asyncio.ensure_future(self.__loop.run_in_executor(self.__executor, requests.get, url))
            response = await asyncio.wait_for(task, None)
            self.bytes_downloaded += len(response.text)
        return response

    def parse_response(self, response):
        links = self.extract_links(response)
        absolute_urls = {self.make_absolute_url(self.normalize_url(link)) for link in links}
        return self.filter_urls(absolute_urls)

    def extract_links(self, response):
        return Selector(response.text).css('a::attr(href)').extract()

    def make_absolute_url(self, link):
        return urljoin(f"http://{self.allowed_domain}", link)

    def normalize_url(self, url):
        return url.strip().strip("/")

    def filter_urls(self, urls):
        return [url for url in urls if self.validate_url(url)]

    def validate_url(self, url):
        return url not in self.visited_urls and self.allowed_domain == urlparse(url).netloc

    def print_stats(self):
        print(f"\nTotal Requests: {len(self.visited_urls)}\nBytes Downloaded: {self.bytes_downloaded}\n"
              f"Size Per Page:{self.bytes_downloaded/len(self.visited_urls)}\n"
              f"Execution Time: {time.time()-self.start_time}")

import asyncio
from urllib.parse import urlparse
from time import time
import queue

import aiohttp
from parsel import Selector


SUCCESS_RESPONSE_CODE = 200

class CrawlWorker:

    def __init__(self, crawl_limit, max_current_requests, download_delay, start_url, loop):
        self.crawl_limit = crawl_limit
        self.max_current_requests = max_current_requests
        self.download_delay = download_delay
        self.loop = loop
        self.url_queue = queue.Queue()
        url = urlparse(start_url)
        self.url_queue.put(url)
        self.allowed_domain = url.netloc
        self.visisted_urls = []
        self.pages_visisted = 0
        self.total_bytes_downloaded = 0
        self.cuncurrent_task_lock = asyncio.Semaphore(value=self.max_current_requests)

    async def start_crawling(self):
        crawl_workers = set()
        start_time = time()
        while self.pages_visisted < self.crawl_limit:
            await self.cuncurrent_task_lock.acquire()
            await asyncio.sleep(self.download_delay)
            crawl_workers.add(self.loop.create_task(self.__create_request(self.cuncurrent_task_lock)))

        self.print_result(start_time)
        await asyncio.wait(crawl_workers)

    def print_result(self, start_time):

        total_bytes_downloaded = self.total_bytes_downloaded
        total_pages_loaded = self.pages_visisted
        avg_page_size = total_bytes_downloaded / total_pages_loaded

        print(f"\nTotal pages loaded: {total_pages_loaded}")
        print(f"Total bytes downloaded: {total_bytes_downloaded}")
        print(f"Average page size: {avg_page_size}")
        print(f"Total time taken: {(time() - start_time)}")

    async def __create_request(self, cuncurrent_task_lock):
        await self.__crawl_request()
        try:
            await cuncurrent_task_lock.release()
        except TypeError:
            pass

    def __is_valid_url(self, url):
        if url and (url.netloc == self.allowed_domain):
            return url.geturl() not in self.visisted_urls

    async def __handle_response(self, response):
        self.pages_visisted += 1
        self.total_bytes_downloaded += len(response)
        selector = Selector(response)
        href_links = selector.xpath('//a/@href').getall()
        for link in href_links:
            new_url = urlparse(link)
            if self.__is_valid_url(new_url):
                self.url_queue.put(new_url)

    def __is_request_allowed(self):
        return self.url_queue.qsize() and self.pages_visisted < self.crawl_limit

    async def __crawl_request(self):
        if not self.__is_request_allowed():
            return
        raw_url = self.url_queue.get()
        self.url_queue.task_done()
        url = raw_url.geturl()
        print(f"Loading URL: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == SUCCESS_RESPONSE_CODE:
                    response = await resp.text()
                    await self.__handle_response(response)

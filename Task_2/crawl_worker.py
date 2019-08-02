import asyncio
from urllib.parse import urlparse
from time import time
import queue

import aiohttp
from parsel import Selector


SUCCESS_RESPONSE_CODE = 200

class CrawlWorker:

    def __init__(self, total_pages_to_load, cuncurrent_request_allowed, \
        download_delay, first_url, loop):
        self.total_pages_to_load = total_pages_to_load
        self.cuncurrent_request_allowed = cuncurrent_request_allowed
        self.download_delay = download_delay
        self.loop = loop
        self.url_queue = queue.Queue()
        url = urlparse(first_url)
        self.url_queue.put(url)
        self.visiting_domain = url.netloc
        self.already_visisted_urls = []
        self.total_urls_requested = 0
        self.page_loaded_successfully = 0
        self.total_bytes_downloaded = 0

    async def start_crawling(self):
        crawl_workers = set()
        cuncurrent_task_lock = asyncio.Semaphore(
            value=self.cuncurrent_request_allowed
        )
        start_time = time()
        while self.page_loaded_successfully < self.total_pages_to_load:
            await cuncurrent_task_lock.acquire()
            await asyncio.sleep(self.download_delay)
            crawl_workers.add(self.loop.create_task(self.__create_request(cuncurrent_task_lock)))

        await asyncio.wait(crawl_workers)
        self.__print_result(start_time)

    def __print_result(self, start_time):

        total_bytes_downloaded = self.total_bytes_downloaded
        total_pages_loaded = self.page_loaded_successfully
        avg_page_size = total_bytes_downloaded / total_pages_loaded

        print(f"\nTotal pages loaded: {total_pages_loaded}")
        print(f"Total bytes downloaded: {total_bytes_downloaded}")
        print(f"Average page size: {avg_page_size}")
        print("Total time taken: %s" % (time() - start_time))

    async def __create_request(self, cuncurrent_task_lock):
        await self.__crawl_request()
        try:
            await cuncurrent_task_lock.release()
        except TypeError:
            pass

    def __is_valid_url(self, url):
        return (not url.geturl() in self.already_visisted_urls) \
            and (url.netloc == self.visiting_domain) \
            and url

    async def __handle_response(self, response):
        self.page_loaded_successfully += 1
        self.total_bytes_downloaded += len(response)
        selector = Selector(response)
        href_links = selector.xpath('//a/@href').getall()
        for link in href_links:
            new_url = urlparse(link)
            if self.__is_valid_url(new_url):
                self.url_queue.put(new_url)

    def __is_request_allowed(self):
        return (self.url_queue.qsize() != 0) and \
            (self.total_urls_requested < self.total_pages_to_load)

    async def __crawl_request(self):
        if not self.__is_request_allowed():
            return
        self.total_urls_requested += 1
        raw_url = self.url_queue.get()
        self.url_queue.task_done()
        if not self.visiting_domain:
            self.visiting_domain = raw_url.netloc
        url = raw_url.geturl()
        print(f"Loading URL: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == SUCCESS_RESPONSE_CODE:
                    response = await resp.text()
                    await self.__handle_response(response)
                else:
                    self.total_urls_requested -= 1

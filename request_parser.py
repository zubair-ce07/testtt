import asyncio
import argparse
import queue
import requests
import sys
import time
import threading
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
from parsel import Selector


PageDetails = namedtuple('Page', ('page_url', 'page_size'))


class RequestParser():

    def __init__(self, base_url, url_limit, req_limit, download_delay):
        self.url_limit = url_limit
        self.base_url = base_url
        self.download_delay = download_delay
        self.number_of_requests = req_limit
        self.traversed_pages = []
        self.url_queue = queue.PriorityQueue()

    async def read_url(self, url):
        request = requests.get(url)
        selector = Selector(request.text)
        page_urls = list(set(selector.css(f'a[href^="{self.base_url}"]::attr(href)').extract()))
        self.traversed_pages += [PageDetails(url, len(request.content))]
        for value in page_urls:
            self.url_queue.put(value)
        await asyncio.sleep(self.download_delay)

    def iterative_concurrent_crawl(self):
        self.url_queue.queue.clear()
        self.url_queue.put(self.base_url)
        loop = asyncio.get_event_loop()

        while (not self.url_queue.empty() and len(self.traversed_pages) < self.url_limit):
            url = self.url_queue.get()
            if any(value == url for value in [value.page_url for value in self.traversed_pages]):
                continue
            loop.run_until_complete(self.read_url(url))
        loop.close()

    def recursive_concurent_crawler(self):
        self.traversed_pages = []
        loop = asyncio.get_event_loop()
        traversed_url = loop.run_until_complete(self.crawl_conccurently(self.base_url))
        loop.close()

    def recursive_parallel_crawler(self):
        self.traversed_pages = []
        traversed_url = self.crawl_parallel(self.base_url)

    async def crawl_conccurently(self, base_url):
        if len(self.traversed_pages) >= self.url_limit:
            return
        request = requests.get(base_url)
        selector = Selector(request.text)
        page_urls = selector.css(f'a[href^="{self.base_url}"]::attr(href)').extract()
        self.traversed_pages += [PageDetails(base_url, len(request.content))]
        for url in page_urls:
            if any(value == url for value in [value.page_url for value in self.traversed_pages]):
                continue
            await self.crawl_conccurently(url)
        await asyncio.sleep(self.download_delay)

    def crawl_parallel(self, base_url):
        if len(self.traversed_pages) >= self.url_limit:
            return
        request = requests.get(base_url)
        self.traversed_pages += [PageDetails(base_url, len(request.content))]
        executor = ThreadPoolExecutor(max_workers=self.number_of_requests)
        selector = Selector(request.text)
        page_urls = selector.css(f'a[href^="{self.base_url}"]::attr(href)').extract()
        for url in page_urls:
            if any(value == url for value in [value.page_url for value in self.traversed_pages]):
                continue
            future = executor.submit(self.crawl_parallel, url)
        return future.result()

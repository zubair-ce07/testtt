import asyncio
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

import requests
from parsel import Selector


class UrlExtractor:
    """
    Class for downloading each page concurrently as well
    as parallel by using asyncio and ThreadPoolExecutor
    """

    def __init__(self, url, total_urls, r_delay, total_requests, crawler_type):
        self.web_text = self.download_page(url).text
        self.urls = self.extract_urls(total_urls, self.web_text)
        self.total_urls = total_urls
        self.delay = r_delay
        self.requests = total_requests
        self.crawler_type = crawler_type

    def processing(self):
        """Function for checking the type of crawling and executing it"""
        loop = asyncio.get_event_loop()
        if self.crawler_type in ['c', 'C']:
            details = loop.run_until_complete(self.run_concurrent())
        elif self.crawler_type in ['p', 'P']:
            details = loop.run_until_complete(self.parallel_crawler(self.urls))
        else:
            print("Invalid crawler type: ", self.crawler_type)
            sys.exit()
        loop.close()
        return details

    def download_page(self, url):
        """Geting the response by requesting any particular url"""
        try:
            response = requests.get(url)
            print("Downloded: ", url)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            sys.exit()

        return response

    def extract_urls(self, url_count, web_text):
        """
        Function uses parsel library (Selectors) for getting
        urls form the web text
        """
        sel = Selector(text=web_text)
        result = sel.xpath('//a[contains(@href, url)]').re(r'http[s]?://(?:[a-zA-Z]|[0-9]\
            |[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

        return result[:url_count]

    async def run_concurrent(self):
        """Async main function for concurrent crawler"""
        details = []
        for url in self.urls:
            details.append(asyncio.ensure_future(self.concurent_crawler(url)))

        await asyncio.gather(*details)
        return details

    @asyncio.coroutine
    async def concurent_crawler(self, url):
        """Coroutine for concurrent crawler"""
        await asyncio.sleep(self.delay)
        request = self.download_page(url)
        return request

    @asyncio.coroutine
    async def parallel_crawler(self, urls):
        """Coroutine for parallel crawler"""
        thread_pool = ThreadPoolExecutor(self.requests)
        futures = []
        for url in self.urls:
            await asyncio.sleep(self.delay)
            futures.append(thread_pool.submit(
                self.download_page, url))
        return futures

    def print_urls(self):
        """Prints the desired number of urls"""
        for i, url in self.urls:
            print(i+1 + " ", url)

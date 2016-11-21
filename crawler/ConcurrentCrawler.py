# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 14:16:37 2016

@author: fatah
"""
import asyncio
import requests
from parsel import Selector


class ConcurrentCrawler:

    def __init__(self, max_workers, download_delay, max_urls):
        self.max_workers = max_workers
        self.download_delay = download_delay
        self.url_limit = max_urls
        self.queue = []  # Queue for storing URLs to be visited
        self.visited = []
        self.byte_count = 0

    def start_crawl(self, start_url):
        self.queue.append(start_url)
        while len(self.visited) < self.url_limit and self.queue:

            allowed = self.url_limit - len(self.visited) \
                if self.url_limit > len(self.visited) \
                else None
            selected = self.queue[:allowed] if allowed else None
            selected = selected[:self.max_workers]
            tasks = [asyncio.ensure_future(self.visit(url)) for url in selected]

            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.gather(*tasks))

            results = [task.result() for task in tasks]
            for result in results:
                self.byte_count += result.get('bytes')
                self.queue.extend(result.get('links'))

            self.visited.extend(self.queue[:len(selected)])
            self.queue = self.queue[len(tasks):]  # Update the queue

    async def visit(self, url):
        await asyncio.sleep(self.download_delay)
        res = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
        byte_count = len(res.content)  # Number of bytes downloaded
        links = Selector(text=res.text).xpath('.//a/@href').re(r'^(/.+)')
        links = [res.url[:-1] + url for url in links]  # Prepend links with base url
        return {'bytes': byte_count, 'links': links}

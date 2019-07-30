import asyncio
from concurrent.futures import ThreadPoolExecutor

import requests
import validators
from parsel import Selector


class ConcurrentCrawler:
    def __init__(self, num_workers, max_urls_to_visit, delay):
        """Initialize attributes and setup asyncio's loop"""
        self.num_workers = num_workers
        self.max_urls_to_visit = max_urls_to_visit
        self.delay = delay
        self.visited_urls = set()
        self.loop = asyncio.get_event_loop()
        self.to_be_visited = asyncio.Queue(loop=self.loop)
        self.downloaded_bytes = 0

    async def _worker(self, id_):
        """Scraps links from URLs until poisoned by a None"""
        print(f"Worker {id_} booting up..")

        while True:
            asyncio.sleep(self.delay)
            url = await self.to_be_visited.get()
            if url is None:
                print(f"Worker {id_} shutting down..")
                self.to_be_visited.task_done()
                break

            print(f"Worker {id_} quering to {url}")

            # running synchronous function in asynchronous fashion
            response = await self.loop.run_in_executor(ThreadPoolExecutor(),
                                                       requests.get, url)

            print(f"Worker {id_} completed query to {url}")

            self.downloaded_bytes += len(response.content)

            urls = self._extract_links(str(response.content))

            for url in urls:
                if len(self.visited_urls) < self.max_urls_to_visit:
                    await self._append_to_queue(url)
                else:
                    await self._poison_all_workers()

            self.to_be_visited.task_done()

    def _extract_links(self, content):
        """Extract links from page"""
        sel = Selector(text=str(content))
        return sel.css('a').xpath('@href').getall()

    async def _poison_all_workers(self):
        """Signal all workers to exit"""
        for _ in range(self.num_workers):
            await self.to_be_visited.put(None)

    async def _append_to_queue(self, url):
        """Add to to_be_visited queue if valid and not already visited"""
        if url not in self.visited_urls and validators.url(url):
            self.visited_urls.add(url)
            await self.to_be_visited.put(url)

    def _report_stats(self):
        """Print crawling statistics to console"""

        stats = f"\nTotal bytes downloaded: {self.downloaded_bytes}\n" \
                f"Total requests made: {self.max_urls_to_visit}\n" \
                f"Average size of pages in kBs: {self.downloaded_bytes/(self.max_urls_to_visit*1000)}\n"
        print(stats)

    def crawl(self, url):
        """Initialize workers to start crawling"""
        self.loop.run_until_complete(self._append_to_queue(url))
        workers = [self.loop.create_task(self._worker(id_))
                   for id_ in range(self.num_workers)]
        self.loop.run_until_complete(asyncio.gather(*workers))
        self.loop.close()
        self._report_stats()

import os
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import requests
import validators
from parsel import Selector


class ParallelCrawler:
    def __init__(self, num_workers, max_urls_to_visit, delay):
        """Initialize attributes and setup shared queue"""
        self.num_workers = num_workers
        self.max_urls_to_visit = max_urls_to_visit
        self.delay = delay
        self.visited_urls = set()
        self.to_be_visited = mp.Manager().Queue()

    def _worker(self):
        """Scraps links from URLs until poisoned by a None"""
        id_ = os.getpid()
        print(f"Worker {id_} booting up..")

        downloaded_bytes = 0

        while True:
            time.sleep(self.delay)
            url = self.to_be_visited.get()
            if url is None:
                print(f"Worker {id_} shutting down..")
                self.to_be_visited.task_done()
                break

            print(f"Worker {id_} quering to {url}")

            response = requests.get(url)

            print(f"Worker {id_} completed query to {url}")

            downloaded_bytes += len(response.content)

            urls = self._extract_links(str(response.content))

            for url in urls:
                if len(self.visited_urls) < self.max_urls_to_visit:
                    self._append_to_queue(url)
                else:
                    self._poison_all_workers()

            self.to_be_visited.task_done()

            return downloaded_bytes

    def _extract_links(self, content):
        """Extract links from page"""
        sel = Selector(text=str(content))
        return sel.css('a').xpath('@href').getall()

    def _poison_all_workers(self):
        """Signal all workers to exit"""
        for _ in range(self.num_workers):
            self.to_be_visited.put(None)

    def _append_to_queue(self, url):
        """Add to to_be_visited queue if valid and not already visited"""
        if url not in self.visited_urls and validators.url(url):
            self.visited_urls.add(url)
            self.to_be_visited.put(url)

    def _report_stats(self, downloaded_bytes):
        """Print crawling statistics to console"""

        stats = f"\nTotal bytes downloaded: {downloaded_bytes}\n" \
                f"Total requests made: {self.max_urls_to_visit}\n" \
                f"Average size of pages in kBs: {downloaded_bytes/(self.max_urls_to_visit*1000)}\n"
        print(stats)

    def crawl(self, url):
        """Initialize workers to start crawling"""
        self._append_to_queue(url)
        futures = []
        with ProcessPoolExecutor() as executor:
            for _ in range(self.num_workers):
                future = executor.submit(self._worker)
                futures.append(future)

            downloaded_bytes = 0
            for f in futures:
                downloaded_bytes += f.result()

        self._report_stats(downloaded_bytes)

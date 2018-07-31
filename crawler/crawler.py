import asyncio
from time import time
from urllib.parse import urlparse, urljoin

import requests
from parsel import Selector


class Crawler:
    def __init__(self, start_url, max_visits_limit, concurrency, download_delay):
        self.ts = time()
        self.queued_urls = [start_url]
        self.visited_urls = set()
        self.total_downloaded_bytes = 0
        self.max_visits_limit = max_visits_limit
        self.concurrency_lock = asyncio.Semaphore(concurrency)
        self.download_delay = download_delay
        self.allowed_domain = urlparse(start_url).netloc
        self.event_loop = asyncio.get_event_loop()
        self.pending_tasks = []

    def run(self):
        try:
            self.event_loop.run_until_complete(self.schedule_requests())
        finally:
            self.event_loop.close()
        self.print_report()

    async def schedule_requests(self):
        while self.queued_urls or self.pending_tasks:
            if len(self.visited_urls) >= self.max_visits_limit:
                break

            if not self.queued_urls:
                continue

            url = self.queued_urls.pop()
            if url in self.visited_urls:
                continue

            self.visited_urls.add(url)
            await self.concurrency_lock.acquire()
            task = self.event_loop.run_in_executor(None, self.parse_response, url)
            task.add_done_callback(lambda _: self.concurrency_lock.release())
            task.add_done_callback(lambda f: self.pending_tasks.remove(f))
            self.pending_tasks.append(task)
            await asyncio.sleep(self.download_delay)
        await asyncio.wait(self.pending_tasks, return_when='ALL_COMPLETED')

    def parse_response(self, url):
        response = requests.get(url)

        self.total_downloaded_bytes += len(response.text)
        urls = self.extract_urls(response)
        absolute_urls = [self.absolute_url(url, u) for u in urls]
        self.queued_urls.extend(self.filter_urls(absolute_urls))

        print(f"done crawling: {url}")

    def print_report(self):
        print('Took seconds to complete:', int(time() - self.ts))
        print('Total data downloaded in kBs:', self.total_downloaded_bytes / 1024)
        no_of_requests_made = len(self.visited_urls)
        print('Number of requests made:', no_of_requests_made)
        if no_of_requests_made:
            print('Average page size in kBs:',
                  self.total_downloaded_bytes // (1024 * no_of_requests_made))

    @staticmethod
    def extract_urls(response):
        selector = Selector(text=response.text)
        return selector.xpath('//a[contains(@href, "/")]/@href').getall()

    @staticmethod
    def absolute_url(base_url, url):
        return urljoin(base_url, url)

    def filter_urls(self, urls):
        return [url for url in urls if self.allowed_domain in urlparse(url).netloc]

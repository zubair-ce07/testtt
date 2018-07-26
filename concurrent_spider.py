import enum
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from urllib.parse import urljoin

import requests
from parsel import Selector


class URLVisitLimit(enum.IntEnum):
    UNLIMITED = -1


class ConcurrentSpider:
    def __init__(self, base_url, concurrent_connections, download_delay, max_url_limit):
        self.base_url = base_url
        self.concurrent_connections = concurrent_connections
        self.download_delay = download_delay
        self.max_url_limit = max_url_limit

        self.response_lock = threading.Lock()
        self.scheduler_lock = threading.Semaphore(value=self.concurrent_connections)

        self.urls_queue = deque([])
        self.seen_urls = []

        self.bytes_downloaded = 0
        self.executor = ThreadPoolExecutor()
        self.workers = []

    def run(self):
        self.urls_queue.append(self.normalize_url(self.base_url))
        self.request_scheduler()

    @property
    def is_url_limit_exceeded(self):
        return self.max_url_limit != URLVisitLimit.UNLIMITED.value \
               and len(self.seen_urls) >= self.max_url_limit

    @property
    def is_worker_active(self):
        return any(w.running() for w in self.workers)

    def request_scheduler(self):
        while self.is_worker_active or self.urls_queue:
            if self.is_url_limit_exceeded:
                return

            if not self.urls_queue:
                continue

            url = self.urls_queue.popleft()

            if self.is_visited_url(url):
                continue

            self.seen_urls.append(url)

            self.scheduler_lock.acquire()
            print(f"> {url}")
            self.workers.append(self.executor.submit(self.crawl, url))
            sleep(self.download_delay)

    def crawl(self, url):
        response = self.send_request(url)

        with self.response_lock:
            self.bytes_downloaded += len(response.text.encode('utf-8'))

        self.process_response(response)

    def process_response(self, response):
        urls = self.extract_urls(response)
        filtered_urls = self.filter_urls(
            [self.normalize_url(self.absolute_url(url)) for url in urls])
        self.enqueue_urls(filtered_urls)
        self.scheduler_lock.release()

    @staticmethod
    def normalize_url(url):
        return url.split('#')[0].replace('/?', '?').rstrip('/')

    @staticmethod
    def send_request(url):
        return requests.get(url)

    @staticmethod
    def extract_urls(response):
        selector = Selector(text=response.text)
        return selector.xpath('//a/@href').getall()

    def absolute_url(self, url):
        return urljoin(self.base_url, url.strip())

    def is_visited_url(self, url):
        return url in self.seen_urls

    def filter_urls(self, urls):
        return {url for url in urls if self.base_url in url}

    def enqueue_urls(self, filtered_urls):
            self.urls_queue.extend(filtered_urls)

    def print_summary(self):
        total_requests_count = len(self.seen_urls)
        average_response_size = self.bytes_downloaded / total_requests_count

        print(f"\nA total of {total_requests_count} requests were made")
        print(f"A total of {self.bytes_downloaded} bytes were downloaded")
        print(f"The average size of pages was {average_response_size} bytes")

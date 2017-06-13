import argparse
import asyncio
import threading
from asyncio.tasks import FIRST_COMPLETED
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue
from urllib import parse

import aiohttp
import requests
import time
from parsel import Selector


class Crawler:
    def __init__(self, base_url, delay, concurrent_requests, max_urls):
        self.base_url = base_url
        self.download_delay = delay
        self.concurrent_requests_count = concurrent_requests
        self.max_urls_to_visit = max_urls
        self.active_requests = []
        self.extracted_urls = []
        self.visited_urls = []
        self.downloaded_bytes = 0
        self.extracted_urls.append(base_url)
        self.visited_urls.append(self.base_url)

    def count_downloaded_bytes(self, html):
        self.downloaded_bytes += len(html)

    def extract_urls_from_html(self, html):
        selector = Selector(text=html)
        for relative_url in selector.xpath('//a/@href').extract():
            if len(self.extracted_urls) == self.max_urls_to_visit:
                break

            if relative_url.startswith('/'):
                relative_url = relative_url[1:]

            if 'http' not in relative_url:
                absolute_url = parse.urljoin(self.base_url, relative_url)
                if self.is_absolute_url(absolute_url) and absolute_url not in self.visited_urls:
                    self.extracted_urls.append(absolute_url)

    def is_absolute_url(self, url):
        return bool(parse.urlparse(url).netloc)

    def show_performance(self, crawling_approach):
        print('Crawling through {}'.format(crawling_approach))
        print('Visited pages: {}'.format(len(self.visited_urls)))
        print('Downloaded Bytes: {}'.format(self.downloaded_bytes))
        print('Average size of a page {0:.2f}\n\n'.format(self.downloaded_bytes / len(self.visited_urls)))


class AsyncCrawler(Crawler):
    async def crawling(self, url, request_count):
        print('request {}'.format(request_count))
        async with aiohttp.request('Get', url) as response:
            html = await response.text()
            self.count_downloaded_bytes(html)
            self.extract_urls_from_html(html)

    async def ensure_concurrency(self):
        await self.crawling(self.base_url, 1)
        requesting_url_index = 1
        while True:
            active_task_count = len([task for task in asyncio.Task.all_tasks() if not task.done()])
            requests_count = self.concurrent_requests_count - active_task_count
            print('Active tasks count: {} New requests will be {}'.format(active_task_count,
                                                                          requests_count))
            if len(self.visited_urls) == self.max_urls_to_visit:
                break

            if requests_count:
                for _ in range(requests_count):
                    await self.schedule_new_request(requesting_url_index)
                    requesting_url_index += 1
                await asyncio.wait(self.active_requests, return_when=FIRST_COMPLETED)
                print('visited_urls: {}\n'.format(len(self.visited_urls)))
            else:
                print('wait for proceeding previous requests\n')
                await asyncio.sleep(self.download_delay)

        while active_task_count > 1:
            print('{} tasks are pending. Wait to complete these tasks\n'.format(active_task_count))
            await asyncio.sleep(self.download_delay)
            active_task_count = len([task for task in asyncio.Task.all_tasks() if not task.done()])

    async def schedule_new_request(self, requesting_url_index):
        if requesting_url_index < len(self.extracted_urls):
            url = self.extracted_urls[requesting_url_index]
            self.visited_urls.append(url)
            task = asyncio.ensure_future(self.crawling(url, requesting_url_index + 1))
            await asyncio.sleep(self.download_delay)
            self.active_requests.append(task)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ensure_concurrency())
        loop.close()


class ParallelCrawler(Crawler):
    def crawling(self, url, request_count=1):
        lock.acquire()
        print('request {}, active requests {}'.format(request_count, threading.active_count()))
        html = requests.get(url).text
        self.count_downloaded_bytes(html)
        self.extract_urls_from_html(html)
        lock.release()

    def ensure_parallelism(self):
        # It ensures number of parallel request by collecting specified number of urls and pass these
        # urls to ThreadPoolExecutor for crawling
        requesting_url_index = 1
        active_request_count = Queue(maxsize=self.concurrent_requests_count)
        while requesting_url_index <= self.concurrent_requests_count:
            active_request_count.put(self.extracted_urls[requesting_url_index])
            self.visited_urls.append(self.extracted_urls[requesting_url_index])
            requesting_url_index += 1

        with ThreadPoolExecutor(max_workers=self.concurrent_requests_count) as executor:
            request_count = 1
            while not active_request_count.empty():
                url = active_request_count.get()
                request_count += 1
                self.active_requests.append(executor.submit(self.crawling, url, request_count))
                time.sleep(self.download_delay)
                if requesting_url_index < len(self.extracted_urls):
                    active_request_count.put(self.extracted_urls[requesting_url_index])
                    self.visited_urls.append(self.extracted_urls[requesting_url_index])
                    requesting_url_index += 1
            executor.map(self.active_requests)

    def start(self):
        self.crawling(self.base_url)
        self.ensure_parallelism()


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--crawling_approach', type=validate_crawling_approach,
                        help='Enter c for concurrent crawling or p for parallel crawling')
    parser.add_argument('-u', '--url', type=validate_url, help='Enter any website url')
    parser.add_argument('-d', '--download_delay', type=validate_float_value,
                        help='Specify download delay')
    parser.add_argument('-r', '--concurrent_request_count', type=validate_int_value,
                        help='Specify number of concurrent requests')
    parser.add_argument('-m', '--max_urls_to_visit', type=validate_int_value,
                        help='Specify the maximum number of urls should be visited')
    arguments = parser.parse_args()
    if not arguments.crawling_approach:
        arguments.crawling_approach = 'c'
    if not arguments.url:
        arguments.url = 'https://www.tutorialspoint.com/'
    if not arguments.concurrent_request_count:
        arguments.concurrent_request_count = 5
    if not arguments.download_delay:
        arguments.download_delay = 0
    if not arguments.max_urls_to_visit:
        arguments.max_urls_to_visit = 20
    return arguments


def validate_crawling_approach(crawling_approach):
    if len(crawling_approach) == 1 and ('c' in crawling_approach or 'p' in crawling_approach):
        return crawling_approach
    else:
        raise argparse.ArgumentTypeError(
            'Please enter c for concurrent crawling or p for parallel crawling')


def validate_url(url):
    if bool(parse.urlparse(url).netloc):
        if not url.endswith('/'):
            url += '/'
        return url
    else:
        raise argparse.ArgumentTypeError('Please enter a valid url')


def validate_float_value(number):
    try:
        return float(number)
    except:
        raise argparse.ArgumentTypeError('Please enter a valid floating point value')


def validate_int_value(number):
    try:
        return int(number)
    except:
        raise argparse.ArgumentTypeError('Please enter a valid integer value')


if __name__ == '__main__':
    args = get_arguments()
    if 'c' in args.crawling_approach:
        async_crawler = AsyncCrawler(
            args.url, args.download_delay, args.concurrent_request_count, args.max_urls_to_visit)
        async_crawler.start()
        async_crawler.show_performance('Asynchronous')
    else:
        lock = threading.Lock()
        parallel_crawler = ParallelCrawler(
            args.url, args.download_delay, args.concurrent_request_count, args.max_urls_to_visit)
        parallel_crawler.start()
        parallel_crawler.show_performance('Parallel')

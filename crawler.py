import argparse
import asyncio
import threading
import time
from asyncio.tasks import FIRST_COMPLETED
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin

import aiohttp
import requests
from parsel import Selector


class Crawler:
    def __init__(self, base_url, delay, concurrent_requests, max_urls):
        self.base_url = base_url
        self.download_delay = delay
        self.concurrent_requests_count = concurrent_requests
        self.max_urls_to_visit = max_urls
        self.active_requests = []
        self.extracted_urls = [base_url]
        self.visited_urls = [base_url]
        self.downloaded_bytes = 0

    def count_downloaded_bytes(self, response):
        self.downloaded_bytes += len(response)

    def extract_urls_from_response(self, response):
        selector = Selector(text=response)
        for relative_url in selector.xpath('//a/@href').extract():
            if len(self.extracted_urls) == self.max_urls_to_visit:
                break

            if 'http' not in relative_url:
                absolute_url = urljoin(self.base_url, relative_url)
                if bool(urlparse(absolute_url).netloc)\
                        and absolute_url not in self.visited_urls:
                    self.extracted_urls.append(absolute_url)

    def show_performance(self, crawling_approach):
        print('Crawling through {}'.format(crawling_approach))
        print('Visited pages: {}'.format(len(self.visited_urls)))
        print('Downloaded Bytes: {}'.format(self.downloaded_bytes))
        print('Average size of a page {0:.2f}\n\n'.
              format(self.downloaded_bytes / len(self.visited_urls)))


class AsyncCrawler(Crawler):
    async def crawling(self, url):
        async with aiohttp.request('Get', url) as response:
            response = await response.text()
            self.count_downloaded_bytes(response)
            self.extract_urls_from_response(response)

    async def ensure_concurrency(self):
        print('request {}'.format(1))
        await self.crawling(self.base_url)
        completed_request_count = 1
        while True:
            if len(self.visited_urls) == self.max_urls_to_visit:
                break
            active_task_count = len([task for task in self.active_requests if not task.done()])
            new_requests_count = self.concurrent_requests_count - active_task_count
            if new_requests_count:
                print('Active tasks count: {} New requests will be {}'.
                      format(active_task_count, new_requests_count))
                for _ in range(new_requests_count):
                    await asyncio.sleep(self.download_delay)
                    if completed_request_count < len(self.extracted_urls):
                        print('request {}'.format(completed_request_count + 1))
                        await self.schedule_new_request(completed_request_count)
                        completed_request_count += 1

                self.active_requests = [task for task in self.active_requests if not task.done()]
                await asyncio.wait(self.active_requests, return_when=FIRST_COMPLETED)
                print('visited_urls: {}\n'.format(len(self.visited_urls)))

        await asyncio.wait(self.active_requests)

    async def schedule_new_request(self, completed_request_count):
        url = self.extracted_urls[completed_request_count]
        self.visited_urls.append(url)
        task = asyncio.ensure_future(self.crawling(url))
        self.active_requests.append(task)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ensure_concurrency())
        loop.close()


class ParallelCrawler(Crawler):
    def __init__(self, base_url, delay, concurrent_requests, max_urls):
        super().__init__(base_url, delay, concurrent_requests, max_urls)
        self.lock = threading.Lock()

    def crawling(self, url, request_count=1):
        active_task_count = len([task for task in self.active_requests if task.running()])
        print('request {}, active requests {}'.format(request_count, active_task_count))
        self.lock.acquire()
        response = requests.get(url).text
        self.count_downloaded_bytes(response)
        self.extract_urls_from_response(response)
        self.lock.release()

    def ensure_parallelism(self):
        with ThreadPoolExecutor(max_workers=self.concurrent_requests_count) as executor:
            completed_request_count = 1
            while completed_request_count < self.max_urls_to_visit:
                time.sleep(self.download_delay)

                if completed_request_count >= len(self.extracted_urls):
                    continue

                url = self.extracted_urls[completed_request_count]
                self.visited_urls.append(url)
                completed_request_count += 1
                self.active_requests.append(executor.submit(self.crawling,
                                                            url, completed_request_count))

    def start(self):
        self.crawling(self.base_url)
        self.ensure_parallelism()


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--choice', choices=['c', 'p'], default='c',
                        help='Choose between Concurrent or Parallel')
    parser.add_argument('-u', '--url', type=validate_url,
                        default='https://www.tutorialspoint.com/', help='Enter any website url')
    parser.add_argument('-d', '--download_delay', type=float,
                        default=0.1, help='Specify download delay')
    parser.add_argument('-r', '--concurrent_request_count', type=int,
                        default=5, help='Specify number of concurrent requests')
    parser.add_argument('-m', '--max_urls_to_visit', type=int,
                        default=20, help='Specify the maximum number of urls should be visited')

    arguments = parser.parse_args()
    return arguments


def validate_url(url):
    if bool(urlparse(url).netloc):
        return url
    else:
        raise argparse.ArgumentTypeError('Please enter a valid url')


if __name__ == '__main__':
    args = get_arguments()
    if 'c' in args.choice:
        async_crawler = AsyncCrawler(
            args.url, args.download_delay, args.concurrent_request_count, args.max_urls_to_visit)
        async_crawler.start()
        async_crawler.show_performance('Asynchronous')
    else:
        parallel_crawler = ParallelCrawler(
            args.url, args.download_delay, args.concurrent_request_count, args.max_urls_to_visit)
        parallel_crawler.start()
        parallel_crawler.show_performance('Parallel')

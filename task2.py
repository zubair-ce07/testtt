import asyncio
import argparse
import functools
import multiprocessing
import concurrent.futures
from time import sleep
from multiprocessing.managers import BaseManager

import aiohttp
import requests
from parsel import Selector


class CustomManager(BaseManager):
    pass


class StatsCollector:
    def __init__(self):
        self.requests_made = 0
        self.bytes_downloaded = 0

    @property
    def requests_count(self):
        return self.requests_made

    def update_stats(self, response_size_in_bytes):
        self.requests_made += 1
        self.bytes_downloaded += response_size_in_bytes

    def print_stats(self):
        try:
            average_page_size = self.bytes_downloaded / self.requests_made
        except ZeroDivisionError:
            average_page_size = 0

        print('#--- Report ---#')
        print('Total Requests made: {}'.format(self.requests_made))
        print('Total bytes downloaded: {}'.format(self.bytes_downloaded))
        print('Average page size(bytes): {}'.format(average_page_size), end='\n')


def extract_new_urls(text):
    links = Selector(text).css('a::attr(href)').extract()
    return [link for link in links if 'http' in link]


async def make_room_for_new_request(active_urls):
    await active_urls.get()


async def process_request(url, active_urls, waiting_urls, stats_collector):
    async with aiohttp.ClientSession() as session:
        response_size = 0
        try:
            async with session.get(url) as resp:
                await make_room_for_new_request(active_urls)
                if resp.status == 200:
                    response_size = len(await resp.read())
                    text = await resp.text()
                    for url in extract_new_urls(text):
                        waiting_urls.put_nowait(url)

        except RuntimeError as e:
            print(str(e))

        finally:
            stats_collector.update_stats(response_size)


async def crawl_concurrently(website_url, concurrent_requests, download_delay,
                             total_requests, stats_collector, **other):
    active_urls = asyncio.Queue(maxsize=concurrent_requests)
    waiting_urls = asyncio.Queue()
    waiting_urls.put_nowait(website_url)
    tasks = []

    crawled_url_count = 0
    while crawled_url_count < total_requests:
        url = await waiting_urls.get()
        await active_urls.put('dummy')
        print('active request count: {}'.format(active_urls.qsize()))

        task = asyncio.ensure_future(process_request(url, active_urls, waiting_urls, stats_collector))
        tasks.append(task)
        crawled_url_count += 1
        await asyncio.sleep(download_delay)

    await asyncio.gather(*tasks)


def worker_process(waiting_urls, download_delay, crawled_url_count, total_requests,
                   stats_collector, counter_lock, stats_lock):
    while True:
        counter_lock.acquire()
        crawled_url_count.value += 1
        counter_lock.release()

        if crawled_url_count.value > total_requests:
            return

        url = waiting_urls.get()
        try:
            r = requests.get(url, allow_redirects=False)
        except Exception as e:
            print(str(e))

        if r.status_code == requests.codes.ok:
            urls = extract_new_urls(r.text)
            for url in urls:
                waiting_urls.put(url)

        stats_lock.acquire()
        stats_collector.update_stats(len(r.content))
        print('crawled count: {}'.format(stats_collector._getvalue().requests_count))
        stats_lock.release()

        sleep(download_delay)


def crawl_in_parallel(website_url, concurrent_requests, download_delay,
                      total_requests, stats_collector, manager, **other):
    counter_lock = manager.Lock()
    stats_lock = manager.Lock()
    crawled_url_count = manager.Value('i', 0)
    waiting_urls = manager.Queue()
    waiting_urls.put_nowait(website_url)

    with concurrent.futures.ProcessPoolExecutor(
            max_workers=concurrent_requests) as executor:
        for _ in range(concurrent_requests):
            executor.submit(
                worker_process,
                waiting_urls, download_delay, crawled_url_count, total_requests,
                stats_collector, counter_lock, stats_lock
            )


def check_positive_number(num_type, error_msg, value):
    try:
        n = num_type(value)
        if n <= 0:
            raise argparse.ArgumentTypeError(error_msg)
    except ValueError:
        raise argparse.ArgumentTypeError(error_msg)
    else:
        return n


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('website_url', type=str)
    parser.add_argument('--crawl_mode', '-m', default='concurrent', choices=['concurrent', 'parallel'])
    parser.add_argument('--concurrent_requests', '-cr', default=4, help='limit simultaneous request count',
                        type=functools.partial(check_positive_number, int, 'invalid positive integer'))
    parser.add_argument('--download_delay', '-dd', default=2, help='delay between each request',
                        type=functools.partial(check_positive_number, float, 'invalid positive float'))
    parser.add_argument('--total_requests', '-tr', default=50, help='total number of requests allowed',
                        type=functools.partial(check_positive_number, int, 'invalid positive integer'))
    args = vars(parser.parse_args())
    args['manager'] = multiprocessing.Manager()

    if args['crawl_mode'] == 'concurrent':
        args['stats_collector'] = StatsCollector()
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(crawl_concurrently(**args))
        event_loop.close()

    elif args['crawl_mode'] == 'parallel':
        CustomManager.register('StatsCollector', StatsCollector)
        custom_manager = CustomManager()
        custom_manager.start()
        args['stats_collector'] = custom_manager.StatsCollector()
        crawl_in_parallel(**args)

    args['stats_collector'].print_stats()


if __name__ == '__main__':
    main()

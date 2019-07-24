import argparse
import asyncio
import concurrent.futures
import functools
import time
from urllib.parse import urljoin
from urllib.parse import urlparse

import requests
from parsel import Selector


class Crawler:
    def __init__(self, start_url, max_workers, delay, max_num_urls):
        self.start_url = start_url
        self.delay = delay
        self.max_num_urls = max_num_urls
        self.visited_urls = set()
        self.bounded_semaphore = asyncio.BoundedSemaphore(max_workers)

    def _validate_urls(self, url, base_url=None):
        if url not in self.visited_urls:
            if "http" not in url:
                url = urljoin(base_url, url)
            if ("http" in url and "#" not in url and
                    "?" not in url and all([urlparse(url).scheme, urlparse(url).netloc])):
                return url

    async def _find_urls(self, http_response, base_url):
        await asyncio.sleep(0.1)
        all_urls = Selector(text=http_response.text).xpath("//a/@href").getall()
        fn = functools.partial(self._validate_urls, base_url=base_url)
        return filter(self._validate_urls, all_urls)

    async def _get_url_data(self, url):
        http_response = await self._http_request(url)
        found_urls = set()
        if http_response:
            urls = await self._find_urls(http_response, url)
            found_urls.update(urls)
        return url, http_response, found_urls

    async def _extract_multi_url(self, to_fetch):
        futures, results = [], []
        for url in to_fetch:
            if url not in self.visited_urls and len(self.visited_urls) < self.max_num_urls:
                self.visited_urls.add(url)
                futures.append(self._get_url_data(url))
        for future in asyncio.as_completed(futures):
            results.append((await future))
        return results

    async def crawl(self):
        to_fetch = [self.start_url]
        results = []
        while len(self.visited_urls) < self.max_num_urls:
            batch = await self._extract_multi_url(to_fetch)
            to_fetch = []
            for url, data, found_urls in batch:
                data = len(data.content) if data else 0
                results.append({"URL": url, "Bytes": data})
                to_fetch.extend(found_urls)
        return results


class ConcurrentCrawler(Crawler):

    async def _http_request(self, url):
        print(f'Fetching: {url}')
        try:
            async with self.bounded_semaphore:
                await asyncio.sleep(self.delay)
                fn = functools.partial(requests.get, url, timeout=10)
                future_response = await asyncio.get_event_loop().run_in_executor(None, fn)
                return future_response
        except (requests.ConnectionError, requests.Timeout):
            pass


class ParallelCrawler(Crawler):

    async def _http_request(self, url):
        print(f'Fetching: {url}')
        try:
            async with self.bounded_semaphore:
                with concurrent.futures.ProcessPoolExecutor() as pool:
                    fn = functools.partial(requests.get, url, timeout=10)
                    future_response = await asyncio.get_running_loop().run_in_executor(pool, fn)
                    await asyncio.sleep(self.delay)
                    return future_response
        except (requests.ConnectionError, requests.Timeout):
            pass


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store', dest='start_url',
                        type=lambda u: u if all([urlparse(u).scheme, urlparse(u).netloc]) else parser.error("Invalid URL"),
                        help='Enter URL where you want to start crawling.')
    parser.add_argument('-w', action='store', dest="concurrent_requests", type=int,
                        help="Enter Number of concurrent requests a worker can make.")
    parser.add_argument('-d', action='store', dest="download_delay", type=float,
                        help="Enter download delay that each worker has to follow.")
    parser.add_argument('-m', action='store', dest="max_urls", type=int,
                        help="Maximum number of URLs to crawl.")
    parser.add_argument('-c', action='store', dest="crawler_to_run", type=str,
                        help="Enter 1 to run concurrent and 2 to run  parallel crawler.")
    return parser.parse_args()


def report(results):
    print(f"Bytes Downloaded: {sum([r['Bytes'] for r in results])}")
    print(f"Average Page Size: {sum([r['Bytes'] for r in results]) / len(results)}")
    print(f"Requests Made: {len(results)}")


def main():
    start = time.time()
    args = arg_parser()

    if args.crawler_to_run == "concurrent":
        crawler = ConcurrentCrawler(args.start_url, args.concurrent_requests, args.download_delay, args.max_urls)
    elif args.crawler_to_run == "parallel":
        crawler = ParallelCrawler(args.start_url, args.concurrent_requests, args.download_delay, args.max_urls)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(crawler.crawl())
    loop.close()
    end = time.time()
    report(results)
    print((f"Execution Time: {end - start}"))


if __name__ == "__main__":
    main()

import time

import requests
import argparse
import asyncio
import concurrent.futures
from parsel import Selector


class Crawler:
    def __init__(self, start_url, max_workers, delay, max_num_urls):
        self.start_url = start_url
        self.delay = delay
        self.max_num_urls = max_num_urls
        self.visited = set()
        self.bounded_semaphore = asyncio.BoundedSemaphore(max_workers)
        self.parser = Parser()

    def _find_urls(self, request):
        all_urls = Selector(text=request.text).xpath("//a/@href").getall()
        found_urls = []
        for url in all_urls:
            if url not in self.visited and self.parser.is_valid_url(url):
                found_urls.append(url)
        return found_urls

    async def _get_url_data(self, url):
        data = await self._http_request(url)
        found_urls = set()
        if data:
            for url in self._find_urls(data):
                found_urls.add(url)
        return url, data, sorted(found_urls)

    async def _extract_multi_url(self, to_fetch):
        futures, results = [], []
        for url in to_fetch:
            if url not in self.visited and len(self.visited) < self.max_num_urls:
                self.visited.add(url)
                futures.append(self._get_url_data(url))
            else:
                break
        for future in asyncio.as_completed(futures):
            results.append((await future))
        return results

    async def crawl(self):
        to_fetch = [self.start_url]
        results = []
        while len(self.visited) < self.max_num_urls:
            batch = await self._extract_multi_url(to_fetch)
            to_fetch = []
            for url, data, found_urls in batch:
                data = self.parser.content_parser(data)
                results.append({"URL": url, "Bytes": data})
                to_fetch.extend(found_urls)
        return results


class ConcurrentCrawler(Crawler):

    async def _http_request(self, url):
        print(f'Fetching: {url}')
        try:
            async with self.bounded_semaphore:
                await asyncio.sleep(self.delay)
                future_response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
                return future_response
        except requests.ConnectionError:
            print(f"Connection Error Occured while trying to get: {url}")
        except requests.Timeout:
            print(f"Timeout Error Occured while trying to get: {url}")


class ParallelCrawler(Crawler):

    async def _http_request(self, url):
        print(f'Fetching: {url}')
        try:
            async with self.bounded_semaphore:
                with concurrent.futures.ProcessPoolExecutor() as pool:
                    future_response = await asyncio.get_running_loop().run_in_executor(pool, requests.get, url)
                    await asyncio.sleep(self.delay)
                    return future_response
        except requests.ConnectionError:
            print(f"Connection Error Occured while trying to get: {url}")
        except requests.Timeout:
            print(f"Timeout Error Occured while trying to get: {url}")


class Parser:
    def is_valid_url(self, url):
        return True if "http" in url else False

    def content_parser(self, data):
        return(len(data.content)) if data else 0

    def arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', action='store', dest='start_url',
                            help='Enter URL where you want to start crawling.')
        parser.add_argument('-w', action='store', dest="concurrent_requests", type=int,
                            help="Enter Number of concurrent requests a worker can make.")
        parser.add_argument('-d', action='store', dest="download_delay", type=float,
                            help="Enter download delay that each worker has to follow.")
        parser.add_argument('-m', action='store', dest="max_urls", type=int,
                            help="Maximum number of URLs to crawl.")
        parser.add_argument('-c', action='store', dest="crawler_to_run", type=int,
                            help="Enter 1 to run concurrent and 2 to run  parallel crawler.")
        return parser.parse_args()


def main():
    start = time.time()
    args = Parser().arg_parser()

    if args.crawler_to_run == 1:
        crawler = ConcurrentCrawler(args.start_url, args.concurrent_requests, args.download_delay, args.max_urls)
    elif args.crawler_to_run == 2:
        crawler = ParallelCrawler(args.start_url, args.concurrent_requests, args.download_delay, args.max_urls)

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(crawler.crawl())
    loop.close()
    end = time.time()

    print(f"Bytes Downloaded: {sum([r['Bytes'] for r in result])}")
    print(f"Average Page Size: {sum([r['Bytes'] for r in result]) / len(result)}")
    print(f"Requests Made: {len(result)}")
    print((f"Execution Time: {end - start}"))
    print(len(result))


if __name__ == "__main__":
    main()

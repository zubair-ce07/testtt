import argparse
import asyncio
import concurrent.futures
import re
from urllib.parse import urljoin

import requests
from parsel import Selector


class Crawler:
    def __init__(self, start_url, max_workers, delay, max_num_urls):
        self.start_url = start_url
        self.delay = delay
        self.max_num_urls = max_num_urls
        self.visited_urls = set()
        self.bounded_semaphore = asyncio.BoundedSemaphore(max_workers)
        self.domain = "tennis-warehouse.com"
        self.loop = asyncio.get_event_loop()

    async def parse(self, http_response, base_url):
        await asyncio.sleep(self.delay)
        anchor_urls = Selector(text=http_response.text).xpath("//a/@href").getall()
        anchor_urls = [u for u in anchor_urls if (self.domain in u or u.startswith('/')) and '@' not in u]
        return map(lambda url: urljoin(base_url, url), anchor_urls)

    async def _extract_url_data(self, url):
        http_response = await self._http_request(url)
        found_urls = set()
        if http_response:
            found_urls.update(await self.parse(http_response, url))
        return url, http_response, found_urls

    async def _extract_multi_url(self, to_fetch):
        futures = []
        for url in to_fetch:
            if url not in self.visited_urls and len(self.visited_urls) < self.max_num_urls:
                self.visited_urls.add(url)
                futures.append(self._extract_url_data(url))
        return [(await future) for future in asyncio.as_completed(futures)]

    async def _crawl(self):
        to_fetch = [self.start_url]
        results = []
        while len(self.visited_urls) < self.max_num_urls:
            batch = await self._extract_multi_url(to_fetch)
            to_fetch = []
            for url, data, found_urls in batch:
                bytes_downloaded = len(data.content) if data else 0
                results.append({"URL": url, "Bytes": bytes_downloaded})
                to_fetch.extend(found_urls)
        return results

    def run_crawler(self):
        try:
            results = self.loop.run_until_complete(self._crawl())
        finally:
            self.loop.close()
        return results


class ConcurrentCrawler(Crawler):

    async def _http_request(self, url):
        try:
            async with self.bounded_semaphore:
                await asyncio.sleep(self.delay)
                future_response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
                return future_response
        except (requests.ConnectionError, requests.Timeout):
            pass


class ParallelCrawler(Crawler):

    async def _http_request(self, url):
        try:
            async with self.bounded_semaphore:
                with concurrent.futures.ProcessPoolExecutor() as pool:
                    future_response = await asyncio.get_running_loop().run_in_executor(pool, requests.get, url)
                    await asyncio.sleep(self.delay)
                    return future_response
        except (requests.ConnectionError, requests.Timeout):
            pass


def _is_valid_url(url):
    regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    if re.match(regex, url):
        return url
    raise argparse.ArgumentTypeError(f"{url} is invalid.")


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store', dest='start_url',
                        type=_is_valid_url,
                        help='Enter URL where you want to start crawling.',
                        default="https://www.tennis-warehouse.com/")
    parser.add_argument('-w', action='store', dest="concurrent_requests",
                        type=lambda n: int(n) if int(n) > 0 else 1,
                        help="Enter Number of concurrent requests a worker can make.")
    parser.add_argument('-d', action='store', dest="download_delay",
                        type=lambda d: float(d) if float(d) >= 0 else 2,
                        help="Enter download delay that each worker has to follow.")
    parser.add_argument('-m', action='store', dest="max_urls",
                        type=lambda n: int(n) if int(n) > 0 else 200,
                        help="Maximum number of URLs to crawl.")
    parser.add_argument('-c', action='store', dest="crawler_to_run", type=str, choices=['parallel', 'concurrent'],
                        help="Enter 1 to run concurrent and 2 to run  parallel crawler.",
                        default="concurrent")
    return parser.parse_args()


def generate_report(results):
    print(f"Bytes Downloaded: {sum([r['Bytes'] for r in results])}")
    print(f"Average Page Size: {sum([r['Bytes'] for r in results]) / len(results)}")
    print(f"Requests Made: {len(results)}")


def main():
    args = arg_parser()

    if args.crawler_to_run == "concurrent":
        results = ConcurrentCrawler(args.start_url, args.concurrent_requests,
                                    args.download_delay, args.max_urls).run_crawler()
    elif args.crawler_to_run == "parallel":
        results = ParallelCrawler(args.start_url, args.concurrent_requests,
                                  args.download_delay, args.max_urls).run_crawler()
    generate_report(results)


if __name__ == "__main__":
    main()

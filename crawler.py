import requests
import time
import argparse
import asyncio
from itertools import islice
from concurrent import futures
from parsel import Selector
from abc import ABC


# Input:
# Number of concurrent request that can be made
# maximum number of urls to visit
# download delay each worker will observe

# Output:
# number of requests made
# total bytes downloaded
# average size of a page


def iterate_links(urls):
    for url_ in urls:
        yield url_


class Crawler(ABC):
    def __init__(self, max_url_hits, download_delay, x_path):
        self.requests_made = 0
        self.max_url_hits = max_url_hits
        self.download_delay = download_delay
        self.x_path = x_path
        self.responses = []

    def get_stats(self):
        print(f"URLs hit: {self.requests_made}")
        print("Bytes downloaded: ", end="")
        print(f"{sum(len(r.text) + len(r.headers) for r in self.responses)}")
        print("Average size of a page: ", end="")
        print(f"{sum(len(r.text) for r in self.responses)/self.requests_made}")


class ConcurrentWebCrawler(Crawler):
    def __init__(self, concurrency, max_url_hits, download_delay, x_path):
        super().__init__(max_url_hits, download_delay, x_path)
        self.concurrency = concurrency

    async def crawl_page(self, link):
        if self.requests_made >= self.max_url_hits:
            return
        else:
            self.requests_made += 1
            await asyncio.sleep(self.download_delay)
            http_response = requests.get(link)
            print(http_response.content)
            self.responses.append(http_response)
            urls = Selector(http_response.text).xpath(self.x_path).extract()
            if urls:
                urls = iterate_links(urls)
                while self.requests_made < self.max_url_hits:
                    await asyncio.gather(*map(
                        self.crawl_page, list(islice(urls, self.concurrency))))


class ParallelWebCrawler(Crawler):
    def __init__(self, concurrency, max_url_hits, download_delay, x_path):
        super().__init__(max_url_hits, download_delay, x_path)
        self.executor = futures.ProcessPoolExecutor(
            max_workers=concurrency)

    def crawl(self, urls):
        future_requests = (self.executor.submit(requests.get, url)
                           for url in urls)
        for future in futures.as_completed(future_requests):
            if self.requests_made >= self.max_url_hits:
                future.cancel()
                continue
            self.requests_made += 1
            time.sleep(self.download_delay)
            http_response = future.result()
            print(http_response.content)
            self.responses.append(http_response)
            urls = Selector(http_response.text).xpath(self.x_path).extract()
            if urls and self.requests_made < self.max_url_hits:
                urls = iterate_links(urls)
                self.crawl(urls)


def get_input():
    delay = int(input("Download Dela1y for every request: "))
    max_hits = int(input("Max URLS to be hit: "))
    max_concurrency = int(input("Max Concurrent requests: "))
    url = input("URL to begin crawling: ")
    x_path = "//a[starts-with(@href,'https')]/@href"
    return max_concurrency, max_hits, delay, x_path, url


def crawler_type():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true')
    return parser.parse_args().p


def init_concurrent(max_concurrency, max_hits, delay, x_path, link):
    crawler = ConcurrentWebCrawler(max_concurrency, max_hits, delay, x_path)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawler.crawl_page(link))
    loop.close()
    crawler.get_stats()


def init_parallel(max_concurrency, max_hits, delay, x_path, link):
    crawler = ParallelWebCrawler(max_concurrency, max_hits, delay, x_path)
    crawler.crawl([link])
    crawler.get_stats()


crawl = {True: init_parallel, False: init_concurrent}


if __name__ == "__main__":
    max_concurrency, max_hits, delay, x_path, url = get_input()
    crawl[crawler_type()](max_concurrency, max_hits, delay, x_path, url)

import requests
import time
import argparse
import asyncio
from itertools import islice
from concurrent import futures
from parsel import Selector


class Crawler:
    def __init__(self, max_url_hits, download_delay):
        self.requests_made = 0
        self.max_url_hits = max_url_hits
        self.download_delay = download_delay
        self.xpath = "//a[starts-with(@href,'https')]/@href"
        self.responses = []

    def get_stats(self):
        print(f"URLs hit: {self.requests_made}")
        print("Bytes downloaded: ", end="")
        print(f"{sum(len(r.text) + len(r.headers) for r in self.responses)}")
        print("Average size of a page: ", end="")
        print(f"{sum(len(r.text) for r in self.responses)/self.requests_made}")


class ConcurrentWebCrawler(Crawler):
    def __init__(self, concurrency, max_url_hits, download_delay):
        super().__init__(max_url_hits, download_delay)
        self.concurrency = concurrency

    async def crawl_page(self, url):
        if self.requests_made >= self.max_url_hits or not url:
            return
        else:
            self.requests_made += 1
            await asyncio.sleep(self.download_delay)
            response = requests.get(url)
            print(response.content)
            self.responses.append(response)
            urls = iter(Selector(response.text).xpath(self.xpath).extract())
            while self.requests_made < self.max_url_hits:
                sublist = list(islice(urls, self.concurrency))
                if sublist:
                    await asyncio.gather(*map(self.crawl_page, sublist))
                else:
                    break


class ParallelWebCrawler(Crawler):
    def __init__(self, concurrency, max_url_hits, download_delay):
        super().__init__(max_url_hits, download_delay)
        self.executor = futures.ProcessPoolExecutor(max_workers=concurrency)

    def crawl(self, urls):
        future_reqs = (self.executor.submit(requests.get, url) for url in urls)
        for future in futures.as_completed(future_reqs):
            if self.requests_made >= self.max_url_hits:
                future.cancel()
                continue
            self.requests_made += 1
            time.sleep(self.download_delay)
            response = future.result()
            print(response.content)
            self.responses.append(response)
            urls = Selector(response.text).xpath(self.xpath).extract()
            if urls and self.requests_made < self.max_url_hits:
                self.crawl(urls)


def get_input():
    download_delay = int(input("Download Delay for every request: "))
    max_hits = int(input("Max URLS to be hit: "))
    max_concurrency = int(input("Max Concurrent requests: "))
    url = input("URL to begin crawling: ")
    return max_concurrency, max_hits, download_delay, url


def crawler_type():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true')
    return parser.parse_args().p


def init_concurrent(max_concurrency, max_hits, download_delay, url):
    crawler = ConcurrentWebCrawler(max_concurrency, max_hits, download_delay)
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(crawler.crawl_page(url))
    event_loop.close()
    crawler.get_stats()


def init_parallel(max_concurrency, max_hits, download_delay, url):
    crawler = ParallelWebCrawler(max_concurrency, max_hits, download_delay)
    crawler.crawl([url])
    crawler.get_stats()


crawl = {True: init_parallel, False: init_concurrent}


if __name__ == "__main__":
    max_concurrency, max_hits, download_delay, url = get_input()
    crawl[crawler_type()](max_concurrency, max_hits, download_delay, url)

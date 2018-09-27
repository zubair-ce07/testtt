import argparse
import asyncio
import time
from urllib import parse

import requests
import parsel


class AsyncSpider:

    def __init__(self, url, concurrent_req, delay, url_visit_limit):
        self.visited_urls = dict()
        self.pending_urls = set([url])
        self.concurrent_req = concurrent_req
        self.delay = delay
        self.url_visit_limit = url_visit_limit
        self.num_request_made = 0
        self.total_bytes_downloaded = 0
        self.semaphore = asyncio.BoundedSemaphore(concurrent_req)

    async def extract_urls(self, url, loop):
        async with self.semaphore:
            future = loop.run_in_executor(None, requests.get, url)
            response = await future
            time.sleep(self.delay)
        self.num_request_made += 1
        if response.status_code == 200\
                and response.headers.get('content-length'):
            self.visited_urls[url] = True
            self.total_bytes_downloaded += int(response.headers.get(
                'content-length'))
            selector = parsel.Selector(text=response.text)
            extracted_urls = selector.css("a::attr(href)").extract()
            for link in extracted_urls:
                link = parse.urljoin(url, link)
                if not self.visited_urls.get(link):
                    self.pending_urls.add(link)

    async def schedule_futures(self, loop):
        futures = []
        while self.pending_urls and self.url_visit_limit > 1:
            url = self.pending_urls.pop()
            self.url_visit_limit -= 1
            futures.append(
                asyncio.ensure_future(self.extract_urls(url, loop)))
        await asyncio.wait(futures)
        return futures

    def crawl(self):
        while self.url_visit_limit > 1:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.schedule_futures(loop))

    def spider_report(self):
        print(f"Total Bytes downloaded: {self.total_bytes_downloaded//1024}KB")
        print(f"Number of requests: {self.num_request_made}")
        print(f"Average page size :"
              f"{(self.total_bytes_downloaded//self.num_request_made)//1024}"
              f"KB")


def validate_url(url):
    if parse.urlparse(url).scheme:
        return url
    raise argparse.ArgumentTypeError('url is not valid')


def main():
    arg_parser = argparse.ArgumentParser(description='Process some date')
    arg_parser.add_argument('url', type=validate_url,
                            help='Domain to crawl')
    arg_parser.add_argument('concurrent_request', type=int,
                            help='Number of Concurrent Request in one go')
    arg_parser.add_argument('delay', type=float,
                            help='Delay time each user gets')
    arg_parser.add_argument('total_urls', type=int,
                            help='Maximum number of urls to visit)')
    args = arg_parser.parse_args()
    sp = AsyncSpider(args.url, args.concurrent_request, args.delay,
                     args.total_urls)
    sp.crawl()
    sp.spider_report()


if __name__ == "__main__":
    main()
import argparse
import asyncio
from urllib.parse import urljoin, urlparse

import requests
import validators
from parsel import Selector


class Crawler:

    def __init__(self, site_to_crawl, urls_limit, download_delay, concurrency):
        self.allowed_domain = urlparse(site_to_crawl).netloc
        self.urls_limit = urls_limit
        self.download_delay = download_delay

        self.workers_lock = asyncio.Semaphore(concurrency)
        self.loop = asyncio.get_event_loop()

        self.submitted_requests = []
        self.seen_urls = set([])
        self.queued_urls = {site_to_crawl}
        self.downloaded_bytes = 0

    def extract_links(self, response):
        return Selector(text=response.text).xpath('//a/@href').extract()

    def absolute_url(self, base_url, url):
        return urljoin(base_url, url)

    def filter_links(self, links):
        return {link for link in links if self.allowed_domain in link}

    def parse_response(self, response):
        links = self.extract_links(response)
        absoulte_links = [self.absolute_url(
            response.url, link) for link in links]
        self.queued_urls.update(self.filter_links(absoulte_links))

    async def make_request(self, url):
        try:
            self.parse_response(requests.get(url))
        except requests.exceptions.RequestException:
            print(f'Failed to Process URL: ', url)

    async def schedule_requests(self):
        while self.is_pending_requests() or self.queued_urls:
            if len(self.seen_urls) == self.urls_limit:
                break

            if not self.queued_urls:
                continue

            url = self.queued_urls.pop()
            if url in self.seen_urls:
                continue

            print(f'URL> {url}')
            self.seen_urls.add(url)

            self.workers_lock.acquire()
            request = self.loop.create_task(self.make_request(url))
            request.add_done_callback(lambda f: self.workers_lock.release())
            self.submitted_requests.append(request)

            await asyncio.sleep(self.download_delay)

    def run(self):
        self.loop.run_until_complete(self.schedule_requests())
        self.loop.close()

    def is_pending_requests(self):
        return not all(r.done() for r in self.submitted_requests)

    def print_stats(self):
        print(f'Number of Requests Made: {len(self.seen_urls)}')
        print(f'Total Downloaded Bytes: {self.downloaded_bytes}')
        print(f'Average Page Size: {self.downloaded_bytes//len(self.seen_urls)}')


def validate_url(url):
    if validators.url(url):
        return url
    raise argparse.ArgumentTypeError("Invalid URL")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("site_to_crawl", type=validate_url,
                        help="Specify the url for website to crawl")
    parser.add_argument("urls_limit", type=int,
                        help="Specify the maximum urls limit to visit")
    parser.add_argument("download_delay", type=float,
                        help="Specify the download delay for a request")
    parser.add_argument("concurrency", type=int,
                        help="Specify the number of concurrent requests")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    crawler = Crawler(args.site_to_crawl, args.urls_limit,
                      args.download_delay, args.concurrency)
    crawler.run()
    crawler.print_stats()

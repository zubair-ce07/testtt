import argparse
import asyncio
from urllib import parse

import requests
import parsel


def main():
    parser = argparse.ArgumentParser(description='A program that crawls a website concurrently.')
    parser.add_argument('url', help='this arguments specifies the url of the website to crawl',
                        type=url_validate)
    parser.add_argument('max_url', help='this arguments specifies the maximum number '
                        'of urls to visit', type=int)
    parser.add_argument('req_limit', help='this arguments specifies the number of '
                        'concurrent requests allowed', type=int)
    parser.add_argument('delay', help='this arguments specifies the delay between each request'
                        , type=float)
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    crawler = Crawler(args.url)
    loop.run_until_complete(crawler.crawl_async(args.max_url, args.req_limit, args.delay))
    crawler.crawl_report()
    loop.close()


def url_validate(url):
    if parse.urlparse(url).netloc:
        return url
    raise argparse.ArgumentTypeError("Invalid url.")


class Crawler:

    def __init__(self, web_url):
        self.website_url = web_url
        self.bytes_downloaded = 0
        self.visited_urls = set()

    async def fetch_page(self, url, delay):
        await asyncio.sleep(delay)
        response = requests.get(url)
        self.bytes_downloaded = self.bytes_downloaded + len(response.content)
        return response.text

    async def extract_urls(self, url, delay):
        url = parse.urljoin(self.website_url, url)
        page_text = await self.fetch_page(url, delay)
        selector = parsel.Selector(text=page_text)
        found_urls = selector.css("a::attr(href)").extract()
        found_urls = set(found_urls)
        found_urls = self.filter_absolute_urls(found_urls)
        return found_urls

    def filter_absolute_urls(self, urls):
        filtered_urls = set(filter(lambda url: not parse.urlparse(url).netloc
                            and not parse.urlparse(url).scheme == 'mailto', urls))
        return filtered_urls

    async def crawl_async(self, url_limit, request_limit, download_delay):
        found_urls = set('/')
        future_requests = []
        self.visited_urls = set()
        while True:
            for request_no in range(request_limit):
                if found_urls:
                    url = found_urls.pop()
                    future_requests.append(self.extract_urls(url, download_delay))
                    self.visited_urls = self.visited_urls.union({url})
                    if len(self.visited_urls) == url_limit:
                        break
            for request in asyncio.as_completed(future_requests):
                found_urls = found_urls.union(await request)
            found_urls = found_urls.difference(self.visited_urls)
            future_requests = []
            if len(self.visited_urls) == url_limit:
                break

    def crawl_report(self):
        print(f"Number of requests: {len(self.visited_urls)}.")
        print(f"Bytes downloaded: {self.bytes_downloaded}B.")
        print(f"Average page size : {self.bytes_downloaded//len(self.visited_urls)}B.")


if __name__ == '__main__':
    main()

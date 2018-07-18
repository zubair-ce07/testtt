import argparse
import asyncio
from urllib import parse

import requests
import parsel


def main():
    parser = argparse.ArgumentParser(description='A program that crawls a website concurrently.')
    parser.add_argument('url', help='this arguments specifies the url of the website to crawl',
                        type=url_validate)
    parser.add_argument('-m', '--max_url', help='this arguments specifies the maximum number '
                        'of urls to visit', default=20, type=int)
    parser.add_argument('-r', '--requests_count', default=5, help='this arguments specifies the number of '
                        'concurrent requests allowed', type=int)
    parser.add_argument('-d', '--delay', default=0.05, help='this arguments specifies the delay '
                        'between each request', type=float)
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    crawler = Crawler(args.url)
    loop.run_until_complete(crawler.crawl_async(args.max_url, args.requests_count, args.delay))
    loop.close()
    crawler.crawl_report()


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
        extracted_urls = selector.css("a::attr(href)").extract()
        extracted_urls = set(extracted_urls)
        extracted_urls = self.filter_absolute_urls(extracted_urls)
        return extracted_urls

    def filter_absolute_urls(self, urls):
        filtered_urls = set(filter(lambda url: not parse.urlparse(url).netloc
                            and not parse.urlparse(url).scheme == 'mailto', urls))
        return filtered_urls

    async def crawl_async(self, url_limit, request_count, download_delay):
        extracted_urls = await self.extract_urls('/', download_delay)
        future_requests = []
        self.visited_urls = set('/')
        for request_no in range(1, url_limit):
            url = extracted_urls.pop()
            future_requests.append(self.extract_urls(url, download_delay))
            self.visited_urls = self.visited_urls.union({url})
            if not request_no % request_count or request_no == url_limit-1:
                for request in asyncio.as_completed(future_requests):
                    extracted_urls = extracted_urls.union(await request)
                future_requests = []
            extracted_urls = extracted_urls.difference(self.visited_urls)

    def crawl_report(self):
        print(f"Number of requests: {len(self.visited_urls)}.")
        print(f"Bytes downloaded: {self.bytes_downloaded}B.")
        print(f"Average page size : {self.bytes_downloaded//len(self.visited_urls)}B.")


if __name__ == '__main__':
    main()

import argparse
import time
from concurrent.futures import ProcessPoolExecutor
from urllib import parse

import requests
import parsel


def main():
    parser = argparse.ArgumentParser(description='A program that crawls a website parallel.')
    parser.add_argument('url', help='this arguments specifies the url of the website to crawl',
                        type=url_validate)
    parser.add_argument('max_url', help='this arguments specifies the maximum number '
                        'of urls to visit', type=int)
    parser.add_argument('req_limit', help='this arguments specifies the number of '
                        'concurrent requests allowed', type=int)
    parser.add_argument('delay', help='this arguments specifies the delay between each request'
                        , type=float)
    args = parser.parse_args()
    crawler = Crawler(args.url)
    crawler.crawl_parallel(args.max_url, args.req_limit, args.delay)
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

    def fetch_page(self, url, delay):
        time.sleep(delay)
        response = requests.get(url)
        return response.text, len(response.content)

    def extract_urls(self, url, delay):
        url = parse.urljoin(self.website_url, url)
        page_text, page_size = self.fetch_page(url, delay)
        selector = parsel.Selector(text=page_text)
        found_urls = selector.css("a::attr(href)").extract()
        found_urls = set(found_urls)
        found_urls = self.filter_absolute_urls(found_urls)
        return found_urls, page_size

    def filter_absolute_urls(self, urls):
        filtered_urls = set(filter(lambda url: not parse.urlparse(url).netloc
                            and not parse.urlparse(url).scheme == 'mailto', urls))
        return filtered_urls

    def crawl_parallel(self, url_limit, request_limit, download_delay):
        found_urls = set('/')
        future_requests = []
        executor = ProcessPoolExecutor(max_workers=request_limit)
        self.visited_urls = set()

        while True:
            for _ in range(url_limit):
                if found_urls:
                    url = found_urls.pop()
                    future_requests.append(executor.submit(self.extract_urls, url, download_delay))
                    self.visited_urls = self.visited_urls.union({url})
                else:
                    break
                if len(self.visited_urls) == url_limit:
                    break
            for request in future_requests:
                urls, page_size = request.result()
                self.bytes_downloaded = self.bytes_downloaded + page_size
                found_urls = found_urls.union(urls)
                found_urls = found_urls.difference(self.visited_urls)
            if len(self.visited_urls) == url_limit:
                break

    def crawl_report(self):
        print(f"Number of requests: {len(self.visited_urls)}.")
        print(f"Bytes downloaded: {self.bytes_downloaded}B.")
        print(f"Average page size : {self.bytes_downloaded//len(self.visited_urls)}B.")


if __name__ == '__main__':
    main()

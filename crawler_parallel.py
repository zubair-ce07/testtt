import argparse
import time
from concurrent.futures import ProcessPoolExecutor, wait
from urllib import parse

import requests
import parsel


def main():
    parser = argparse.ArgumentParser(description='A program that crawls a website parallel.')
    parser.add_argument('url', help='this arguments specifies the url of the website to crawl',
                        type=url_validate)
    parser.add_argument('-m', '--max_url', help='this arguments specifies the maximum number '
                        'of urls to visit', default=20, type=int)
    parser.add_argument('-r', '--requests_count', default=5, help='this arguments specifies the number of '
                        'concurrent requests allowed', type=int)
    parser.add_argument('-d', '--delay', default=0.05, help='this arguments specifies the delay '
                        'between each request', type=float)
    args = parser.parse_args()
    crawler = Crawler(args.url)
    crawler.crawl_parallel(args.max_url, args.requests_count, args.delay)
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
        self.urls_queue = {self.website_url}

    @classmethod
    def fetch_page(cls, url, delay):
        response = requests.get(url)
        time.sleep(delay)
        return response.text, len(response.content)

    def crawl_next_urls(self, url, delay):
        page_text, page_size = self.fetch_page(url, delay)
        found_urls = self.extract_and_filter_urls(page_text)
        return found_urls, page_size

    def extract_and_filter_urls(self, page_text):
        selector = parsel.Selector(text=page_text)
        extracted_urls = selector.css("a::attr(href)").extract()
        extracted_urls = [parse.urljoin(self.website_url, url) for url in extracted_urls]
        extracted_urls = set(filter(lambda url: url.startswith(self.website_url), extracted_urls))
        return extracted_urls

    def crawl_parallel(self, url_limit, request_limit, download_delay):
        executor = ProcessPoolExecutor(max_workers=request_limit)
        tasks = []
        for _ in range(url_limit):
            url = self.urls_queue.pop()
            self.visited_urls |= {url}
            tasks.append(executor.submit(self.crawl_next_urls, url, download_delay))
            if not self.urls_queue:
                self.execute_tasks(tasks)

        self.execute_tasks(tasks)

    def execute_tasks(self, tasks):
        for task in tasks:
            urls_extracted, page_size = task.result()
            urls_extracted -= self.visited_urls
            self.urls_queue |= urls_extracted
            self.bytes_downloaded += page_size
        wait(tasks)

    def crawl_report(self):
        print(f"Number of requests: {len(self.visited_urls)}.")
        print(f"Bytes downloaded: {self.bytes_downloaded}B.")
        print(f"Average page size : {self.bytes_downloaded//len(self.visited_urls)}B.")


if __name__ == '__main__':
    main()

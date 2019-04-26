import argparse
from urllib.parse import urljoin, urlparse
from multiprocessing import Pool, Manager
import time
import logging

import requests
from lxml import html


class HtmlParser:
    def __init__(self, start_url):
        self.start_url = start_url

    def parse_response(self, url):
        raw_response = requests.get(url)
        return raw_response.status_code, raw_response.text

    def parse_urls(self, raw_response_text):
        response = html.fromstring(raw_response_text)
        return response.xpath('//a[contains(@href, "/")]/@href')


class Crawler:
    def __init__(self, start_url, delay, threads, max_urls_limit):
        self.start_url = start_url
        self.delay = delay
        self.threads = threads
        self.max_urls_limit = max_urls_limit
        self.visited_urls = Manager().list()
        self.crawler_stats = CrawlStats()
        self.scheduler = Scheduler(self.start_url)

    def crawl_parallel(self):
        while len(self.visited_urls) < self.max_urls_limit:
            pool = Pool(self.threads)
            pool.apply(self.fetch_url_response)
            pool.terminate()
            pool.join()

        return self.crawler_stats

    def fetch_url_response(self):
        url = self.scheduler.get_next_url()
        self.visited_urls.append(url)

        html_parser = HtmlParser(self.start_url)

        raw_response_status_code, raw_response_text = html_parser.parse_response(url)
        time.sleep(self.delay)
        self.crawl_page(html_parser, raw_response_status_code, raw_response_text)

    def crawl_page(self, html_parser, raw_response_status_code, raw_response_text):
        if raw_response_status_code == 200:
            self.calculate_bytes_downloaded(raw_response_text)
            self.calculate_pages_crawled()

            domain_urls = self.fetch_next_urls(html_parser, raw_response_text)
            self.scheduler.add_next_urls(domain_urls)

        else:
            self.calculate_crawled_pages_error()

    def fetch_next_urls(self, html_parser, raw_response_text):
        relative_urls = html_parser.parse_urls(raw_response_text)
        absolute_urls = self.fetch_absolute_urls(relative_urls)
        domain_urls = self.filter_domain_urls(absolute_urls)

        domain_urls = set(domain_urls)
        return domain_urls - set(self.visited_urls)

    def fetch_absolute_urls(self, relative_urls):
        return [urljoin(self.start_url, url) for url in relative_urls]

    def filter_domain_urls(self, absolute_urls):
        return [url for url in absolute_urls if self.start_url in url]

    def calculate_bytes_downloaded(self, raw_response_text):
        self.crawler_stats.bytes_downloaded.value += len(raw_response_text)

    def calculate_pages_crawled(self):
        self.crawler_stats.pages_crawled.value += 1

    def calculate_crawled_pages_error(self):
        self.crawler_stats.errors.value += 1


class Scheduler:
    def __init__(self, start_url):
        self.extracted_urls = Manager().list([start_url])

    def get_next_url(self):
        return self.extracted_urls.pop()

    def add_next_urls(self, domain_urls):
        [self.extracted_urls.append(url) for url in domain_urls if url not in self.extracted_urls]


class CrawlStats:
    def __init__(self):
        self.bytes_downloaded = Manager().Value('value', 0)
        self.pages_crawled = Manager().Value('value', 0)
        self.errors = Manager().Value('value', 0)

    def print_crawler_report(self, start_time):
        print(f"Total bytes downloaded: {self.bytes_downloaded.value}")
        print(f"Total pages crawled: {self.pages_crawled.value}")
        print(f"Average page size: {self.bytes_downloaded.value / self.pages_crawled.value}")
        print(f"Total crawel time: {time.time() - start_time}")
        print(f"Total Errors: {self.errors.value}")


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')

    args = parse_arguments()
    start_time = time.time()

    crawler = Crawler(args.url, args.delay, args.threads, args.limit)
    crawler.fetch_url_response()

    stats = crawler.crawl_parallel()
    stats.print_crawler_report(start_time)


def validate_url(url):
    if urlparse(url).netloc and urlparse(url).scheme:
        return url
    raise argparse.ArgumentTypeError('{0} is not a valid url'.format(url))


def parse_arguments():
    try:
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('-u', '--url', type=validate_url,
                                help='Enter site url --Input format: https://website.com/ ')
        arg_parser.add_argument('-d', '--delay', type=int, help='Enter delay time ')
        arg_parser.add_argument('-t', '--threads', type=int, help='Enter concurrent call requests')
        arg_parser.add_argument('-l', '--limit', type=int, help='Total urls to visit limit')

        return arg_parser.parse_args()

    except argparse.ArgumentTypeError:
        arg_parser.print_help()


if __name__ == '__main__':
    main()


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

    def parse_url_response(self, url):
        raw_response = requests.get(url)
        return raw_response.status_code, raw_response.text

    def parse_urls(self, raw_response_text):
        response = html.fromstring(raw_response_text)
        return response.xpath('//a[contains(@href, "/")]/@href')

    def fetch_absolute_urls(self, relative_urls):
        return [urljoin(self.start_url, url) for url in relative_urls]

    def filter_domain_urls(self, absolute_urls):
        return [url for url in absolute_urls if self.start_url in url]


class Scheduler:
    def __init__(self, start_url, delay, threads, max_urls_limit):
        self.start_url = start_url
        self.delay = delay
        self.threads = threads
        self.max_urls_limit = max_urls_limit
        self.extracted_urls = Manager().list([start_url])
        self.visited_urls = Manager().list()
        self.crawler_stats = CrawlStats()

    def crawl_parallel(self):
        while len(self.visited_urls) < self.max_urls_limit:
            pool = Pool(self.threads)
            pool.apply(self.get_url_response)
            pool.terminate()
            pool.join()

        return self.crawler_stats

    def get_url_response(self):
        url = self.extracted_urls.pop()
        self.visited_urls.append(url)

        fetch = HtmlParser(self.start_url)
        raw_response_status_code, raw_response_text = fetch.parse_url_response(url)

        time.sleep(self.delay)
        self.fetch_next_urls(fetch, raw_response_status_code, raw_response_text)

    def fetch_next_urls(self, fetch, raw_response_status_code, raw_response_text):
        if raw_response_status_code == 200:
            self.crawler_stats.bytes_downloaded.value += len(raw_response_text)
            self.crawler_stats.pages_crawled.value += 1

            relative_urls = fetch.parse_urls(raw_response_text)
            absolute_urls = fetch.fetch_absolute_urls(relative_urls)
            domain_urls = fetch.filter_domain_urls(absolute_urls)

            domain_urls = set(domain_urls)
            domain_urls = domain_urls - set(self.visited_urls)

            self.add_next_urls(domain_urls)

        else:
            self.crawler_stats.errors += 1

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

    scheduler = Scheduler(args.url, args.delay, args.threads, args.limit)
    scheduler.get_url_response()
    crawl_stats = scheduler.crawl_parallel()
    crawl_stats.print_crawler_report(start_time)


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


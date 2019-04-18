import argparse
from urllib.parse import urljoin, urlparse
from multiprocessing import Pool, Manager
from lxml import html
import time

import requests


class Crawler:
    def __init__(self, base_url, delay, threads, max_urls_limit):
        self.base_url = base_url
        self.delay = delay
        self.threads = threads
        self.max_urls_limit = max_urls_limit
        self.extracted_urls = Manager().list([base_url])
        self.visited_urls = Manager().list()
        self.total_bytes_downloaded = Manager().Value('value', 0)
        self.total_pages_crawled = Manager().Value('value', 0)
        self.total_errors = Manager().Value('value', 0)

    def parse_url_response(self, url):
        self.extracted_urls.remove(url)

        if url not in self.visited_urls:
            self.visited_urls.append(url)

        if (len(self.visited_urls) <= self.max_urls_limit):
            raw_response = requests.get(url)
            time.sleep(self.delay)

            if raw_response.status_code == 200:
                self.total_bytes_downloaded.value += len(raw_response.text)
                self.total_pages_crawled.value += 1

                response = html.fromstring(raw_response.text)
                relative_urls = response.xpath('//a[contains(@href, "/")]/@href')

                for url in relative_urls:
                    if 'http' in url and self.base_url in url and url not in self.visited_urls and url not in self.extracted_urls:
                        self.extracted_urls.append(url)
                    elif 'http' not in url:
                        absolute_url = urljoin(self.base_url, url)
                        if absolute_url not in self.visited_urls and absolute_url not in self.extracted_urls:
                            self.extracted_urls.append(absolute_url)
            else:
                self.total_errors.value += 1

    def crawl_parallel(self):
        p = Pool(self.threads)
        p.map(self.parse_url_response, self.extracted_urls)
        p.terminate()
        p.join()

    def print_crawler_report(self, start_time):
        total_crawl_time = time.time() - start_time
        print("Total bytes downloaded: {}".format(self.total_bytes_downloaded.value))
        print("Total pages crawled: {}".format(self.total_pages_crawled.value))
        print("Average page size: {}".format(self.total_bytes_downloaded.value / self.max_urls_limit))
        print("Total crawel time: {}".format(total_crawl_time))
        print("Total Errors: {}".format(self.total_errors.value))


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-u', '--url', type=validate_url,
                            help='Enter site url --Input format: https://website.com/ ')
    arg_parser.add_argument('-d', '--delay', type=int, help='Enter delay time ')
    arg_parser.add_argument('-t', '--threads', type=int, help='Enter concurrent call requests')
    arg_parser.add_argument('-l', '--limit', type=int, help='Total urls to visit limit')

    try:
        args = arg_parser.parse_args()
        start_time = time.time()

        crawler = Crawler(args.url, args.delay, args.threads, args.limit)
        crawler.parse_url_response(args.url)
        crawler.crawl_parallel()
        crawler.print_crawler_report(start_time)

    except argparse.ArgumentTypeError:
        arg_parser.print_help()


def validate_url(url):
    if urlparse(url).netloc and urlparse(url).scheme:
        return url
    else:
        raise argparse.ArgumentTypeError('{0} is not a valid url'.format(url))


if __name__ == '__main__':
    main()

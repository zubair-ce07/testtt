import argparse
import requests
from parsel import Selector
from urllib import parse
from requests.compat import urljoin

from concurrent_crawler import CrawlerResults
from concurrent_crawler import ConcurrentCrawler


def extract_urls(start_url):
    selector = Selector(requests.get(start_url).text)
    extracted_urls = selector.css("a::attr(href)").extract()
    return extracted_urls


def filter_urls(start_url, extracted_urls, max_reqs):
    domain = parse.urlparse(start_url).netloc
    filtered_urls = [urljoin(start_url, url)
                     for url in extracted_urls if parse.urlparse(url).netloc == domain]
    return filtered_urls[:max_reqs]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("starting_url", type=str,
                        help="Url to start crawling with")
    parser.add_argument("-r", "--concurrent_requests", type=int, default=5)
    parser.add_argument("-d", "--download_delay", type=int, default=2)
    parser.add_argument(
        "-n", "--maximum_requests", type=int, default=50)
    return parser.parse_args()


def print_results(crawl_report):
    print(f'Total bytes: {crawl_report.total_bytes}\nTotal requests: {crawl_report.total_requests}\nAverage page size:'
          f'{round(crawl_report.total_bytes/crawl_report.total_requests, 2)} bytes')


def main():

    args = parse_arguments()

    max_reqs = args.maximum_requests

    conc_reqs = args.concurrent_requests

    download_delay = args.download_delay

    start_url = args.starting_url

    extracted_urls = extract_urls(start_url)

    filtered_urls = filter_urls(start_url, extracted_urls, max_reqs)

    conc_crawler = ConcurrentCrawler(download_delay, conc_reqs)

    conc_crawler.start_crawler(filtered_urls)

    print_results(conc_crawler.crawler_results)


if __name__ == "__main__":
    main()

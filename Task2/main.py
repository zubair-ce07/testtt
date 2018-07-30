import argparse

import validators

from concurrent_spider import ConcurrentSpider


def validate_url(url):
    if not validators.url(url):
        raise argparse.ArgumentTypeError(f"The url: {url} is not valid")
    return url


def validate_positive_input(value):
    value = float(value)
    if value < 0:
        raise argparse.ArgumentTypeError(f"The value: {value} should be greater than zero")
    return value


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("site_to_crawl", help="This arg stores the link of the site to Crawl", type=validate_url)
    parser.add_argument("urls_limit", help="Total number of urls to visit", type=validate_positive_input)
    parser.add_argument("download_delay", help="Amount of delay in consecutive downloads", type=validate_positive_input)
    parser.add_argument("concurrency", help="Total number of concurrent requests", type=validate_positive_input)
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    spider = ConcurrentSpider(arguments.site_to_crawl, arguments.download_delay, int(arguments.concurrency))
    spider.run(int(arguments.urls_limit), arguments.site_to_crawl)
    spider.print_stats()


if __name__ == '__main__':
    main()

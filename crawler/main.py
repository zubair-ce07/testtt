import argparse

import validators

from crawler import Crawler


def validate_url(url):
    if validators.url(url):
        return url
    raise argparse.ArgumentTypeError("Not a valid URL")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Report will be generated according to the Arguments')
    parser.add_argument('url', type=validate_url, help='Enter the starting url')
    parser.add_argument('-c', '--concurrency', type=int, help='Maximum No of Concurrent Requests', required=True)
    parser.add_argument('-d', '--download_delay', type=float, help='Download Delay', required=True)
    parser.add_argument('-l', '--max_visits_limit', type=int, help='Maximum no. of urls limit', required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()
    crawler = Crawler(args.url, args.max_visits_limit, args.concurrency, args.download_delay)
    crawler.run()


if __name__ == '__main__':
    main()

import argparse

from crawler import *


def main():
    arg_parser = argparse.ArgumentParser(description='Process some date')
    arg_parser.add_argument('url', type=validate_url,
                            help='Domain to crawl')
    arg_parser.add_argument('concurrent_request', type=int,
                            help='Number of Concurrent Request in one go')
    arg_parser.add_argument('delay', type=float,
                            help='Delay time each user gets')
    arg_parser.add_argument('total_urls', type=int,
                            help='Maximum number of urls to visit)')
    args = arg_parser.parse_args()
    sp = SprinterSpider(args.url, args.concurrent_request, args.delay,
                     args.total_urls)
    url = "https://www.sprinter.es/"
    sp = SprinterSpider(url, args.concurrent_request, args.delay,
                        args.total_urls)
    sp.crawl()


def validate_url(url):
    if parse.urlparse(url).scheme:
        return url
    raise argparse.ArgumentTypeError('url is not valid')


if __name__ == "__main__":
    main()
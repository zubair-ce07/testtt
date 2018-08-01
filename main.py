import argparse

from crawler import *


def main():
    # arg_parser = argparse.ArgumentParser()
    # arg_parser.add_argument('concurrent_request', type=int,
    #                         help='Number of Concurrent Request in one go')
    # arg_parser.add_argument('delay', type=float,
    #                         help='Delay time each user gets')
    # arg_parser.add_argument('total_pages', type=int,
    #                         help='Maximum number of pages to visit)')
    # args = arg_parser.parse_args()
    url = "https://www.sprinter.es/"
    sp = SprinterSpider(url, 1, 0.5, 2)
    # sp = SprinterSpider(url, args.concurrent_request, args.delay,
    #                     args.total_pages)
    sp.crawl()


if __name__ == "__main__":
    main()

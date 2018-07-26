import argparse

from concurrent_spider import ConcurrentSpider, URLVisitLimit


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads",
                        help="Specify numbers of concurrent connections to maintain", type=int,
                        default=1)
    parser.add_argument("-d", "--download_delay",
                        help="Specify download delay between requests in seconds",
                        type=int, default=0)
    parser.add_argument("-m", "--max_url_limit",
                        help="Specify number of maximum URLs to visit", type=int,
                        default=URLVisitLimit.UNLIMITED.value)
    return parser.parse_args()


def main():
    arguments = parse_arguments()

    concurrent_spider = ConcurrentSpider('https://www.arbisoft.com/', arguments.threads,
                                         arguments.download_delay, arguments.max_url_limit)

    concurrent_spider.run()
    concurrent_spider.print_summary()


if __name__ == '__main__':
    main()

import argparse

from concurrent_crawler import ConcurrentCrawler
from parallel_crawler import ParallelCrawler
from validators import validate_url_as_arg


def print_stats(stats):
    print(f'Total requests made: {stats.requests_made}')
    print(f'Total bytes downloaded: {stats.bytes_downloaded} bytes')
    print(f'Average page size: {round(stats.average_page_size, 2)} bytes')


def main():
    args = initialize_arguments()

    params = {
        'url': args.starting_url,
        'count': 100 if args.count is None else args.count,
        'workers': 10 if args.workers is None else args.workers,
        'delay': 0 if args.delay is None else args.delay
    }

    if args.parallel:
        stats = ParallelCrawler(params).crawl()
        print_stats(stats)

    if args.concurrent:
        stats = ConcurrentCrawler(params).crawl()
        print_stats(stats)


def initialize_arguments():
    description = 'This program can crawls a website both recursively and in parallel. User can specify different ' \
                  'options to customize the crawling process'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('starting_url',
                        type=validate_url_as_arg,
                        help='Url of the starting page')

    parser.add_argument('--delay',
                        type=int,
                        help='Download delay between 2 requests')

    parser.add_argument('--count',
                        type=int,
                        help='Number of requests to make')

    parser.add_argument('--workers',
                        type=int,
                        help='Number of concurrent requests that can be made')

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--parallel',
                       help='Crawl the given website through parallel approach',
                       action='store_true')

    group.add_argument('--concurrent',
                       help='Crawl the given website through concurrent approach',
                       action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    main()

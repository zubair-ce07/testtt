import argparse
import sys
import asyncio
import time
from request_parser import RequestParser


def valid_url_count(url_count):
    if 1 <= int(url_count) <= 100:
        return url_count
    raise ValueError()


def crawler_report(pages, start_time, end_time):
    requests_count = len(pages)
    pages_sum = sum([value.page_size for value in pages])
    print(f'Number of URL Traversed: {requests_count}')
    print(f'Sum of page sizes: {pages_sum}')
    print(f'Avg page size: {int(pages_sum / requests_count)}')
    print(f'Time Taken: {end_time - start_time}s \n')


def recursive_concurent_crawler(request_parser):
    start_time = time.time()
    print('Recursive Concurrent Crawling')
    request_parser.recursive_concurent_crawler()
    end_time = time.time()
    crawler_report(request_parser.traversed_pages, start_time, end_time)


def recursive_parallel_crawler(request_parser):
    start_time = time.time()
    print('Recursive Parallel Crawling')
    request_parser.recursive_parallel_crawler()
    end_time = time.time()
    crawler_report(request_parser.traversed_pages, start_time, end_time)


def iterative_concurrent_crawler(request_parser):
    start_time = time.time()
    print('Ietrative Concurent Crawling')
    request_parser.iterative_concurrent_crawl()
    end_time = time.time()
    crawler_report(request_parser.traversed_pages, start_time, end_time)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-d', type=float, nargs='?', default=0.0, help="Time(ms) for download delay")
    parser.add_argument('-r', type=int, nargs='?', default=1, help="Number of requests")
    parser.add_argument('-l', type=valid_url_count, nargs='?', default=5, help="Max URL to crawl")
    args = parser.parse_args()
    request_parser = RequestParser(args.url, int(args.l), int(args.r), int(args.d))
    recursive_concurent_crawler(request_parser)
    recursive_parallel_crawler(request_parser)
    iterative_concurrent_crawler(request_parser)


if __name__ == '__main__':
    main()

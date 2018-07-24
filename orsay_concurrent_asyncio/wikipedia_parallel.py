import argparse
import time
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import urljoin

import requests
from parsel import Selector


def process_requests(start_url, parallel_requests, max_requests, total_bytes):
    response = requests.get(start_url)
    response = Selector(response.text)
    urls = response.css('.mw-parser-output a:not([href*="#"])::attr(href)').extract()
    urls = urls[:max_requests]
    with ThreadPoolExecutor(max_workers=parallel_requests) as executor:
        future_to_url = {executor.submit(process_results, urljoin(start_url, url)) for url in urls}
        for future in as_completed(future_to_url):
            total_bytes += future.result()
    return total_bytes


def process_results(url):
    print('{}'.format(url))
    response = requests.get(url)
    return int(response.headers['content-length'])


def print_results(parallel_requests, max_requests, total_time):
    print('\nParallel Threads: {}'.format(parallel_requests))
    print('Total Requests: {}'.format(max_requests))
    print('Total Bytes downloaded: {} bytes'.format(total_bytes))
    print('Average Page Size: {} bytes'.format('{:.2f}'.format(total_bytes / max_requests)))
    print('Time Taken: {} seconds'.format('{:.1f}'.format(total_time)))


def arg_parser():
    parser = argparse.ArgumentParser(description='Parallel Task')
    parser.add_argument('-p', nargs=1, default=['5'], help='Number of Parallel Requests to handle')
    parser.add_argument('-r', nargs=1, default=['50'], help='Total number of url to request')
    return parser.parse_args()


if __name__ == '__main__':
    parsed_args = arg_parser()
    start_url = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'
    max_requests = int(parsed_args.r[0])
    parallel_requests = int(parsed_args.p[0])
    start_time = time.time()
    total_bytes = process_requests(start_url, parallel_requests, max_requests, 0)
    total_time = time.time() - start_time
    print_results(parallel_requests, max_requests, total_time)

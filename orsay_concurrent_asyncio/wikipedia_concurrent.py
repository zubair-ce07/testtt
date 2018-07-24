import argparse
import asyncio
import time

import requests
from parsel import Selector
from requests.compat import urljoin


def process_requests(start_url, parallel_requests, max_requests, delay, total_bytes):
    response = requests.get(start_url)
    response = Selector(response.text)
    urls = response.css('.mw-parser-output a:not([href*="#"])::attr(href)').extract()
    for counter in range(0, max_requests, parallel_requests):
        if counter+parallel_requests > max_requests:
            temp_urls = urls[counter:max_requests]
        else:
            temp_urls = urls[counter:counter+parallel_requests]
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(None, requests.get, urljoin(start_url, url)) for url in temp_urls]
        results = loop.run_until_complete(asyncio.gather(*futures))
        for result in results:
            total_bytes += process_result(result)
        asyncio.sleep(delay)
    return total_bytes


def process_result(result):
    print('{}'.format(result.url))
    return int(result.headers['content-length'])


def print_results(max_requests, parallel_requests, delay, total_bytes,total_time):
    print('\nParallel Tasks: {}'.format(parallel_requests))
    print('Total Requests: {}'.format(max_requests))
    print('Delay between Requests: {} Seconds'.format(delay))
    print('Total Bytes downloaded: {} bytes'.format(total_bytes))
    print('Average Page Size: {} bytes'.format('{:.2f}'.format(total_bytes / max_requests)))
    print('Time Taken: {} seconds'.format('{:.1f}'.format(total_time)))


def arg_parser():
    parser = argparse.ArgumentParser(description='Concurrent Task')
    parser.add_argument('-p', nargs=1, default=['5'], help='Number of Parallel Requests to handle')
    parser.add_argument('-r', nargs=1, default=['50'], help='Total number of url to request')
    parser.add_argument('-d', nargs=1, default=['2'], help='Total number of seconds to wait between request')
    return parser.parse_args()


if __name__ == '__main__':
    parsed_args = arg_parser()
    start_url = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'
    max_requests = int(parsed_args.r[0])
    parallel_requests = int(parsed_args.p[0])
    delay = int(parsed_args.d[0])
    start_time = time.time()
    total_bytes = process_requests(start_url, parallel_requests, max_requests, delay, 0)
    total_time = time.time() - start_time
    print_results(max_requests, parallel_requests, delay, total_bytes, total_time)

import argparse
import time
import asyncio
import requests
from parsel import Selector
from urllib import parse
from requests.compat import urljoin


def parse_raw_url(start_url, conc_reqs, delay, max_reqs):
    selector = Selector(requests.get(start_url).text)
    extracted_urls = selector.css("a::attr(href)").extract()
    absolute_urls = [urljoin(start_url, url)
                     for url in extracted_urls if not parse.urlparse(url).scheme == 'mailto']

    q, r = divmod(max_reqs, conc_reqs)
    if r:
        url_sets = [absolute_urls[i:i+conc_reqs]
                    for i in range(0, max_reqs, conc_reqs)] + [absolute_urls[q*r:max_reqs]]
    else:
        url_sets = [absolute_urls[i:i+conc_reqs]
                    for i in range(0, max_reqs, conc_reqs)]

    total_bytes = 0
    total_requests = 0
    for url_set in url_sets:
        loop = asyncio.get_event_loop()
        future = [loop.run_in_executor(None, requests.get, url)
                  for url in url_set]
        results = loop.run_until_complete(asyncio.gather(*future))
        total_bytes, total_requests = calculate_results(
            results, total_bytes, total_requests)
        asyncio.sleep(delay)
    return total_bytes, total_requests


def calculate_results(results, total_bytes, total_requests):
    for result in results:
        total_bytes += len(result.text)
        total_requests += 1
    return total_bytes, total_requests


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("starting_url", type=str,
                        help="Url to start crawling with")
    parser.add_argument("-r", "--concurrent_requests", type=int, default=5)
    parser.add_argument("-d", "--download_delay", type=int, default=2)
    parser.add_argument(
        "-n", "--maximum_number_of_requests", type=int, default=50)
    return parser.parse_args()


def print_results(total_time, total_bytes, total_requests):
    print(f'Total bytes: {total_bytes}\nTotal requests: {total_requests}\nAverage page size:'
          f'{total_bytes/total_requests} bytes\nTotal time: {total_time}s')


def main():

    args = parse_arguments()
    start_url = args.starting_url
    start_time = time.time()
    total_bytes, total_requests = parse_raw_url(start_url, args.concurrent_requests,
                                                args.download_delay, args.maximum_number_of_requests)
    total_time = time.time() - start_time
    print_results(total_time, total_bytes, total_requests)


if __name__ == "__main__":
    main()

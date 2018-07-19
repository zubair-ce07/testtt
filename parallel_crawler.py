import argparse
import time
import requests
from parsel import Selector
from urllib import parse
from requests.compat import urljoin
import concurrent.futures


def parse_raw_url(start_url, parallel_reqs, delay, max_reqs):
    selector = Selector(requests.get(start_url).text)
    extracted_urls = selector.css("a::attr(href)").extract()
    absolute_urls = [urljoin(start_url, url)
                     for url in extracted_urls if not parse.urlparse(url).scheme == 'mailto']

    q, r = divmod(max_reqs, parallel_reqs)
    if r:
        url_sets = [absolute_urls[i:i+parallel_reqs]
                    for i in range(0, max_reqs, parallel_reqs)] + [absolute_urls[q*r:max_reqs]]
    else:
        url_sets = [absolute_urls[i:i+parallel_reqs]
                    for i in range(0, max_reqs, parallel_reqs)]

    total_bytes = 0
    total_requests = 0
    for url_set in url_sets:
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_reqs) as executor:
            future_to_url = {executor.submit(
                parse_url, url): url for url in url_set}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                total_requests += 1
                try:
                    total_bytes += len(future.result())
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
    return total_bytes, total_requests


def parse_url(url):
    return requests.get(url).text


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("starting_url", type=str,
                        help="Url to start crawling with")
    parser.add_argument("-p", "--parallel_requests", type=int, default=5)
    parser.add_argument("-d", "--download_delay", type=int, default=2)
    parser.add_argument(
        "-n", "--maximum_number_of_requests", type=int, default=50)
    return parser.parse_args()


def print_results(total_time, total_bytes, total_requests):
    print(f'Total bytes: {total_bytes}\nTotal requests: {total_requests}\nAverage page size: '
          f'{total_bytes/total_requests} bytes\nTotal time: {round(total_time,2)}s')


def main():

    args = parse_arguments()
    start_url = args.starting_url
    start_time = time.time()
    total_bytes, total_requests = parse_raw_url(start_url, args.parallel_requests,
                                                args.download_delay, args.maximum_number_of_requests)
    total_time = time.time() - start_time
    print_results(total_time, total_bytes, total_requests)


if __name__ == "__main__":
    main()

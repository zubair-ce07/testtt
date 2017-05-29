from urllib.parse import urljoin
import concurrent.futures

import requests
import time
from parsel import Selector
import argparse
import sys

parse_url = 'https://www.pakwheels.com/used-cars/search/-/mk_toyota/md_corolla/ct_lahore/'
workers = 10
download_delay = 0.01


def get_all_urls(url_link):
    fetched_html = requests.get(url_link, timeout=20)
    sel = Selector(text=fetched_html.text)
    urls = sel.css('div.col-md-9.grid-style a::attr(href)')

    complete_urls = []
    for url in urls:
        url = urljoin(url_link, url.extract())
        complete_urls.append(url)
    return complete_urls


def fetch_url_data(url_link):
    time.sleep(download_delay)
    try:
        fetched_html = requests.get(url_link, timeout=10.0)
        return len(fetched_html.text)
    except:
        return 0


def fetch_child_urls(urls):
    fetched_bytes = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for bytes_length in executor.map(fetch_url_data, urls):
            fetched_bytes = fetched_bytes + bytes_length

    return fetched_bytes


def check_negative_inputs(num1, num2, num3):
    if (num1 and num1 < 0) or (num2 and num2 < 0) or (num3 and num3 < 0):
        # only verifies a negative input if present
        return True
    else:
        return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parallel downloading program')

    parser.add_argument('-n', '--concurrent_requests',
                        help='number of threads',
                        type=int)
    parser.add_argument('-t', '--download_delay',
                        help='timeout for web request',
                        type=float)
    parser.add_argument('-m', '--maxurls',
                        help='number of maxurls',
                        type=int)

    args = parser.parse_args()
    if check_negative_inputs(args.concurrent_requests, args.download_delay, args.maxurls):
        # exit script if any value is negative, as all input should either is none or non-negative
        print ("Please provide positive inputs")
        sys.exit()

    # assigning input values or default values
    workers = args.concurrent_requests or 10
    download_delay = args.download_delay or 0.01
    max_urls = args.maxurls or 99999

    urls = get_all_urls(parse_url)
    if len(urls) > max_urls:
        # limiting the number of urls to be crawled
        urls = urls[0:max_urls]

    total_bytes = fetch_child_urls(urls)

    print("total bytes: ", total_bytes)
    print("total requests: ", len(urls)+1)
    print("average size per page: ", round(total_bytes/(len(urls)+1), 0))


import argparse
import asyncio
import sys
import time
from urllib.parse import urljoin

import aiohttp
import requests
from parsel import Selector


parse_url = 'https://www.pakwheels.com/used-cars/search/-/mk_toyota/md_corolla/ct_lahore/'

default_max_urls = 99999
default_concurrent_requests = 10
default_download_delay = 0.0001


def get_all_urls(url_to_parse):
    fetched_html = requests.get(url_to_parse)
    sel = Selector(text=fetched_html.text)
    partial_urls = sel.css('div.col-md-9.grid-style a::attr(href)').extract()
    complete_urls = [urljoin(url_to_parse, url) for url in partial_urls]
    return complete_urls


async def fetch_child_urls(urls_to_fetch):
    connector = aiohttp.TCPConnector(verify_ssl=False)
    total_bytes = 0
    for url in urls_to_fetch:
        time.sleep(download_delay)
        try:
            response = await aiohttp.request('get', url, connector=connector)
        except Exception as e:
            print('bad link %s: %s' % (url, e))
        else:
            total_bytes += len(await response.text())
    connector.close()
    return total_bytes


def validate_args(concurrent_requests, download_delay, max_urls):
    return concurrent_requests >= 0 and download_delay >= 0 and max_urls >= 0


def parse_arguments():
    parser = argparse.ArgumentParser(description='Parallel downloading program')

    parser.add_argument('-n', '--concurrent_requests',
                        help='number of threads',
                        default=default_concurrent_requests,
                        type=int)
    parser.add_argument('-t', '--download_delay',
                        help='timeout for web request',
                        default=default_download_delay,
                        type=float)
    parser.add_argument('-m', '--max_urls',
                        help='number of max_urls',
                        default=default_max_urls,
                        type=int)
    return parser.parse_args()


def display_report(downloaded_bytes, num_urls):
    print("total_bytes: ", downloaded_bytes)
    print("total requests: ", num_urls)
    print("average size per page: ", round(downloaded_bytes / num_urls, 0))


if __name__ == '__main__':

    args = parse_arguments()
    if not validate_args(args.concurrent_requests, args.download_delay, args.max_urls):
        print("Please provide positive inputs")
        sys.exit()

    workers = args.concurrent_requests
    download_delay = args.download_delay

    urls = get_all_urls(parse_url)
    if len(urls) > args.max_urls:
        urls = urls[0:args.max_urls]

    total_bytes_downloaded = asyncio.get_event_loop().run_until_complete(fetch_child_urls(urls))
    display_report(total_bytes_downloaded, len(urls))

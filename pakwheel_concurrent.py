import argparse
import asyncio
import sys
import time
from urllib.parse import urljoin

import aiohttp
import requests
from parsel import Selector


parse_url = 'https://www.pakwheels.com/used-cars/search/-/mk_toyota/md_corolla/ct_lahore/'

default_concurrency = 99999
default_concurent_requests = 10
default_download_delay = 0.001


def get_all_urls(url_link):
    fetched_html = requests.get(url_link)
    sel = Selector(text=fetched_html.text)
    partial_urls = sel.css('div.col-md-9.grid-style a::attr(href)')
    complete_urls = [urljoin(url_link, url.extract()) for url in partial_urls]
    return complete_urls


async def fetch_child_urls(urls):
    connector = aiohttp.TCPConnector(verify_ssl=False)
    total_bytes = 0
    for url in urls:
        time.sleep(download_delay)
        try:
            r = await aiohttp.request('get', url, connector=connector)
        except Exception as e:
            print('bad link %s: %s' % (url, e))
        else:
            total_bytes += len(await r.text())
    connector.close()
    return total_bytes


def validate_args(num1, num2, num3):
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
    if validate_args(args.concurrent_requests, args.download_delay, args.maxurls):
        # exit script if any value is negative, as all input should either is none or non-negative
        print("Please provide positive inputs")
        sys.exit()

    workers = args.concurrent_requests or default_concurent_requests
    download_delay = args.download_delay or default_download_delay
    max_urls = args.maxurls or default_concurrency

    urls = get_all_urls(parse_url)
    if len(urls) > max_urls:
        urls = urls[0:max_urls]

    total_bytes_downloaded = asyncio.get_event_loop().run_until_complete(fetch_child_urls(urls))

    print("total_bytes: ", total_bytes_downloaded)
    print("total requests: ", len(urls))
    print("average size per page: ", round(total_bytes_downloaded/(len(urls)), 0))


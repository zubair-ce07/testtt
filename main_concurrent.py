import argparse
import asyncio

import requests
from parsel import Selector


async def get_links(url, timeout_):
    links = []
    response = requests.get(url, timeout=timeout_)
    sel = Selector(response.text)
    data = sel.css('a[href^="http"]::attr(href)')
    for link in data:
        links.append(link.extract())
    return links


async def get_result(url_list, index, count, max_urls, timeout_):
    if index < len(url_list) and url_list[index] and count < max_urls:
        links = await get_links(url_list[index], timeout_);
        for link in links:
            url_list.append(link)
        bytesdownloaded = len(links)
        index += 1
        count += 1
        return bytesdownloaded + await  get_result(url_list, index, count, max_urls, timeout_)
    else:
        return 0


async def print_report(url_list, index, count, max_urls, timeout_):
    bytesdownloaded = await  get_result(url_list, index, count, max_urls, timeout_)
    if max_urls > len(url_list):
        max_urls = len(url_list)
    print("Total requests made are {0}".format(max_urls))
    print("Total bytes downloaded are {0}".format(bytesdownloaded))
    print("Average size of a page is {0}".format(bytesdownloaded / max_urls))


def main():
    links = ['https://en.wikipedia.org/wiki/Constitution_of_Pakistan']
    parser = argparse.ArgumentParser(
        description='Script retrieves Commands from User')
    parser.add_argument(
        '-m', '--max_urls', type=str, help='Maximum Urls', required=True)
    parser.add_argument(
        '-d', '--delay', type=str, help='tolerate download delay', required=True)
    args = parser.parse_args()

    max_urls = int(args.max_urls)
    index = 0
    count = 0
    timeout_ = int(args.delay)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_report(links, index, count, max_urls,
                                         timeout_))
    loop.close()


if __name__ == "__main__":
    main()

import argparse
import concurrent.futures

import requests
from parsel import Selector


def get_links(url, timeout_):
    links = []
    response = requests.get(url, timeout=timeout_)
    sel = Selector(response.text)
    data = sel.css(' a[href^="http"]::attr(href)  ')
    for link in data:
        links.append(link.extract())
    return links


def visit_links_parallel(url_list, index, count, max_urls, timeout_, max_worker):
    if index < len(url_list) and url_list[index] and count < max_urls:
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_worker) as executor:
            future = executor.submit(get_links, url_list[index], timeout_)
            try:
                data = future.result()
            except Exception as exc:
                print('{0} generated an exception: {1}'.format(url_list[index], exc))
            else:
                bytesdownloaded = len(data)
                for link in data:
                    url_list.append(link)
        count += 1
        return bytesdownloaded + visit_links_parallel(url_list, index + 1, count, max_urls,
                                                      timeout_, max_worker)
    return 0


def print_report(url_list, index, count, max_urls, timeout_, max_worker):
    bytesdownloaded = visit_links_parallel(url_list, index, count, max_urls, timeout_, max_worker)
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
    parser.add_argument(
        '-c', '--concurrent_requests', type=str, help='Concurrent requests made', required=True)
    args = parser.parse_args()

    max_urls = int(args.max_urls)
    index = 0
    count = 0
    timeout_ = int(args.delay)
    max_worker = int(args.concurrent_requests)
    print_report(links, index, count, max_urls, timeout_, max_worker)


if __name__ == "__main__":
    main()

import argparse
import asyncio
import concurrent.futures
import re
import requests
import time

from parsel import Selector
from statistics import mean
from urllib.parse import urlparse, urljoin


concurrent_site_sizes = []


def is_valid_url(url):
    http_request = requests.head(url)
    if http_request.status_code == 200:
        return url
    else:
        exit('Website not accessible')


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_url', type=is_valid_url)
    parser.add_argument('-c', '-concurrent', nargs='+', help='Type the commands in '
                                                             'the format: -c (max urls)'
                                                             ' (concurrent requests) (download delay)')
    parser.add_argument('-p', '-parallel', type=int, nargs='+', help='Type the commands in '
                                                           'the format: -p (max urls) (max workers)')
    return parser.parse_args()


def get_anchor_urls(start_url, max_urls):
    parsed_url = urlparse(start_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    raw_html = requests.get(start_url)
    html_selector = Selector(raw_html.text)
    href_links = html_selector.xpath('//a/@href').getall()
    final_href_links = []
    for href in href_links:

        if len(final_href_links) == max_urls:
            break
        elif re.match(r'http', href):
            final_href_links.append(href)
        elif re.match(r'/', href):
            final_href_links.append(urljoin(base_url, href))
        else:
            continue
    return final_href_links


async def concurrent_page_download(url, download_delay, bounded_semaphore):
    async with bounded_semaphore:
        print(f"Downloading the URL {url}")
        downloaded_content = requests.get(url)
        await asyncio.sleep(download_delay)
        concurrent_site_sizes.append(len(downloaded_content.content))
        return concurrent_site_sizes


async def concurrent_processing(start_url, maximum_urls, concurrent_requests, download_delay):
    starting_time = time.time()
    bounded_semaphore = asyncio.BoundedSemaphore(concurrent_requests)
    url_list = get_anchor_urls(start_url, maximum_urls)
    concurrent_tasks = [concurrent_page_download(url, download_delay, bounded_semaphore) for url in url_list]
    await asyncio.gather(*concurrent_tasks)
    ending_time = time.time()
    print(f"Concurrent requests time taken is {round(ending_time-starting_time,2)} seconds with "
          f"{concurrent_requests} concurrent requests and {download_delay} download delay")
    return concurrent_tasks


def parallel_page_download(url):
    print(f"Downloading the URL {url}")
    downloaded_content = requests.get(url)
    return len(downloaded_content.content)


def parallel_processing(start_url, maximum_urls, max_workers):
    parallel_site_sizes = []
    starting_time = time.time()
    url_list = get_anchor_urls(start_url, maximum_urls)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as worker:
        futures = {worker.submit(parallel_page_download, url) for url in url_list}
        concurrent.futures.wait(futures)
        for future in futures:
            parallel_site_sizes.append((future.result()))
    ending_time = time.time()
    print(f"Parallel requests time taken is {round(ending_time - starting_time,2)} "
          f"seconds with {max_workers} maximum workers")
    return parallel_site_sizes


def report_generator(site_sizes):
    print(f"Total number of website visits are: {len(site_sizes)}")
    print(f"Total bytes downloaded are: {sum(site_sizes)} Bytes / {sum(site_sizes)/1000} Kilobytes")
    print(f"Average size of a page is : {round(mean(site_sizes),2)} Bytes / {round(mean(site_sizes)/1000,2)} Kilobytes")


if __name__ == "__main__":
    input_arguments = arg_parser()
    if input_arguments.c:
        arg_list = input_arguments.c
        loop = asyncio.get_event_loop()
        loop.run_until_complete(concurrent_processing(input_arguments.start_url, int(arg_list[0]),
                                                      int(arg_list[1]), float(arg_list[2])))
        report_generator(concurrent_site_sizes)
    if input_arguments.p:
        arg_list = input_arguments.p
        result_list = parallel_processing(input_arguments.start_url, arg_list[0], arg_list[1])
        report_generator(result_list)

"""Format of commands for parallel: https://website.org -p (max_websites) (max_workers)"""
"""Format of commands for concurrent: htt[s://website.org -c (max urls) (concurrent requests) (download delay)"""
"""Both concurrent and parallel commands can be scheduled in one command line"""

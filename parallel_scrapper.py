import requests
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from time import sleep
from collections import namedtuple


def filter_invalid_urls(urls):
    urls = [url for url in urls if len(url) > 5 or "/" not in url]
    return urls


def fix_url_path(url, origin):
    if url.startswith("//"):
        url = "http:" + url
    if url.startswith("/"):
        url = origin + url

    return url


def hit_target_link(url, results_collections, config, allow_sleep=True, collect_response=True):
    if allow_sleep:
        sleep(config.download_delay)

    print("Hit : %s" % url)
    response = None
    try:
        response = requests.get(url)
        if collect_response:
            results_collections.responses_collection.append(response)
    except ValueError:
        response = None

    return response, results_collections, config


def extract_anchor_tags_link(html):
    parser = Selector(text=html)
    page_links = parser.xpath("//a/@href").extract()
    urls_collection = filter_invalid_urls(page_links)

    return urls_collection


def future_task_finished(future):
    response, results_collections, config = future.result()
    if response:
        urls_collection = extract_anchor_tags_link(response.text)

        recursively_extract_html(urls_collection, config.origin, results_collections, config)


def recursively_extract_html(urls_collection, origin, results_collections, config):
    for target_link in urls_collection:
        if results_collections.number_of_hits >= config.hits_limit:
            break

        target_link = fix_url_path(target_link, origin)
        future_task = config.thread_pool.submit(hit_target_link, target_link, results_collections, config)

        results_collections.number_of_hits += 1
        # future_task.add_done_callback(future_task_finished)
        results_collections.futures_collection.append(future_task)


def main():
    origin = "http://sfbay.craigslist.org"
    url = "http://sfbay.craigslist.org/search/eby/jjj"

    config = namedtuple('Config', "max_number_of_concurrent_requests thread_pool hits_limit download_delay origin")
    config.download_delay = 2
    config.max_number_of_concurrent_requests = 3
    config.hits_limit = 25
    config.thread_pool = ThreadPoolExecutor(max_workers=config.max_number_of_concurrent_requests)
    config.origin = origin

    results_collections = namedtuple("Results", "responses_collection number_of_hits futures_collection processed_urls")
    results_collections.responses_collection = []
    results_collections.futures_collection = []
    results_collections.processed_urls = []
    results_collections.number_of_hits = 0

    response, results_collections, config = hit_target_link(url, results_collections, config, False, False)
    urls_collection = extract_anchor_tags_link(response.text)

    recursively_extract_html(urls_collection, origin, results_collections, config)
    for future in concurrent.futures.as_completed(results_collections.futures_collection):
        response, results_collections, config = future.result()
        if response:
            parser = Selector(text=response.text)
            page_links = parser.xpath("//a/@href").extract()
            urls_collection = filter_invalid_urls(page_links)

            recursively_extract_html(urls_collection, config.origin, results_collections, config)

    total_requests = config.hits_limit
    content_size_collection = sum([len(response.content) for response in results_collections.responses_collection])

    print("Total Requests: %s\nTotal Data Bytes: %s\nAverage Page Size: %s" %
          (total_requests, content_size_collection, content_size_collection / total_requests))


if __name__ == '__main__':
    main()

import requests
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from time import sleep
from collections import namedtuple


def filter_invalid_urls(urls):
    urls = [url for url in urls if len(url) > 5]
    return urls


def fix_url_path(url, origin):
    if url.startswith("//"):
        url = "http:" + url
    if url.startswith("/"):
        url = origin + url

    return url


def hit_target_link(url, results_collections, config):
    sleep(config.download_delay)

    print("Hit #: %s | %s" % (results_collections.number_of_hits, url))
    response = requests.get(url)

    results_collections.responses_collection.append(response)

    return response, results_collections, config


def future_task_finished(future):
    response, results_collections, config = future.result()
    parser = Selector(text=response.text)
    page_links = parser.xpath("//a/@href").extract()
    urls_collection = filter_invalid_urls(page_links)

    recursively_extract_html(urls_collection, config.origin, results_collections, config)
    print("FINISHED......")


def recursively_extract_html(urls_collection, origin, results_collections, config):
    for target_link in urls_collection:
        if results_collections.number_of_hits >= config.hits_limit:
            break

        target_link = fix_url_path(target_link, origin)

        future_task = config.thread_pool.submit(hit_target_link, target_link, results_collections, config)
        future_task.add_done_callback(future_task_finished)
        results_collections.number_of_hits += 1


def main():
    origin = "http://sfbay.craigslist.org"
    url = "http://sfbay.craigslist.org/search/eby/jjj"

    config = namedtuple('Config', "max_number_of_concurrent_requests thread_pool hits_limit download_delay origin")
    config.download_delay = 2
    config.max_number_of_concurrent_requests = 2
    config.hits_limit = 5
    config.thread_pool = ThreadPoolExecutor(max_workers=config.max_number_of_concurrent_requests)
    config.origin = origin

    results_collections = namedtuple("Results", "responses_collection number_of_hits futures_collection processed_urls")
    results_collections.responses_collection = []
    results_collections.futures_collection = []
    results_collections.processed_urls = []
    results_collections.number_of_hits = 0

    urls_collection = [url]

    recursively_extract_html(urls_collection, origin, results_collections, config)

    print("YYYYYYYYYYYp")

    # print("Total Requests: %s\nTotal Data Bytes: %s\nAverage Page Size: %s" % (len(page_lengths),sum(page_lengths),
    #                                                                            sum(page_lengths) / len(page_lengths)))


if __name__ == '__main__':
    main()

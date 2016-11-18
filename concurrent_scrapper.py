from parsel import Selector
from time import sleep
from collections import namedtuple
import aiohttp


def filter_invalid_urls(urls):
    urls = [url for url in urls if len(url) > 5]
    return urls


def fix_url_path(url, origin):
    if url.startswith("//"):
        url = "http:" + url
    if url.startswith("/"):
        url = origin + url

    return url


async def hit_target_link(url, config):
    sleep(config.download_delay)

    print("Hit : %s" % url)
    response = await aiohttp.ClientSession.get(url)

    return await response


def recursively_extract_html(urls_collection, origin, results_collections, config):
    for target_link in urls_collection:
        if results_collections.number_of_hits >= config.hits_limit:
            break

        target_link = fix_url_path(target_link, origin)
        response = hit_target_link(target_link, config)

        results_collections.number_of_hits += 1


def main():
    origin = "http://sfbay.craigslist.org"
    url = "http://sfbay.craigslist.org/search/eby/jjj"

    config = namedtuple('Config', "max_number_of_concurrent_requests thread_pool hits_limit download_delay origin")
    config.download_delay = 2
    config.hits_limit = 5

    results_collections = namedtuple("Results", "responses_collection number_of_hits futures_collection processed_urls")
    results_collections.responses_collection = []
    results_collections.number_of_hits = 0

    urls_collection = [url]

    recursively_extract_html(urls_collection, origin, results_collections, config)

    # total_requests = len(results_collections.responses_collection)
    # content_size_collection = sum([len(response.content) for response in results_collections.responses_collection])
    #
    # print("Total Requests: %s\nTotal Data Bytes: %s\nAverage Page Size: %s" %
    #       (total_requests, content_size_collection, content_size_collection / total_requests))


if __name__ == '__main__':
    main()

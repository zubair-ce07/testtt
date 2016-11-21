from parsel import Selector
from collections import namedtuple
from aiohttp import ClientSession
import asyncio
import requests


def filter_invalid_urls(urls):
    urls = [url for url in urls if len(url) > 5 and "/" in url]
    return urls


def fix_url_path(url, origin):
    if url.startswith("//"):
        url = "http:" + url
    if url.startswith("/"):
        url = origin + url

    return url


def hit_target_link_normal(url):
    response = requests.get(url)
    return response.text


async def hit_target_link(url, config):
    await asyncio.sleep(config.download_delay)
    print("Hit : %s" % url)

    response = None
    async with ClientSession() as session:
        try:
            async with session.get(url) as response:
                response = await response.read()
        except ValueError:
            response = None

    return response


def extract_pages_link(html, urls_to_remove=[]):
    parser = Selector(text=html)
    page_links = parser.xpath("//a/@href").extract()
    urls_collection = filter_invalid_urls(page_links)

    urls_collection = list(set(urls_collection) - set(urls_to_remove))

    return urls_collection


async def recursively_extract_html(urls_collection, origin, results_collections, config):
    for target_link in urls_collection:
        if results_collections.number_of_hits >= config.hits_limit:
            break

        target_link = fix_url_path(target_link, origin)
        if target_link in results_collections.processed_urls:
            continue

        results_collections.processed_urls.append(target_link)
        html = await hit_target_link(target_link, config)

        if not html:
            continue

        results_collections.responses_collection.append(html)
        results_collections.number_of_hits += 1

        new_urls_collection = extract_pages_link(html.decode("utf-8", errors='ignore'), results_collections.processed_urls)
        await results_collections.event_loop.create_task(recursively_extract_html(new_urls_collection, origin,
                                                                                  results_collections, config))


def main():
    origin = "http://sfbay.craigslist.org"
    url = "http://sfbay.craigslist.org/search/eby/jjj"

    config = namedtuple('Config', "max_number_of_concurrent_requests thread_pool hits_limit download_delay origin")
    print("Enter time delay in seconds: ")
    config.download_delay = int(input())
    print("Enter maximum number of urls to visit: ")
    config.hits_limit = int(input())

    results_collections = namedtuple("Results", "responses_collection number_of_hits event_loop processed_urls")
    results_collections.responses_collection = []
    results_collections.processed_urls = []
    results_collections.event_loop = asyncio.get_event_loop()
    results_collections.number_of_hits = 0

    html = hit_target_link_normal(url)
    urls_collection = extract_pages_link(html)

    results_collections.event_loop.run_until_complete(recursively_extract_html(urls_collection, origin,
                                                                               results_collections, config))

    total_requests = len(results_collections.responses_collection)
    content_size_collection = sum([len(response) for response in results_collections.responses_collection])

    print("Total Requests: %s\nTotal Data Bytes: %s\nAverage Page Size: %s" %
          (total_requests, content_size_collection, content_size_collection / total_requests))

main()

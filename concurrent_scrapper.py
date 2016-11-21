from parsel import Selector
from collections import namedtuple
import aiohttp
import asyncio
import time


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
    await asyncio.sleep(config.download_delay)

    print("Hit : %s" % url)
    response = await aiohttp.get(url=url)
    return await response.text()


def extract_pages_link(html):
    parser = Selector(text=html)
    page_links = parser.xpath("//a/@href").extract()
    urls_collection = filter_invalid_urls(page_links)

    return urls_collection


async def recursively_extract_html(urls_collection, origin, results_collections, config):
    for target_link in urls_collection:
        if results_collections.number_of_hits >= config.hits_limit:
            break

        target_link = fix_url_path(target_link, origin)
        html = await hit_target_link(target_link, config)
        results_collections.number_of_hits += 1

        new_urls_collection = extract_pages_link(html)
        await results_collections.event_loop.create_task(recursively_extract_html(new_urls_collection, origin,
                                                                                  results_collections, config))


def main():
    origin = "http://sfbay.craigslist.org"
    url = "http://sfbay.craigslist.org/search/eby/jjj"

    config = namedtuple('Config', "max_number_of_concurrent_requests thread_pool hits_limit download_delay origin")
    config.download_delay = 2
    config.hits_limit = 5

    results_collections = namedtuple("Results", "responses_collection number_of_hits event_loop processed_urls")
    results_collections.responses_collection = []
    results_collections.event_loop = asyncio.get_event_loop()
    results_collections.number_of_hits = 0

    urls_collection = [url]

    results_collections.event_loop.run_until_complete(recursively_extract_html(urls_collection, origin,
                                                                               results_collections, config))

main()

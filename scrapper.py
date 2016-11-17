import requests
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from time import sleep
import pdb


def filter_invalid_urls(urls):
    urls = [url for url in urls if len(url) > 5]
    return urls


def hit_target_link(url, download_delay=0):
    sleep(download_delay)
    response = requests.get(url)
    return response.text, len(response.content)


def recursively_extract_html(urls, origin, hits_limit, page_lengths, thread_pool, thread_collector,
                             download_delay, total_hits=0):
    if urls and total_hits < hits_limit:
        target_link = urls.pop(0)

        if target_link.startswith("//"):
            target_link = "http:" + target_link
        if target_link.startswith("/"):
            target_link = origin + target_link

        future_task = thread_pool.submit(hit_target_link(target_link, download_delay))

        thread_collector.append(future_task)
        total_hits += 1
        print("Total Hits: %s | %s" % (total_hits, target_link))

        for future in concurrent.futures.as_completed(thread_collector):
            response_html, content_size = future.result()
            page_lengths.append(content_size)

            parser = Selector(response_html)

            page_links = parser.xpath("//a/@href").extract()
            urls += filter_invalid_urls(page_links)

            recursively_extract_html(urls, origin, hits_limit, page_lengths, thread_pool, thread_collector,
                                     download_delay, total_hits)


def main():
    origin = "http://sfbay.craigslist.org"
    url = "http://sfbay.craigslist.org/search/eby/jjj"

    hits_limit = 100
    max_number_of_concurrent_requests = 5
    download_delay = 2

    page_lengths = []
    thread_collector = []
    thread_pool = ThreadPoolExecutor(max_number_of_concurrent_requests)

    recursively_extract_html([url], origin, hits_limit, page_lengths, thread_pool, thread_collector, download_delay)

    # print("Total Requests: %s\nTotal Data Bytes: %s\nAverage Page Size: %s" % (len(page_lengths),sum(page_lengths),
    #                                                                            sum(page_lengths) / len(page_lengths)))

if __name__ == '__main__':
    main()

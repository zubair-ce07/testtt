import requests
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from time import sleep
import pdb


def filter_invalid_urls(urls):
    urls = [url for url in urls if len(url) > 5]
    return urls


def hit_target_link(url, download_delay, hit_number):
    sleep(download_delay)
    response = requests.get(url)
    # print("Hit: %s" % (url))
    return response.text, len(response.content), hit_number


def recursively_extract_html(urls, origin, hits_limit, page_lengths, thread_pool, thread_collector,
                             download_delay, total_hits):
    if urls and total_hits < hits_limit:
        print("Hits: %s" % total_hits)

        target_link = urls.pop(0)

        if target_link.startswith("//"):
            target_link = "http:" + target_link
        if target_link.startswith("/"):
            target_link = origin + target_link

        future_task = thread_pool.submit(hit_target_link, target_link, download_delay, total_hits)

        thread_collector.append(future_task)
        total_hits += 1

        for future in concurrent.futures.as_completed(thread_collector):

            response_html, content_size, hit_number = future.result()

            print("Hit#: %s" % hit_number)
            page_lengths.append(content_size)

            parser = Selector(response_html)

            page_links = parser.xpath("//a/@href").extract()
            urls += filter_invalid_urls(page_links)

            recursively_extract_html(urls, origin, hits_limit, page_lengths, thread_pool, thread_collector,
                                     download_delay, total_hits)


def main():
    origin = "http://sfbay.craigslist.org"
    url = "http://sfbay.craigslist.org/search/eby/jjj"

    hits_limit = 3
    max_number_of_concurrent_requests = 2
    download_delay = 2

    page_lengths = []
    thread_collector = []
    thread_pool = ThreadPoolExecutor(max_workers=max_number_of_concurrent_requests)

    recursively_extract_html([url], origin, hits_limit, page_lengths, thread_pool, thread_collector, download_delay, 0)

    # print("Total Requests: %s\nTotal Data Bytes: %s\nAverage Page Size: %s" % (len(page_lengths),sum(page_lengths),
    #                                                                            sum(page_lengths) / len(page_lengths)))

if __name__ == '__main__':
    main()

import requests
from parsel import Selector
import argparse
import asyncio


async def retrieve_bytes(link, timeout_delay):
    url = 'https://arbisoft.com'
    await asyncio.sleep(timeout_delay)
    try:
        if link[0:4] == "http":
            html = requests.get(link, timeout=15).text

        else:
            html = requests.get(url + link, timeout=15).text

        # print(len(html))
        return len(html)
    except:
        return 0


def clean_url_list(links, max_urls):
    for link in links:

        if len(link) <= 1 or len(link) is None:
            links.remove(link)

    links = list(set(links))

    if max_urls < len(links):
        links = links[0:max_urls]

    return links


def retrieve_urls(url):
    html = requests.get(url, timeout=15).text
    selector = Selector(text=html)
    return selector.css('a::attr(href)').extract()


def start_loop(links, thread_count, timeout_delay):

    loop = asyncio.get_event_loop()
    tasks = []
    results = []
    iter = 1
    if len(links) > thread_count:

        for link in links:
            tasks.append(asyncio.ensure_future(retrieve_bytes(link, timeout_delay)))
            if iter % thread_count == 0:
                temp = loop.run_until_complete(asyncio.wait(tasks))
                results = results + list(temp[0])
                tasks.clear()
            iter += 1

        if len(tasks) != 0:
            temp = loop.run_until_complete(asyncio.wait(tasks))
            results = results + list(temp[0])
    else:
        for link in links:
            tasks.append(asyncio.ensure_future(retrieve_bytes(link, timeout_delay)))
        temp = loop.run_until_complete(asyncio.wait(tasks))
        results = results + list(temp[0])

    loop.close()
    total_bytes = 0
    for res in results:
        total_bytes += res.result()

    return total_bytes

    # total_bytes = 0
    # connection_error = 0;
    # pool = ProcessPoolExecutor(thread_count)
    # futures = []
    # for link in links:
    #     futures.append(pool.submit(retrieve_bytes, link, timeout_delay))
    #
    # for future in as_completed(futures):
    #     if future.result == 0:
    #         connection_error += 1
    #     total_bytes += future.result()
    #
    # return total_bytes, connection_error


def display(links, total_bytes):
    print("Total Downloaded bytes : " + str(total_bytes))
    print("Total requests : " + str(len(links)))
    print("Average Page size : " + str(total_bytes/(len(links))))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads",
                        help="number of concurrent requests", type=int)
    parser.add_argument("-o", "--timeout",
                        help="time out delay value to visit", type=int)
    parser.add_argument("-m", "--max_url",
                        help="max number of urls to visit", type=int)
    args = parser.parse_args()

    if not args.threads:
        args.threads = 1
    elif args.threads <= 0:
        print("Please provide a positive number of threads")
        exit()

    if not args.timeout:
        args.timeout = 0
    elif args.timeout < 0:
        print("Please provide a positive timeout")
        exit()

    if not args.max_url:
        args.max_url = 100000
    elif args.max_url <= 0:
        print("Please provide a positive number of max_url")
        exit()

    url = 'https://arbisoft.com'
    links = retrieve_urls(url)
    links = clean_url_list(links, args.max_url)
    total_bytes = start_loop(links, args.threads, args.timeout)
    display(links, total_bytes)


if __name__ == '__main__':
    main()

import requests
from parsel import Selector
import argparse
import asyncio


async def retrieve_bytes(link, timeout_delay):

    await asyncio.sleep(timeout_delay)
    try:
        html = requests.get(link, timeout=15).text
        return len(html)
    except:
        return 0


def clean_url_list(links, max_urls, url):

    for link in links:
        if link is None or len(link) <= 1:
            links.remove(link)
    links = list(set(links))

    if max_urls < len(links):
        links = links[0:max_urls]

    for ids, link in enumerate(links):
        if not link.startswith('http'):
            links[ids] = url+link

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
            temp_results_list = loop.run_until_complete(asyncio.wait(tasks))
            results = results + list(temp_results_list[0])
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


def display(links, total_bytes):
    print("Total Downloaded bytes : {0:.0f}".format(total_bytes))
    print("Total requests : {0:.0f}".format(len(links)))
    print("Average Page size : {0:.0f}".format(total_bytes/(len(links))))


def argument_check(args):

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

    return args.threads, args.timeout, args.max_url


def arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads",
                        help="number of concurrent requests", type=int)
    parser.add_argument("-o", "--timeout",
                        help="time out delay value to visit", type=int)
    parser.add_argument("-m", "--max_url",
                        help="max number of urls to visit", type=int)
    return parser.parse_args()


def main():

    args = arguments()
    threads, timeout, max_url = argument_check(args)
    url = 'https://arbisoft.com'
    links = retrieve_urls(url)
    links = clean_url_list(links, max_url, url)
    total_bytes = start_loop(links, threads, timeout)
    display(links, total_bytes)


if __name__ == '__main__':
    main()

__author__ = 'rabia'
import requests
from lxml import html
import asyncio


def generate_report(urls_data_list, total_bytes, total_requests):
    print("\n\n---------------Report---------------------")
    for item in urls_data_list:
        print("url: " + item['url'])
        print("page bytes: " + str(item['bytes']))

    print("\n\nTotal Requests made: " + str(total_requests))
    print("Total Bytes downloaded: " + str(total_bytes))
    average_size_of_page = total_bytes / total_requests
    print("Average size of Page: " + str(average_size_of_page))


@asyncio.coroutine
def get_url_data(url):
    response = requests.get(url)
    yield from asyncio.sleep(5.0)
    return response


@asyncio.coroutine
def concurrent_crawler():
    urls_data_list = []
    total_bytes = 0
    total_requests = 0

    base_url = "https://en.wikipedia.org/wiki/Data_science"
    response = requests.get(base_url)
    raw_string = html.fromstring(response.text)
    urls = raw_string.xpath("/html/body//a[starts-with(@href,'/wiki/')]/@href")
    urls_list = ['https://en.wikipedia.org' + url for url in urls]

    for url in urls_list[:20]:
        print(url)
        response = yield from get_url_data(url)
        response_size = len(response.text)
        total_requests += 1
        total_bytes += response_size
        urls_data_list.append({'url': url, 'bytes': response_size})

    generate_report(urls_data_list, total_bytes, total_requests)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(concurrent_crawler())
    loop.close()


if __name__ == "__main__":
    main()
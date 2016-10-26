__author__ = 'rabia'
import requests
from lxml import html
import asyncio
import argparse


def generate_report(urls, total_bytes):
    print("\n\n---------------Report---------------------")
    for item in urls:
        print('{} page is {} bytes'.format(item['url'], item['bytes']))

    total_requests = len(urls)
    average_size_of_page = total_bytes / total_requests

    return '\n\n Total Requests made: {} \n Total Bytes downloaded: {} \n Average size of Page: {} '.\
        format(total_requests, total_bytes, average_size_of_page)


async def get_url_data(url, download_delay):
    response = requests.get(url)
    await asyncio.sleep(download_delay)
    return response



async def concurrent_crawler(download_delay):
    site_urls = []
    total_bytes = 0

    base_url = "https://en.wikipedia.org/wiki/Data_science"
    response = requests.get(base_url)
    raw_response = html.fromstring(response.text)
    urls = raw_response.xpath("/html/body//a[starts-with(@href,'/wiki/')]/@href")
    urls_list = ['https://en.wikipedia.org' + url for url in urls]

    for url in urls_list[:20]:
        response = await get_url_data(url, download_delay)
        response_size = len(response.text)
        total_bytes += response_size
        site_urls.append({'url': url, 'bytes': response_size})

    print(generate_report(site_urls, total_bytes))


def main(args):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(concurrent_crawler(args.download_delay))
    loop.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-download_delay', action="store", default=5, type=int, dest='download_delay',
                        help='Download delay between each request')
    main(parser.parse_args())
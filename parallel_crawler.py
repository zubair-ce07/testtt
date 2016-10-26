__author__ = 'rabia'
import concurrent.futures
import requests
import time
from lxml import html
import argparse

def generate_report(urls, total_bytes, no_of_workers):
    print("\n---------------Report---------------------")
    for item in urls:
        print('{} page is {} bytes'.format(item['url'], item['bytes']))

    total_requests = len(urls)
    average_size_of_page = total_bytes / total_requests

    return '\n\n Total Requests made: {} \n Total Bytes downloaded: {} \n Average size of Page: {} \n Max Workers: {}'.\
        format(total_requests, total_bytes, average_size_of_page, no_of_workers)


def get_url_data(url, download_delay):
    response = requests.get(url, download_delay)
    time.sleep(int(download_delay))
    return response


def parallel_crawler(urls, no_of_workers, download_delay):

    site_urls = []
    total_bytes = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=no_of_workers) as executor:
        future_to_url = {executor.submit(get_url_data, url, download_delay): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            response = future.result()
            response_size = len(response.text)
            total_bytes += response_size
            site_urls.append({'url': url, 'bytes': response_size})

        print(generate_report(site_urls, total_bytes, no_of_workers))


def main(args):

    base_url = "https://en.wikipedia.org/wiki/Data_science"
    response = requests.get(base_url)
    raw_response = html.fromstring(response.text)
    response_urls = raw_response.xpath("/html/body//a[starts-with(@href,'/wiki/')]/@href")
    urls = ['https://en.wikipedia.org' + url for url in response_urls]
    urls = urls[:100]

    parallel_crawler(urls, args.no_of_workers, args.download_delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-download_delay', action="store", default=5, type=str, dest='download_delay',
                        help='Download delay between each request')
    parser.add_argument('-no_of_workers', action="store", default=5, type=int, dest='no_of_workers',
                        help='no. of workers for parallel requests')
    main(parser.parse_args())
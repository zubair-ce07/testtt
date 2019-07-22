import argparse
from classes import *
from bs4 import BeautifulSoup
import requests

parser = argparse.ArgumentParser()
parser.add_argument('website', help="the website url you want to crawl", type=str)
parser.add_argument('max_urls',help='maximum urls to visit')
parser.add_argument('concurrent_requests', help='total number of concurrent requests')
parser.add_argument('download_delay', help='download delay')
args = parser.parse_args()


def main():

    urls = get_urls(args.website)
    max_urls = int(args.max_urls)
    concurrent_requests = int(args.concurrent_requests)
    dl_delay = float(args.download_delay)
    concurrent_crawler = RecursiveCrawler(urls, concurrent_requests, max_urls, dl_delay)
    concurrent_crawler.event_loop()
    print(f'\nTotal Number of Requests: {concurrent_crawler.request_count}')
    print(f'Total Bytes Downloaded: {concurrent_crawler.length}')
    print(f'Average File Size: {round(concurrent_crawler.length / max_urls)}')


def get_urls(url):
    url_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    for link in soup.findAll('a'):
        url = link.get('href')
        if re.match('http', str(url)):
            url_list.append(url)
        else:
            continue

    return url_list


if __name__ == '__main__':
    main()
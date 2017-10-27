import argparse

from Functions import get_urls
from Classes import ConcurrentCrawler

parser = argparse.ArgumentParser()
parser.add_argument('website', type=str)
args = parser.parse_args()


def main():

    urls = get_urls(args.website)
    max_threads = 10
    max_urls = 100
    time_delay = 5

    if urls:
        concurrent_crawler = ConcurrentCrawler(urls, max_threads, max_urls, time_delay)
        concurrent_crawler.event_loop()
        average = concurrent_crawler.length / max_urls
        print('\nTotal Requests made: {}'.format(concurrent_crawler.request_count))
        print('Total Bytes Downloaded: {}'.format(concurrent_crawler.length))
        print('Average File Size: {}'.format(average))

    else:
        print('No Urls Extracted From the URL')

if __name__ == '__main__':

    main()
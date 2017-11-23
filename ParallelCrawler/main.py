import argparse

from Function import get_urls
from ParallelCrawrler import ParallelCrawler

parser = argparse.ArgumentParser()
parser.add_argument('website', type=str)
args = parser.parse_args()


def main():

    urls = get_urls(args.website)
    max_threads = 10
    max_urls = 10
    time_delay = 0.1

    if urls:
        crawler = ParallelCrawler(urls, max_threads, max_urls, time_delay)
        crawler.start()

        print("\nTotal Requests Made: {0} Requests".format(crawler.request_count))
        print("Total Bytes Downloaded: {0} Bytes".format(crawler.length))
        print("Average Size Of A Page: {0} Bytes".format(round(crawler.length/crawler.request_count,2)))

    else:
        print('No Urls Extracted From the URL')

if __name__ == '__main__':
    main()


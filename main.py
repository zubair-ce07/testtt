import argparse

from concurrent_spider import ConcurrentSpider


parser = argparse.ArgumentParser()
parser.add_argument('website', help="the website url you want to crawl", type=str)
parser.add_argument('max_urls', help='maximum urls to visit')
parser.add_argument('concurrent_requests', help='total number of concurrent requests')
parser.add_argument('download_delay', help='download delay')
args = parser.parse_args()


def main():
    start_url = args.website
    max_urls = int(args.max_urls)
    concurrent_requests = int(args.concurrent_requests)
    dl_delay = float(args.download_delay)
    concurrent_crawler = ConcurrentSpider(start_url, max_urls, dl_delay, concurrent_requests)
    concurrent_crawler.crawl()
    concurrent_crawler.print_results()


if __name__ == '__main__':
    main()

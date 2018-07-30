import argparse

from concurrent_crawler import ConcurrentCrawler
from concurrent_crawler import UrlProcessor


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("starting_url", type=str,
                        help="Url to start crawling with")
    parser.add_argument("-r", "--concurrent_requests", type=int, default=5)
    parser.add_argument("-d", "--download_delay", type=int, default=2)
    parser.add_argument(
        "-n", "--maximum_requests", type=int, default=50)
    return parser.parse_args()


def print_results(total_bytes, total_requests):
    print(f'Total bytes: {total_bytes}\nTotal requests: {total_requests}\nAverage page size:'
          f'{round(total_bytes/total_requests, 2)} bytes')


def main():

    args = parse_arguments()

    max_reqs = args.maximum_requests
    conc_reqs = args.concurrent_requests
    download_delay = args.download_delay
    start_url = args.starting_url

    extracted_urls = UrlProcessor.extract_urls(start_url)
    filtered_urls = UrlProcessor.filter_urls(start_url, extracted_urls)

    conc_crawler = ConcurrentCrawler(
        start_url, download_delay, conc_reqs, max_reqs)
    conc_crawler.start_crawler(filtered_urls)

    print_results(conc_crawler.total_bytes, conc_crawler.total_requests)


if __name__ == "__main__":
    main()

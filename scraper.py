import argparse
from parserfactory import ParserFactory
import time

class Scraper:
    @staticmethod
    def main():
        arg_parser = argparse.ArgumentParser(description='Crawl Web')
        arg_parser.add_argument("type", help="Parser Type")
        arg_parser.add_argument('-d', metavar='N', nargs='+', type=int,
                                help='Download Delay')
        arg_parser.add_argument('-m', metavar='N', nargs='+', type=int,
                                help='Max request count')
        arg_parser.add_argument('-c', metavar='N', nargs='+', type=int,
                                help='Max Concurrent Request')
        arg_list = arg_parser.parse_args()
        download_delay = 0
        max_request = 1000
        concurrent_request_count = 1000
        if arg_list.d is not None:
            download_delay = int(arg_list.d[0])
        if arg_list.m is not None:
            max_request = int(arg_list.m[0])
        if arg_list.c is not None:
            concurrent_request_count = int(arg_list.c[0])

        crawler = ParserFactory.get_parser(arg_list.type, download_delay, max_request, concurrent_request_count)

        start = time.time()
        crawler.crawl("https://www.trulia.com/for_rent/New_York,NY")
        end = time.time()

        print("Total Time Taken = " + str(end - start))
        print("Total Bytes Downloaded = " + str(crawler.total_bytes_downloaded))
        print("Total Request = " + str(crawler.request_count))
        print("Average Size of a Page = " + str(crawler.total_bytes_downloaded / crawler.request_count))


if __name__ == "__main__":
    Scraper.main()

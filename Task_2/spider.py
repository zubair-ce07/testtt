from time import time
from threading import Thread
from urllib.parse import urlparse
import argparse

from crawl_worker import CrawlWorker


def setup_arguments():
    parser = argparse.ArgumentParser(description='URL data monitor.')

    parser.add_argument('-download_delay', type=int, default=100, \
        help='Time delay in ms for each worker to hit URL.')

    parser.add_argument('-page_count', type=int, default=15, \
        help='Total number of URLs to hit.')

    parser.add_argument('-c_requests', type=int, default=5, \
        help='Total number of cuncurrent requests')

    return parser.parse_args()

def create_worker():
    worker = CrawlWorker()
    worker.load_url()

def main():
    args = setup_arguments()
    CrawlWorker.cuncurrent_request_allowed = args.c_requests
    CrawlWorker.download_delay = args.download_delay
    CrawlWorker.total_pages_to_load = args.page_count

    start_time = time()
    CrawlWorker()
    url = urlparse('https://arbisoft.com/')
    CrawlWorker.url_queue.put(url, False)
    while True:
        if CrawlWorker.cuncurrent_request_made < CrawlWorker.cuncurrent_request_allowed \
            and CrawlWorker.loading_request_made < CrawlWorker.total_pages_to_load:
            worker_thread = Thread(target=create_worker)
            worker_thread.start()

        if CrawlWorker.page_loaded_successfully >= CrawlWorker.total_pages_to_load:
            print("page loaded: " + str(CrawlWorker.page_loaded_successfully))
            print("Total downloaded size: " + str(CrawlWorker.total_bytes_downloaded))
            print("Total time taken: %s" % (time() - start_time))
            break


if __name__ == "__main__":

    main()

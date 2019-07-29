from time import time
from threading import Thread
from urllib.parse import urlparse

from crawl_worker import CrawlWorker


def create_worker():
    worker = CrawlWorker()
    worker.load_url()

def main():
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

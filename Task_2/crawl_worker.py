import queue
from urllib.parse import urlparse
import requests
from time import time
from time import sleep
from parsel import Selector


SUCCESS_RESPONSE_CODE = 200

class CrawlWorker:

    total_bytes_downloaded = 0
    total_pages_to_load = 15
    loading_request_made = 0
    already_visisted_urls = []
    cuncurrent_request_allowed = 5
    cuncurrent_request_made = 0
    page_loaded_successfully = 0
    url_queue = None
    download_delay = 1

    def __init__(self):
        CrawlWorker.cuncurrent_request_made += 1
        self.start_time = time()
        if not CrawlWorker.url_queue:
            CrawlWorker.url_queue = queue.Queue(maxsize=CrawlWorker.total_pages_to_load)

    def __del__(self):
        CrawlWorker.cuncurrent_request_made -= 1

    def load_url(self):
        if CrawlWorker.url_queue.qsize() == 0:
            return
        CrawlWorker.loading_request_made += 1
        url = CrawlWorker.url_queue.get()
        CrawlWorker.url_queue.task_done()
        CrawlWorker.already_visisted_urls.append(url.geturl())
        print("Loading URL: " + url.geturl())
        sleep_time_ms = CrawlWorker.download_delay - ((self.start_time - time())*1000)
        if sleep_time_ms > 0:
            sleep(sleep_time_ms/1000)
        response = requests.get(url.geturl())
        if response.status_code == SUCCESS_RESPONSE_CODE:
            self.start_time = time()
            CrawlWorker.total_bytes_downloaded += len(response.content)
            CrawlWorker.page_loaded_successfully += 1
            if CrawlWorker.page_loaded_successfully >= CrawlWorker.total_pages_to_load:
                return

            selector = Selector(response.text)
            href_links = selector.xpath('//a/@href').getall()
            try:
                for link in href_links:
                    new_url = urlparse(link)
                    if (not new_url.geturl() in CrawlWorker.already_visisted_urls) \
                        and (new_url.netloc == url.netloc) \
                        and new_url:
                        CrawlWorker.url_queue.put(new_url, False)

            except queue.Full:
                pass
            finally:
                if CrawlWorker.total_pages_to_load < CrawlWorker.loading_request_made:
                    self.load_url()
        else:
            if CrawlWorker.total_pages_to_load <= CrawlWorker.loading_request_made:
                CrawlWorker.loading_request_made -= 1
                self.load_url()

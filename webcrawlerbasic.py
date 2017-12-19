import time
from concurrent import futures

from spider import Spider


class WebCrawlerBasic:
    def __init__(self, download_delay, max_request_count, concurrent_request_count):
        self.executor = futures.ThreadPoolExecutor(max_workers=concurrent_request_count)
        self.spider = Spider(download_delay)
        self.max_request_count = max_request_count
        self.request_count = 0

    def crawl(self, url):

        self.spider.last_request_time = time.time()
        self.spider.crawlable_url.put_nowait(url)
        self.schedule_tasks()

    def schedule_tasks(self):
        while not self.spider.crawlable_url.empty() and self.max_request_count > self.request_count:
            url = self.spider.crawlable_url.get()
            self.spider.crawl(url)
            self.request_count += 1




import time
from concurrent import futures
from scheduler import Scheduler

from spider import Spider


class WebCrawlerConcurrent:
    def __init__(self, download_delay, max_request_count, max_concurrent_request):
        self.spider = Spider(download_delay)
        self.spider.last_request_time = time.time()
        executor = futures.ThreadPoolExecutor(max_workers=max_concurrent_request)
        self.scheduler = Scheduler(self.spider, max_request_count, executor)

    async def crawl(self, url):
        self.scheduler.spider.crawlable_url.put_nowait(url)
        await self.scheduler.schedule_tasks()

    def request_count(self):
        return self.scheduler.request_count

    def bytes_downloaded(self):
        return self.spider.total_bytes_downloaded

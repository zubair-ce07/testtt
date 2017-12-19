from scheduler import Scheduler
from spider import Spider
import time


class WebCrawlerAsync:
    def __init__(self, download_delay, max_request_count,max_concurrent_request):
        self.spider = Spider(download_delay)
        self.spider.last_request_time = time.time()
        self.scheduler = Scheduler(self.spider, max_request_count)

    async def crawl(self, url):
        self.spider.crawlable_url.put_nowait(url)
        await self.scheduler.schedule_tasks()

    def request_count(self):
        return self.scheduler.request_count

    def bytes_downloaded(self):
        return self.spider.total_bytes_downloaded

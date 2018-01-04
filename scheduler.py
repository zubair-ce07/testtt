import asyncio
from threading import Lock


class Scheduler:

    def __init__(self, spider, max_request_count, executor=None):
        self.executor = executor
        self.spider = spider
        self.futures = []
        self.max_request_count = max_request_count
        self.request_count = 0
        self.request_count_lock = Lock()
        self.loop = asyncio.get_event_loop()

    async def schedule_tasks(self):

        while not self.spider.crawlable_url.empty():
            url = self.spider.crawlable_url.get_nowait()
            if self.max_request_count > self.request_count:
                future = self.loop.run_in_executor(
                    None,
                    self.spider.crawl,
                    url
                )
                self.futures.append(future)
                self.request_count_lock.acquire()
                try:
                    self.request_count += 1
                finally:
                    self.request_count_lock.release()
        await asyncio.gather(*self.futures)
        if not self.spider.crawlable_url.empty():
            await self.schedule_tasks()

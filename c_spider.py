import asyncio
from parsel import Selector
from queue import Queue
import aiohttp


class CSpider:
    def __init__(self, domain, workers=5, delay=1, max_urls=20):
        self.urls_q = asyncio.Queue()
        self.visited = set()
        self.size = 0
        self.domain = domain.rstrip("/")
        self.max_urls = max_urls
        self.workers = workers
        self.delay = delay
        self.tasks = []

        self.urls_q.put_nowait(self.domain)
        self.init_workers()

    def init_workers(self):
        #self.tasks = [self.crawl("worker-%d" % i) for i in range(self.workers)]
        self.tasks = [self.crawl()]

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self.tasks))
        loop.close()

    async def crawl(self):
        while not self.urls_q.empty() or len(self.visited) < self.max_urls:
            url = await self.urls_q.get()
            #print(worker + " grabbed: " + url)
            if url not in self.visited:
                self.visited.add(url)
                url_size, new_urls = await self.visit(url)

                self.size = self.size + url_size
                for new_url in new_urls:
                    new_url = self.domain + new_url
                    if new_url not in self.visited:
                        self.urls_q.put_nowait(new_url)
            asyncio.sleep(self.delay)

    async def visit(self, url):
        print(url)
        try:
            resp = await aiohttp.request('GET', url)
            body = await resp.read()
            size = len(body)
            urls = self.get_urls(body.decode('utf-16'))
            return (size, urls)
        except Exception as exc:
            print("Warning: (%s) url skipped due to error" % url)
            print(str(exc))
            return (0, [])


    def get_urls(self, body):
        sel = Selector(text=body)
        return sel.xpath('//a//@href').extract()

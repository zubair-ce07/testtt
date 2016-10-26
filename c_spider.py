import asyncio
from parsel import Selector
from queue import Queue
import requests
from time import sleep


class CSpider:

    def __init__(self, domain, workers=5, max_urls=50, delay=1 ):
        self.domain = domain.rstrip("/")
        self.workers = workers
        self.max_urls = max_urls
        self.delay = delay
        self.size = 0
        self.visited = set()
        self.urls = urls = async.Queue()
        self.tasks = []

        self.init_workers()

    def crawl(self):
        loop = asyncio.get_event_loop()

        urls.put(self.domain)
        while len(visited) < self.max_urls:
            url = urls.get()
            if url not in visited:
                size, new_urls = self.visit(url)
                self.size = self.size + size                
                visited.add(url)
                for new_url in new_urls:
                    new_url = self.domain + new_url
                    if new_url not in visited:
                        urls.put(new_url)
            sleep(self.delay)

    def init_workers(self):
        for i in range(self.workers):
            self.task.append(visit('worker-' + str(i)))

    @asyncio.coroutine
    def visit(self, url):
        
        print(url)
        try:
            conn = requests.get(url, timeout=5)
            size = len(conn.text)
            urls = self.get_urls(conn.text)
            yield (size, urls)
        except Exception as exc:
            print("Warning: (%s) url skipped due to error" % url)
            print(str(exc))
            yield (0, [])

    def get_urls(self, body):
        sel = Selector(text=body)
        return sel.xpath('//a//@href').extract()

import asyncio
from parsel import Selector
from queue import Queue
import aiohttp
from concurrent.futures import ProcessPoolExecutor


class PSpider:
    def __init__(self, domain, delay=5, max_urls=20):
        self.visited = set()
        self.size = 0
        self.domain = domain.rstrip("/")
        self.max_urls = max_urls
        self.delay = delay
        self.tasks = []


    def start(self):
        self.urls_q = Queue()
        self.urls_q.put_nowait(self.domain)
        self.crawl()


    def crawl(self):
        futures = []
        with ProcessPoolExecutor() as pool:
            while len(self.visited) < self.max_urls:
                url = self.urls_q.get()
                if url not in self.visited:
                    self.visited.add(url)
                    future = pool.submit(self.visit, url)
                    futures.append(future)

                    # check if any futures returned and
                    # update spider attributes
                    for f in as_completed(futures):
                        url_size, new_urls = f.result()

                        self.size = self.size + url_size
                        for new_url in new_urls:
                            new_url = self.domain + new_url
                            if new_url not in self.visited:
                                self.urls_q.put_nowait(new_url)
                asyncio.sleep(self.delay)

    def visit(self, url):
        print(url)
        try:
            resp = aiohttp.request('GET', url)
            body = resp.read()
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

import asyncio
from parsel import Selector
from queue import Queue
from multiprocessing import Manager
import requests
from concurrent.futures import ProcessPoolExecutor, as_completed


class PSpider:
    def __init__(self, domain, delay=5, max_urls=20):
        self.visited = set()
        self.size = 0
        self.domain = domain.rstrip("/")
        self.max_urls = max_urls
        self.delay = delay
        self.tasks = []
        #self.urls_q = ["https://www.arbisoft.com"]

        #self.urls_q.put(self.domain)
        manager  = Manager()
        self.urls_q = manager.Queue()
        self.urls_q.put_nowait(self.domain)

    def crawl(self):
        futures = []
        with ProcessPoolExecutor() as pool:
            while True:
                pass
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
            resp = requests.get(url)
            body = resp.text
            size = len(body)
            urls = self.get_urls(resp.text)
            return (size, urls)
        except Exception as exc:
            print("Warning: (%s) url skipped due to error" % url)
            print(str(exc))
            return (0, [])

    def get_urls(self, body):
        sel = Selector(text=body)
        return sel.xpath('//a//@href').extract()

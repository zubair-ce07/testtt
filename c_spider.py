import asyncio
from parsel import Selector
from queue import Queue
import requests
from time import sleep


class CSpider:

    def __init__(self, domain, max_urls=50, delay=1 ):
        self.domain = domain.rstrip("/")
        self.max_urls = max_urls
        self.delay = delay
        self.size = 0

    def crawl(self):
        urls = Queue()
        visited = set()

        urls.put(self.domain)
        while not urls.empty() and len(visited) < self.max_urls:
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

    def visit(self, url):
        print(url)
        try:
            conn = requests.get(url, timeout=5)
            size = len(conn.text)
            urls = self.get_urls(conn.text)
            #return (size, urls)
        except Exception as exc:
            print("Warning: (%s) url skipped due to error" % url)
            print(str(exc))
            #return (0, [])

    def get_urls(self, body):
        sel = Selector(text=body)
        return sel.xpath('//a//@href').extract()

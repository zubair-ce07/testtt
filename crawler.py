import json
from urllib import parse

from parser import *


class SprinterSpider:
    def __init__(self, url, concurrent_req, delay, url_visit_limit):
        self.visited_urls = dict()
        self.items_visited_urls = dict()
        self.crawler_pending_urls = set([url])
        self.items_pending_urls = set([])
        self.concurrent_req = concurrent_req
        self.delay = delay
        self.url_visit_limit = url_visit_limit
        self.semaphore = asyncio.BoundedSemaphore(concurrent_req)
        self.host = parse.urlsplit(url).netloc
        self.sprinter_records = list()

    async def filter_bad_urls(self, extracted_urls):
        return list(filter(lambda e: parse.urlsplit(e).netloc == self.host,
                           extracted_urls))

    async def add_crawler_links(self, extracted_urls, url):
        for link in extracted_urls:
            link = parse.urljoin(url, link)
            if not self.visited_urls.get(link):
                self.crawler_pending_urls.add(link)

    async def add_items_links(self, item_urls, url):
        for link in item_urls:
            link = parse.urljoin(url, link)
            if len(link.split('/')) < 5:
                continue
            if not self.items_visited_urls.get(link):
                self.items_pending_urls.add(link)

    async def extract_urls(self, url, loop):
        async with self.semaphore:
            future = loop.run_in_executor(None, requests.post, url)
            response = await future
            time.sleep(self.delay)

        if response.status_code == 200\
                and len(response.text):
            self.visited_urls[url] = True
            selector = parsel.Selector(text=response.text)
            extracted_urls = selector.css("a::attr(href)").extract()
            item_link_key = '//div[@class="item"]/a/@href'
            item_urls = selector.xpath(item_link_key).getall()
            extracted_urls = await self.filter_bad_urls(extracted_urls)
            await self.add_crawler_links(extracted_urls, url)
            await self.add_items_links(item_urls, url)

    async def schedule_futures(self, loop):
        futures = []
        while self.crawler_pending_urls and self.url_visit_limit > 1:
            url = self.crawler_pending_urls.pop()
            self.url_visit_limit -= 1
            futures.append(
                asyncio.ensure_future(self.extract_urls(url, loop)))
        await asyncio.wait(futures)
        return futures

    def crawl(self):
        while self.url_visit_limit > 1 and self.crawler_pending_urls:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.schedule_futures(loop))
            traverse_items(self.items_visited_urls, self.items_pending_urls,
                           self.sprinter_records)

        with open('schema.json', 'w') as outfile:
            outfile.write(json.dumps(self.sprinter_records, indent=4,
                          ensure_ascii=False))
            outfile.write(",\n")
        print("File Saved!")





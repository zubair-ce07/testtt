import json
from urllib.parse import urlsplit, urljoin

from parser import *


class SprinterSpider:
    def __init__(self, url, concurrent_req, delay, max_urls_limit):
        self.visited_urls = set()
        self.items_visited_urls = set()
        self.cat_urls = {url}
        self.items_urls = set()
        self.concurrent_req = concurrent_req
        self.delay = delay
        self.max_urls_limit = max_urls_limit
        self.semaphore = asyncio.BoundedSemaphore(concurrent_req)
        self.host = "www.sprinter.es"
        self.sprinter_records = list()

    def filter_bad_urls(self, extracted_urls):
        return list(filter(lambda e: urlsplit(e).netloc == self.host,
                           extracted_urls))

    async def extract_urls(self, url, loop):
        async with self.semaphore:
            future = loop.run_in_executor(None, requests.post, url)
            response = await future
            time.sleep(self.delay)

        if response.status_code == 200\
                and len(response.text):
            self.visited_urls.add(url)
            text_s = parsel.Selector(text=response.text)
            extracted_urls = text_s.css('a[rel="follow"]::attr(href)').extract()
            item_link_css = 'article[class="listing-item"] a::attr(href)'
            item_urls = text_s.css(item_link_css).extract()
            extracted_urls = self.filter_bad_urls(extracted_urls)
            self.cat_urls |= set(urljoin(url, link) for link in extracted_urls
                                 if not self.items_visited_urls)
            self.items_urls |= set(urljoin(url, link) for link in item_urls
                                   if link not in self.items_visited_urls)

    async def schedule_futures(self, loop):
        futures = []
        while self.cat_urls and self.max_urls_limit > 1:
            url = self.cat_urls.pop()
            print(url)
            self.max_urls_limit -= 1
            futures.append(
                asyncio.ensure_future(self.extract_urls(url, loop)))
        await asyncio.wait(futures)
        return futures

    def crawl(self):
        while self.max_urls_limit > 1 and self.cat_urls:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.schedule_futures(loop))
            traverse_items(self.items_visited_urls, self.items_urls,
                           self.sprinter_records)

        with open('schema.json', 'w') as outfile:
            outfile.write(json.dumps(self.sprinter_records, indent=4,
                          ensure_ascii=False))
            outfile.write(",\n")
        print("File Saved!")





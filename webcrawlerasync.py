import time
import asyncio
from lxml import html
import requests
from elements.webpage import WebPage
from elements.element import Element
from data.datanode import DataNode


class WebCrawlerAsync:
    def __init__(self, download_delay, max_request_count, concurrent_request_count):
        self.download_delay = download_delay
        self.max_request_count = max_request_count
        self.request_pool_count = concurrent_request_count
        self.pending_crawls = []
        self.loop = None
        self.threads = 1
        self.request_count = 0
        self.last_request_time = None
        self.total_bytes_downloaded = 0
        self.visited_url = []

    def crawl(self, web_page: WebPage):
        crawl = {'pending': True}
        self.pending_crawls.append(crawl)
        self.loop = asyncio.get_event_loop()
        url = web_page.url_string("")
        self.last_request_time = time.time()
        self.visited_url.append(url)
        source = requests.get(url)
        self.request_count += 1
        doc = html.fromstring(source.content)
        self.total_bytes_downloaded += len(source.content)
        result = self._crawl_element([doc], web_page)
        asyncio.ensure_future(self._stop_loop(), loop=self.loop)
        crawl.update({"pending": False})
        self.loop.run_forever()
        return result

    def _crawl_element(self, source_elements, element: Element):
        items = []
        for source in source_elements:
            item = DataNode(element.multiple)
            item.name = element.item_name()
            item.add_data_items(self._parse_data(source, element))

            if len(element.crawlable_links) > 0:
                asyncio.ensure_future(self._crawl_sub_pages(item, source, element),
                                      loop=self.loop)
            for sub_element in element.data_elements:
                sub_source = source.xpath(sub_element.xpath())
                if len(sub_source) > 0:
                    sub_items = self._crawl_element(sub_source, sub_element)
                    item.add_sub_items(sub_items)
            items.append(item)
        return items

    def _parse_data(self, source_element, element: Element):
        data = {}
        for leaf in element.leaf_elements:
            text = source_element.xpath(leaf.xpath())
            if len(text) == 0:
                data.update({leaf.name: None})
            elif len(text) == 1:
                data.update({leaf.name: text[0]})
            else:
                data.update({leaf.name: text})
        return data

    async def _crawl_sub_pages(self, item, source_element, element):
        crawl = {'pending': True}
        try:
            self.pending_crawls.append(crawl)
            sub_items = []
            self.threads += 1
            if self.max_request_count > self.request_count:
                for crawlable in element.crawlable_links:
                    matches = source_element.xpath(crawlable.xpath())
                    for match in matches:
                        url = crawlable.url_string(match.attrib.get('href'))
                        visited_url = [explored_url for explored_url in self.visited_url if explored_url == url]
                        if len(visited_url) == 0:
                            self.visited_url.append(url)
                            future1 = self.loop.run_in_executor(None, requests.get, url)
                            self.request_count += 1
                            current_time = time.time()

                            if current_time - self.last_request_time < self.download_delay:
                                asyncio.sleep(current_time - self.last_request_time)
                                current_time = time.time()

                            self.last_request_time = current_time
                            while self.request_pool_count == 0:
                                asyncio.sleep(1)

                            self.request_pool_count -= 1
                            response = await future1
                            self.request_pool_count += 1

                            self.total_bytes_downloaded += len(response.content)
                            doc = html.fromstring(response.content)
                            crawled_list = self._crawl_element(doc, crawlable)
                            sub_items += crawled_list
            item.add_sub_items(sub_items)
        finally:
            crawl.update({'pending': False})

    async def _stop_loop(self):
        while True:
            pending = [pending for pending in self.pending_crawls if pending.get("pending") is True]
            if len(pending) == 0:
                self.loop.stop()
                return
            else:
                await asyncio.sleep(10)

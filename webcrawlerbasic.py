from lxml import html
import requests
import time
from elements.webpage import WebPage
from elements.element import Element
from data.datanode import DataNode


class WebCrawlerBasic:
    def __init__(self, download_delay, max_request_count):
        self.download_delay = download_delay
        self.max_request_count = max_request_count
        self.pending_crawls = []
        self.loop = None
        self.threads = 1
        self.request_count = 0
        self.total_bytes_downloaded = 0
        self.last_request_time = None
        self.visited_url = []

    def crawl(self, web_page: WebPage):
        url = web_page.url_string("")
        self.visited_url.append(url)
        self.last_request_time = time.time()
        source = requests.get(url)
        doc = html.fromstring(source.content)
        self.request_count += 1
        self.total_bytes_downloaded += len(source.content)
        result = self.crawl_element([doc], web_page)

        return result

    def crawl_element(self, source_elements, element: Element):
        items = []
        for source in source_elements:
            item = DataNode(element.multiple)
            item.name = element.item_name()
            item.add_data_items(self.parse_data(source, element))
            item.add_sub_items(self.crawl_sub_pages(source, element))
            for sub_element in element.data_elements:
                sub_source = source.xpath(sub_element.xpath())
                if len(sub_source) > 0:
                    sub_items = self.crawl_element(sub_source, sub_element)
                    item.add_sub_items(sub_items)
            items.append(item)
        return items

    @staticmethod
    def parse_data(source_element, element: Element):
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

    def crawl_sub_pages(self, source_element, element):
        sub_items = []
        for crawlable in element.crawlable_links:
            if self.max_request_count > self.request_count:
                matches = source_element.xpath(crawlable.xpath())
                for match in matches:
                    url = crawlable.url_string(match.attrib.get('href'))
                    visited_url = [explored_url for explored_url in self.visited_url if explored_url == url]
                    if len(visited_url) == 0:
                        self.visited_url.append(url)
                        current_time = time.time()
                        if current_time - self.last_request_time < self.download_delay:
                            time.sleep(current_time - self.last_request_time)

                        new_source = requests.get(url)
                        doc = html.fromstring(new_source.content)
                        self.request_count += 1
                        self.total_bytes_downloaded += len(new_source.content)
                        sub_items += self.crawl_element(doc, crawlable)
        return sub_items

import requests
from linkfinder import LinkFinder
from lxml import html


class Spider:
    start_url = ''
    queue = set()
    crawled = set()
    products = []

    def __init__(self, start_url):
        Spider.start_url = start_url
        self.crawl_page(Spider.start_url)

    @staticmethod
    def crawl_page(page_url):
        print("First Spider gathering links")
        Spider.add_links_to_queue(Spider.gather_links(page_url))

    @staticmethod
    def gather_links(url):
        source = Spider.source_code(url)
        finder = LinkFinder()
        finder.findlinks(source)
        return finder.links

    @staticmethod
    def gather_links_category(url):
        source = Spider.source_code(url)
        finder = LinkFinder()
        finder.find_links_category(source)
        return finder.links

    @staticmethod
    def source_code(url):
        source_code = requests.get(url)
        source_element = html.fromstring(source_code.content)
        return source_element

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            Spider.queue.add(url)

    @staticmethod
    def crawl_category(thread_name, url):
        if url not in Spider.crawled:
            print(thread_name + ' now crawling ' + url)
            Spider.add_links_to_queue(Spider.gather_links_category(url))
            Spider.queue.remove(url)
            Spider.crawled.add(url)

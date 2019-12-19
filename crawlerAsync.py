from urllib.request import urlopen
from file_functions import *
from link_finder import LinkFinder
from domain import *
import time
import asyncio
import aiohttp
import threading


class CrawlerAsync:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''

    max_page_crawl = 0
    download_delay = 0
    total_request_made = 1
    total_bytes_downloaded = 1
    average_page_size = 1

    queue = set()
    crawled = set()

    def __init__(self, project_name,
                 base_url, domain_name,
                 max_page_crawl, download_delay):

        self.project_name = project_name
        self.base_url = base_url
        self.domain_name = domain_name
        self.queue_file = self.project_name + '/queue.txt'
        self.crawled_file = self.project_name + '/crawled.txt'
        self.max_page_crawl = max_page_crawl
        self.download_delay = download_delay
        self.boot()

    def boot(self):
        create_project_dir(self.project_name)
        create_data_files(self.project_name, self.base_url)
        self.queue = file_to_set(self.queue_file)
        self.crawled = file_to_set(self.crawled_file)

    async def f(self, url):
        async with aiohttp.ClientSession() as session:
            task = asyncio.ensure_future(self.gather_links(session, url))
            return await asyncio.gather(task, return_exceptions=True)

    def crawl_page(self, thread_name, page_url):
        if page_url not in self.crawled:
            print(f"{threading.current_thread().name} now crawling {page_url}")
            loop = asyncio.get_event_loop()
            links = loop.run_until_complete(self.f(page_url))
            self.add_links_to_queue(*links)
            self.queue.remove(page_url)
            self.crawled.add(page_url)
            self.update_files()
        if len(self.queue) and self.max_page_crawl > self.total_request_made:
            u = list(self.queue)[-1]
            self.crawl_page(thread_name, u)

    async def gather_links(self, session, page_url):
        async with session.get(page_url) as response:
            html = await response.text()
            finder = LinkFinder(self.base_url, page_url)
            finder.feed(html)
            self.total_bytes_downloaded += len(html)
            self.total_request_made += 1
            return finder.page_links()

    def add_links_to_queue(self, links):
        for url in links:
            if (url in self.queue) or (url in self.crawled):
                continue
            if self.domain_name != get_domain_name(url):
                continue
            self.queue.add(url)

    def update_files(self):
        set_to_file(self.queue, self.queue_file)
        set_to_file(self.crawled, self.crawled_file)

    def __del__(self):
        print(f"Total request made by crawler : {self.total_request_made}")
        print(
            f"Total bytes Downloaded by crawler : {self.total_bytes_downloaded}")
        print(
            f"Average size of page : {self.total_bytes_downloaded/self.total_request_made:.1f}")

from urllib.request import urlopen
from file_functions import *
from link_finder import LinkFinder
from domain import *
import time


class Crawler:

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
        self.crawl_page('Main', self.base_url)

    def boot(self):
        create_project_dir(self.project_name)
        create_data_files(self.project_name, self.base_url)
        self.queue = file_to_set(self.queue_file)
        self.crawled = file_to_set(self.crawled_file)

    def crawl_page(self, thread_name, page_url):
        if page_url not in self.crawled:
            print(f"{thread_name} now crawling {page_url}")
            self.add_links_to_queue(self.gather_links(page_url))
            self.queue.remove(page_url)
            self.crawled.add(page_url)
            self.update_files()

    def gather_links(self, page_url):
        html_string = ''
        time.sleep(self.download_delay)
        response = urlopen(page_url)
        self.total_request_made += 1
        if 'text/html' in response.getheader('Content-Type'):
            html_bytes = response.read()
            self.total_bytes_downloaded += len(html_bytes)
            html_string = html_bytes.decode("utf-8")
        finder = LinkFinder(self.base_url, page_url)
        finder.feed(html_string)
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
        print(f"Total bytes Downloaded by crawler : {self.total_bytes_downloaded}")
        print(f"Average size of page : {self.total_bytes_downloaded/self.total_request_made:.1f}")


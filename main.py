from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading
from crawler import Crawler
import time
from domain import *
from file_functions import *

start_time = time.time()
PROJECT_NAME = 'Task 2'
HOMEPAGE = 'http://quotes.toscrape.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
MAX_PAGE_CRAWL = 200
DOWNLOAD_DELAY = 0

queue = Queue()

crawler = Crawler(
    PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, MAX_PAGE_CRAWL, DOWNLOAD_DELAY)


def work():
    while True:
        url = queue.get(block=True, timeout=5)
        crawler.crawl_page(threading.current_thread().name, url)
        queue.task_done()


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    crawled_links = file_to_set(CRAWLED_FILE)
    if len(queued_links) > 0:
        if len(crawled_links) > MAX_PAGE_CRAWL:
            print("Max number of pages crawled")
        else:
            create_jobs()
    else:
        print("Crawled all pages")


with ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
    executor.submit(work)
    executor.submit(work)
    executor.submit(work)
    executor.submit(work)
    executor.submit(work)
    executor.submit(work)
    executor.submit(work)
    executor.submit(work)
    crawl()


print(f"Time Taken to Execute : {time.time() - start_time:.2f} seconds")

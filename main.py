from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading
from crawlerParallel import CrawlerParallel
from crawlerAsync import CrawlerAsync
import time
from domain import *
from file_functions import *
from My_ArgParser import *

start_time = time.time()

arguments = My_ArgParser()

PROJECT_NAME = 'Task 2'
HOMEPAGE = arguments.args.base_URL
NUMBER_OF_THREADS = arguments.args.r
MAX_PAGE_CRAWL = arguments.args.m
DOWNLOAD_DELAY = arguments.args.d
crawler_type = arguments.args.crawler_type

DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'


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
        print(f"Crawled all pages :{MAX_PAGE_CRAWL}")


if crawler_type is 1:

    queue = Queue()
    crawler = CrawlerParallel(
        PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, MAX_PAGE_CRAWL, DOWNLOAD_DELAY)

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

if crawler_type == 2:

    crawler = CrawlerAsync(
        PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, MAX_PAGE_CRAWL, DOWNLOAD_DELAY)
    crawler.crawl_page("M", list(crawler.queue)[-1])

print(f"Time Taken to Execute : {time.time() - start_time:.2f} seconds")

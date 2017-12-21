import threading
from queue import Queue
from spider import Spider
import argparse

homepage = "https://www.ginatricot.com/eu/en/start"
queue = Queue()
spider = Spider(homepage)


def create_workers(no_of_threads):
    for _ in range(no_of_threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        Spider.crawl_category(threading.current_thread().name, url)
        queue.task_done()


def create_jobs():
    for link in spider.queue:
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    queued_links = spider.queue
    if queued_links:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()
    else:
        print(len(spider.products))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("no_of_threads", help="Enter number of workers you want to create")
    parameters = parser.parse_args()
    no_of_threads = int(parameters.no_of_threads)
    create_workers(no_of_threads)
    crawl()

if __name__ == '__main__':
    main()

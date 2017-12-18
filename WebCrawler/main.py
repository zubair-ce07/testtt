import threading
from queue import Queue
from spider import Spider

homepage = "https://www.ginatricot.com/eu/en/start"
no_of_threads = 20
queue = Queue()
spider = Spider(homepage)


def create_workers():
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
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()
    else:
        print(len(spider.products))


def main():
    create_workers()
    crawl()

if __name__ == '__main__':
    main()

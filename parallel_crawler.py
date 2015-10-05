from multiprocessing import Process, Manager
from time import sleep
from multiprocessing.queues import JoinableQueue
import requests
import logging
import links_parser

logging.basicConfig(level=logging.DEBUG,
                    format='(%(processName)-10s) %(message)s',  #: Output the Process Name just for checking purposes
                    )


class ParallelCrawler(object):

    def __init__(self, base_url1,  allowed_domain, no_of_parallel_requests=0, download_delay=0):

        self.download_delay = download_delay
        self.base_url = base_url1
        self.no_of_parallel_requests = no_of_parallel_requests
        self.allowed_domain = allowed_domain

        self.queue = JoinableQueue()        # Making a queue to share urls b/w all processes
        self.queue.put(self.base_url)      # Initializing queue by base url

        self.seen_urls = Manager().list()  # list of URLs that have already been seen
        self.seen_urls.append(self.base_url)

        self.total_requests = Manager().Value('i', 0)  # Shared variable b/w processes
        self.total_bytes = Manager().Value('i', 0)     # Shared variable b/w processes

    def make_processes(self):

        for i in range(self.no_of_parallel_requests):
            p = Process(name=str(i) + " Process Number", target=self.crawl)
            p.daemon = True
            p.start()
        self.queue.join()

        return self.total_bytes.value, self.total_requests.value

    #: Crawl requests in parallel
    def crawl(self):

        while True:
            url = self.queue.get()
            html = requests.get(url).text

            size = html.__sizeof__()

            #: Increment the requests number and total bytes downloaded
            self.total_requests.value += 1
            self.total_bytes.value += size

            #: Finding all the links in a page
            parser = links_parser.LinksParser(self.base_url, self.allowed_domain)
            parser.feed(html)
            links = parser.get_urls()

            #: Removing duplicates within a certain process
            links = set(links)

            #: set subtraction
            #: Removing duplicates within all process
            links = links - set(self.seen_urls)
            links = list(links)

            for link in links:
                if link != 'http://':
                    self.seen_urls.append(link)
                    self.queue.put(link)

            #: Sleep for the time given in the download delay
            sleep(self.download_delay)
            self.queue.task_done()





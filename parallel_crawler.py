__author__ = "root"
from multiprocessing import Process, Manager
import re
from time import sleep
import stat_summary
from multiprocessing.queues import JoinableQueue
import requests
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(processName)-10s) %(message)s',  #: Output the Process Name just for checking purposes
                    )


class ParallelCrawler(object):

    def __init__(self, base_url1, no_of_parallel_requests=0, download_delay=0):

        self.download_delay = download_delay
        self.base_url = base_url1
        self.no_of_parallel_requests = no_of_parallel_requests
        self.summary = stat_summary.StatSummary()   #: Making Statistics summary object to save statistics saved
        self.queue = JoinableQueue()        # Making a queue to share urls b/w all processes
        self.queue.put(self.base_url)      # Initializing queue by base url
        self.seen_urls = Manager().list()  # list of URLs that have already been seen

    def make_processes(self):

        for i in range(self.no_of_parallel_requests):
            p = Process(name=str(i) + " Process Number", target=self.crawl)
            p.daemon = True
            p.start()
        self.queue.join()

        #: Now calculate average size of the page
        self.summary.calculate_average_size()

    #: Parallel Crawling will be done in Processes
    def crawl(self):

        while True:

            url = self.queue.get()

            #: add url in the list of seen urls
            self.seen_urls.append(url)

            html = requests.get(url).text

            #: Set total bytes downloaded (in Bytes)
            size = html.__sizeof__()

            self.summary.add_bytes(size)

            #: Increment the requests number
            self.summary.increment_request()

            #: use re.findall to get all the links
            links = re.findall('"((http)s?://.*?)"', html)
            links = map(lambda x: x[0], links)

            #: Removing duplicates within a certain process
            links = set(links)

            #: set subtraction
            #: Removing duplicates within all process
            links = links - set(self.seen_urls)
            links = list(links)

            for link in links:
                if link != 'http://':
                    self.queue.put(link)

            #: Sleep for the time given in the download delay
            sleep(self.download_delay)
            self.queue.task_done()





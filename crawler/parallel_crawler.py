from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from parsel import Selector
import time
import requests
import sys


class ParallelCrawler:
    def __init__(self, urls, no_of_request, delay=0, max_threads=5):
        self.urls = urls
        self.max_threads = max_threads
        self.no_of_request = no_of_request
        self.results = []
        self.delay = delay
        self.avg_page_size = 0
        self.download_size = 0

    def __makerequest(self, url):
        try:
            html_text = requests.get(url=url).text
            return html_text
        except requests.Timeout as ex:
            print("request time out")
            raise ex
        except requests.ConnectionError as ex:
            print("Connection error occured")
            raise ex
        except requests.RequestException as ex:
            raise ex

    def __parseresults(self, html_text):
        try:
            selector = Selector(text=html_text)
            urls = selector.xpath('//a/@href').extract()
            return urls
        except Exception as ex:
            print("EXception occured")
            raise ex

    def wrapper(self, url):
        time.sleep(self.delay)
        html_text = self.__makerequest(url)
        urls = self.__parseresults(html_text)
        return sys.getsizeof(html_text), urls

    def run(self):
        with ThreadPoolExecutor(max_workers=min(self.no_of_request, self.max_threads)) as Executor:
            jobs = [Executor.submit(self.wrapper, url) for url, t_id in zip(self.urls, range(self.no_of_request))]
            counter = 0
            for job in concurrent.futures.as_completed(jobs):
                result = job.result()
                self.avg_page_size += result[0]
                self.results.append(result[1])
                counter += 1
            if counter > 0:
                self.avg_page_size = int(self.avg_page_size/counter)
            self.download_size = sys.getsizeof(self.results)

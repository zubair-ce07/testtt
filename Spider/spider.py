import sys
import argparse
import parsel
import requests
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, wait, as_completed


class Spider:
    def __init__(self, t_urls, request_delay, t_requests, s_type):
        self.t_urls = t_urls
        self.request_delay = request_delay
        self.t_requests = t_requests
        self.s_type = s_type
        self.web_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.reports = Reports()
        html_doc = self.http_requester(self.web_url).text
        next_urls = self.url_parser(html_doc)
        if s_type is "r":
            self.recursive_spider(self.t_urls, next_urls, i=1)
            self.get_report(tasks=None)
        loop = asyncio.get_event_loop()
        if s_type is "c":
            tasks = []
            for i in range(self.t_urls):
                tasks.append(asyncio.ensure_future(self.concurent_spider(
                    next_urls[i])))
            loop.run_until_complete(asyncio.wait(tasks))
            self.get_report(tasks)
        if s_type is "p":
            loop.run_until_complete(self.parallel_spider(
                next_urls))
        loop.close()

    def get_report(self, tasks):
        if self.s_type is not "r":
            for data in tasks:
                self.reports.results["total_downloaded"] = (
                    self.reports.results["total_downloaded"]
                    + len(data.result().content))
        self.reports.results["average"] = (
                self.reports.results["total_downloaded"]
                / self.t_urls)   
        self.reports.results["requests"] = self.t_requests
        self.reports.get_spider_report()
    
    def http_requester(self, web_url):
        r = requests.get(web_url)
        return r
    
    def url_parser(self, html_doc):
        sel = parsel.Selector(html_doc)
        all_urls = sel.css("a::attr(href)").getall()
        next_url = [url for url in all_urls
                    if "http" in url or "https" in url]
        return next_url

    def recursive_spider(self, urls_to_visit, next_url, i):
        if urls_to_visit == 0:
            return
        else:
            time.sleep(self.request_delay)
            r = self.http_requester(next_url[i])
            self.reports.results["total_downloaded"] = (
                    self.reports.results["total_downloaded"]
                    + len(r.content))
            self.recursive_spider(urls_to_visit - 1, next_url, i+1)
                
    @asyncio.coroutine
    async def parallel_spider(self, next_urls):
        pool = ThreadPoolExecutor(self.t_requests)
        futures = []
        for i in range(self.t_urls):
            await asyncio.sleep(self.request_delay)
            futures.append(pool.submit(self.http_requester, next_urls[i]))
        self.get_report(as_completed(futures))
    
    @asyncio.coroutine
    async def concurent_spider(self, url):
        await asyncio.sleep(self.request_delay)
        return self.http_requester(url)

    
class Reports:
    def __init__(self):
        self.results = {"total_downloaded": 0}

    def get_spider_report(self):
        print("Total Requests: {}".format(self.results["requests"]))
        print("Average Page Size: {} Bytes".format(self.results["average"]))
        print("Total Download Size: {} Bytes".format(
            self.results["total_downloaded"]))


def input_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', help="No of URLS")
    parser.add_argument('delay', help="Delay between each request")
    parser.add_argument('requests', help="No of concurrent requests")
    parser.add_argument('type', choices=['r', 'c', 'p'], default='r',
                        help="Select type of spider \nr-----Recursive" +
                        "c-----Concurrent p-----Parallel " +
                        "Default is recursive")
    args = parser.parse_args()
    spider = Spider(int(args.urls), int(args.delay),
                    int(args.requests), args.type)
    
    
if __name__ == "__main__":
    input_parser()
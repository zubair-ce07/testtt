import re
import time
import requests
from bs4 import BeautifulSoup
from ParallelCrawler import ParallelCrawler
from ConcurrentListCrawler import ConcurrentCrawler


class Crawler:

    def __init__(self):
        self.base_url = []
        self.no_of_threads = 0
        self.download_delay = 0
        self.links = []
        self.no_of_requests = 0
        self.max_urls_to_visit = 0
        self.total_bytes_downloaded = 0;

    def get_user_input(self):
        self.base_url = input("Enter base url: ")
        self.no_of_threads = int(input("Enter the concurrent no of requests you want to proceed: "))
        self.download_delay = int(input("Enter the download delay (in seconds): "))
        self.max_urls_to_visit = int(input("Enter the max urls to visit: "))
        self.links.append(self.base_url)

    def recursive_app_concurrent(self):
        self.no_of_requests += 1
        if self.max_urls_to_visit < self.no_of_requests * self.no_of_threads:
            print("Total Bytes downloaded are: " + str(self.total_bytes_downloaded))
            print("Average Size of page is: " + str(self.total_bytes_downloaded/self.max_urls_to_visit))
            return
        print("Crawling Request #: " + str(self.no_of_requests))
        print("Crawling following links: " + str(self.links[0:self.no_of_threads]))
        con_crawler = ConcurrentCrawler(self.links[0:self.no_of_threads], self.no_of_threads)
        con_crawler.run_script()
        #print(con_crawler.results)
        self.total_bytes_downloaded = self.total_bytes_downloaded + con_crawler.bytes_downloaded
        print("Results after crawling are: " + str(con_crawler.links) + "\n")
        time.sleep(self.download_delay)
        for i in con_crawler.links:
            self.links.append(i)
        self.links = self.links[self.no_of_threads+1:]
        self.recursive_app_concurrent()

    def recursive_app_parallel(self):
        self.no_of_requests += 1
        if self.max_urls_to_visit < self.no_of_requests * self.no_of_threads:
            print("Total Bytes downloaded are: " + str(self.total_bytes_downloaded))
            print("Average Size of page is: " + str(self.total_bytes_downloaded / self.max_urls_to_visit))
            return
        print("Crawling Request #: " + str(self.no_of_requests))
        print("Crawling following links: " + str(self.links[0:self.no_of_threads]))
        par_crawler = ParallelCrawler(self.links[0:self.no_of_threads], self.no_of_threads)
        par_crawler.eventloop()
        #print(par_crawler.results)
        self.total_bytes_downloaded = self.total_bytes_downloaded + par_crawler.bytes_downloaded
        print("Results after crawling are: " + str(par_crawler.links) + "\n")
        time.sleep(self.download_delay)
        for i in par_crawler.links:
            self.links.append(i)
        self.links = self.links[self.no_of_threads + 1:]
        self.recursive_app_parallel()


if __name__ == '__main__':
    crawl_concurrent = Crawler()
    crawl_parallel = Crawler()
    choice = int(input("Which recursive crawler you want to use\n1. Concurrent\n2. Parallel\n"))
    crawl_concurrent.get_user_input()
    count = 0
    source_code = requests.get(crawl_concurrent.base_url).text
    soup = BeautifulSoup(source_code, "html.parser")
    parse_web_links = soup.findAll('a', attrs={'href': re.compile("^https://")})[0:53]
    for link in parse_web_links:
        crawl_concurrent.links.append(link.get('href'))
    crawl_concurrent.links = crawl_concurrent.links[3:53]
    crawl_parallel = crawl_concurrent
    if(choice == 1):
        crawl_concurrent.recursive_app_concurrent()
    else:
        crawl_parallel.recursive_app_parallel()

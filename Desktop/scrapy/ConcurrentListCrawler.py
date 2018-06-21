import re
import requests
import concurrent.futures
from bs4 import BeautifulSoup


class ConcurrentCrawler:

    def __init__(self, url_list, threads):
        self.urls = url_list
        self.results = {}
        self.max_threads = threads
        self.links = []
        self.bytes_downloaded = 0

    def run_script(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers = self.max_threads) as Executor:
            jobs = [Executor.submit(self.wrapper, u) for u in self.urls]

    def wrapper(self, url):
        url, html = self.__make_request(url)
        self.__parse_results(url, html)

    def __make_request(self, url):
        r = requests.get(url=url, timeout=20)
        r.raise_for_status()
        self.bytes_downloaded = self.bytes_downloaded + len(r.content)
        return r.url, r.text


    def __parse_results(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        parse_web_links = soup.findAll('a', attrs={'href': re.compile("^https://")})[0:50]
        for link in parse_web_links:
            self.links.append(link.get('href'))

        if self.links:
            self.results[url] = self.links

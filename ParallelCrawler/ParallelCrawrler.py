import concurrent.futures
import urllib.request
import re

from bs4 import BeautifulSoup
from time import sleep


class ParallelCrawler():

    def __init__(self, url, threads, url_limit, delay):

        self.urls = url
        self.max_threads = threads
        self.length = 0
        self.request_count = 0
        self.url_limit = url_limit
        self.download_delay = delay

    def start(self):
        # Retrieve a single page and report the URL and contents

        def load_url(url , timeout):

            with urllib.request.urlopen(url, timeout=timeout) as conn:
                return conn.read()

        # We can use a with statement to ensure threads are cleaned up promptly
        # Start the load operations and mark each future with its URL
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for index in range(self.request_count, self.url_limit):
                future_to_url = {executor.submit(load_url, self.urls[index], 60): self.urls[index]}

                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()

                    except Exception as exc:
                        self.request_count = self.request_count + 1
                        print('%r generated an exception: %s' % (url, exc))
                    else:
                        print('%r page is %d bytes %d' % (url, len(data),self.request_count))
                        self.length = self.length + len(data)
                        self.request_count = self.request_count + 1
                        soup = BeautifulSoup(data, 'lxml')
                        for link in soup.findAll('a'):

                            url = link.get('href')
                            if re.match('http', str(url)):
                                self.urls.append(url)
                            else:
                                continue
                sleep(self.download_delay)

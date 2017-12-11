from concurrent.futures import ThreadPoolExecutor
import requests
from parsel import Selector
import time


class ParallelCrawler(object):
    def __init__(self, url, threads, url_limit, delay):
        self.url = url
        self.titles = {}
        self.url_list = []
        self.max_threads = threads
        self.length = 0
        self.request_count = 0
        self.url_limit = url_limit
        self.download_delay = delay

    def __make_request(self, url):
        """Function to get the HTML content of the given URL"""
        try:
            r = requests.get(url=url, timeout=20)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            r = requests.get(url=url, timeout=60)
        except requests.exceptions.ConnectionError:
            r = requests.get(url=url, timeout=60)
        except requests.exceptions.RequestException as e:
            raise e
        self.request_count += 1
        return r.url, len(r.content), r.text

    def __parse_results(self, url, html):
        """Parse the HTML Body to take out all included urls"""
        try:
            sel = Selector(text=html)
            title = sel.css('title::text').extract_first()
            divs = sel.xpath('//div')
            divs = divs.xpath('.//p')
            page_url_list = divs.css('a::attr(href)').extract()

        except Exception as e:
            raise e

        if title:
            self.titles[url] = title

        if page_url_list:
            for element in page_url_list:
                url_temp = 'https://en.wikipedia.org' + element
                self.url_list.append(url_temp)

    def wrapper(self, url):
        """Wrapper Functions to call request and parse function"""
        if self.request_count < self.url_limit:
            url_name, file_size, html = self.__make_request(url)
            self.length += file_size
            self.__parse_results(url_name, html)
            time.sleep(self.download_delay)

    def run_script(self):
        with ThreadPoolExecutor(max_workers=min(len(self.url), self.max_threads)) as Executor:
            jobs = [Executor.submit(self.wrapper, u) for u in self.url]


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_urls():
    url = ['https://en.wikipedia.org/wiki/Web_crawler']
    example = ParallelCrawler(url, 1, 1, 1)
    example.run_script()
    urls = example.url_list
    return urls


def main():

    urls = get_urls()
    max_threads = 10
    max_urls = 10
    time_delay = 5

    crawler = ParallelCrawler(urls, max_threads, max_urls, time_delay)
    crawler.run_script()

    average = crawler.length / max_urls

    print('Total Requests made: {}'.format(crawler.request_count))
    print('Total Bytes Downloaded: {}'.format(sizeof_fmt(crawler.length)))
    print('Average File Size: {}'.format(sizeof_fmt(average)))


if __name__ == '__main__':

    main()

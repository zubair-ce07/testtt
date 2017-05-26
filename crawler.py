import aiohttp
import asyncio
import requests
from concurrent import futures
from parsel import Selector


class Crawler:

    def __init__(self, base_url, concurrent_requests, delay, visiting_urls):
        self.base_url = base_url
        self.concurrent_requests = concurrent_requests
        self.delay = delay
        self.visiting_urls = visiting_urls   # number of urls to be visited
        self.downloaded_bytes = 0
        self.urls_reading = []
        self.visited_url = []

    def downloaded_bytes_counter(self, response):
        self.downloaded_bytes += len(response)

    def url_reader(self, html):
        selector = Selector(text=html)
        url_in_page = selector.xpath('//a/@href').extract()
        for url in url_in_page:
            if len(self.urls_reading) == self.visiting_urls:
                break
            if url.startswith('/'):
                url = url[1:]
            if url.find('http') == -1:
                url = self.base_url + url
                if url not in self.visited_url:
                    self.urls_reading.append(url)

    def show_performance(self, method):
        print('Crawling through {}'.format(method))
        print('Visited pages: {}'.format(len(self.visited_url)))
        print('Downloaded Bytes: {}'.format(self.downloaded_bytes))
        print('Average size of a page {}\n\n'.format(self.downloaded_bytes / len(self.visited_url)))


class AsyncCrawler(Crawler):

    async def crawling(self, url):
        self.visited_url.append(url)
        async with aiohttp.request('Get', url) as response:
            html = await response.text()
            self.downloaded_bytes_counter(html)
            self.url_reader(html)

    async def ensure_concurrency(self):
        # It ensures number of concurrent request by creating specified number of tasks named
        # async_requesting_urls and pass it to the asyncio.wait()
        await self.crawling(self.base_url)
        while len(self.visited_url) < len(self.urls_reading):
            async_crawling_urls = []
            for url_index in range(len(self.visited_url),
                                   len(self.visited_url) + self.concurrent_requests):
                if url_index < len(self.urls_reading):
                    url = self.urls_reading[url_index]
                    crawling_url = asyncio.ensure_future(self.crawling(url))
                    async_crawling_urls.append(crawling_url)
                    await asyncio.sleep(self.delay)
            await asyncio.wait(async_crawling_urls)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ensure_concurrency())
        loop.close()


class ParallelCrawler(Crawler):

    def crawling(self, url):
        self.visited_url.append(url)
        html = requests.get(url).text
        self.downloaded_bytes_counter(html)
        self.url_reader(html)

    def ensure_parallelism(self):
        # It ensures number of parallel request by collecting specified number of urls and pass these
        # urls to ThreadPoolExecutor for crawling
        while len(self.visited_url) < len(self.urls_reading):
            parallel_crawling_urls = []
            for url_index in range(len(self.visited_url),
                                   len(self.visited_url) + self.concurrent_requests):
                if url_index < len(self.urls_reading):
                    url = self.urls_reading[url_index]
                    parallel_crawling_urls.append(url)
            with futures.ThreadPoolExecutor(max_workers=self.concurrent_requests) as executor:
                executor.map(self.crawling, parallel_crawling_urls)

    def start(self):
        self.crawling(self.base_url)
        self.ensure_parallelism()

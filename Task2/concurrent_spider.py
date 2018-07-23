import concurrent.futures
import asyncio

from urllib.parse import urlparse, urljoin, quote
from parsel import Selector
import requests

from scraping_report import CrawlingSummaryReport


class RecursiveConcurrentSpider:
    def __init__(self, site_to_crawl, download_delay, concurrent_requests_limit):
        self.site_to_crawl = site_to_crawl
        self.spider_execution_report = CrawlingSummaryReport()
        self.download_delay = download_delay
        self.concurrent_requests_limit = concurrent_requests_limit
        self.visited_urls = []
        self.__loop = asyncio.get_event_loop()
        self.__executor = concurrent.futures.ThreadPoolExecutor()
        self.__tasks_limiting_semaphore = asyncio.BoundedSemaphore(self.concurrent_requests_limit)

    async def start_crawler(self, urls, limit):
        if len(self.visited_urls) < limit and urls:
            if len(urls) > limit - len(self.visited_urls):
                urls = urls[:limit - len(self.visited_urls)]

            completed_futures, pending_futures = await self.visit_urls(urls)
            self.visited_urls.extend(urls)

            while True:
                for completed in completed_futures:
                    self.spider_execution_report.bytes_downloaded += len(completed.result())
                    self.spider_execution_report.total_requests += 1
                    await self.start_crawler(self.get_urls(completed.result()), limit)

                if pending_futures:
                    completed_futures, pending_futures = await asyncio.wait(pending_futures,
                                                                            return_when=asyncio.FIRST_COMPLETED)
                else:
                    break

    async def visit_urls(self, urls):
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(self.make_get_request(url, self.__tasks_limiting_semaphore)))
            await asyncio.sleep(self.download_delay)

        completed, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        return completed, pending

    async def make_get_request(self, url, tasks_limiting_semaphore):
        async with tasks_limiting_semaphore:
            task = asyncio.ensure_future(self.__loop.run_in_executor(self.__executor, requests.get, url.geturl()))
            response = await asyncio.wait_for(task, None)

        return response.text

    def get_urls(self, html_text):
        absolute_urls = self.get_absolute_urls(html_text)
        filtered_urls = self.get_filtered_urls(absolute_urls)
        return list(filtered_urls)

    def get_filtered_urls(self, absolute_urls):
        visited_urls_strings = [url.geturl() for url in self.visited_urls]
        return [url for url in absolute_urls if url.geturl() not in visited_urls_strings]
    
    def get_absolute_urls(self, html_text):
        return {self.get_parsed_url(url) for url in self.get_links_from_html(html_text)
                if urlparse(url).scheme == '' and urlparse(url).path not in ('', '/')}

    def get_parsed_url(self, url):
        url_string = urljoin(self.site_to_crawl, urlparse(url).path)
        normalized_url = quote(url_string, "\./_-:")
        return urlparse(normalized_url)

    def get_links_from_html(self, html_text):
        html_selector = Selector(html_text)
        return html_selector.css('a::attr(href)').extract()

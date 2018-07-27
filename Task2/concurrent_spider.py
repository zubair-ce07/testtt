import concurrent.futures
import asyncio

from urllib.parse import urljoin
from parsel import Selector
import requests

from scraping_report import CrawlingSummaryReport


class RecursiveConcurrentSpider:
    def __init__(self, site_to_crawl, download_delay, concurrent_requests_limit):
        self.site_url = site_to_crawl
        self.spider_execution_report = CrawlingSummaryReport()
        self.download_delay = download_delay
        self.concurrent_requests_limit = concurrent_requests_limit
        self.visited_urls = []
        self.__loop = asyncio.get_event_loop()
        self.__executor = concurrent.futures.ThreadPoolExecutor()
        self.__tasks_limiting_semaphore = asyncio.BoundedSemaphore(self.concurrent_requests_limit)

    def run(self, total_urls):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.schedule_requests([self.site_url.strip("/")], total_urls))

    async def schedule_requests(self, urls, limit):
        if len(self.visited_urls) < limit and urls:
            urls = urls[:limit-len(self.visited_urls)] if len(urls) > limit-len(self.visited_urls) else urls

            scheduled_tasks = await self.visit_urls(urls)
            self.visited_urls.extend(urls)

            for task in scheduled_tasks:
                response = await task
                await self.schedule_requests(self.extract_links(response), limit)

    async def visit_urls(self, urls):
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(self.make_request(url)))
            await asyncio.sleep(self.download_delay)

        return asyncio.as_completed(tasks)

    async def make_request(self, url):
        async with self.__tasks_limiting_semaphore:
            task = asyncio.ensure_future(self.__loop.run_in_executor(self.__executor, requests.get, url))
            response = await asyncio.wait_for(task, None)
            self.spider_execution_report.bytes_downloaded += len(response.text)
            self.spider_execution_report.total_requests += 1

        return response

    def extract_links(self, response):
        links = self.get_links(response)
        absolute_urls = {self.get_absolute_url(link.strip()) for link in links}
        filtered_urls = self.filter_urls(absolute_urls)
        return filtered_urls

    def get_links(self, response):
        return Selector(response.text).css('a::attr(href)').extract()

    def get_absolute_url(self, link):
        if "://" in link:
            return link.strip("/")
        return urljoin(self.site_url, link).strip("/")

    def filter_urls(self, urls):
        return [url for url in urls if url not in self.visited_urls and self.site_url in url]

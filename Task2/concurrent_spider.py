import requests
from parsel import Selector
from urllib.parse import urlparse
from urllib.parse import urljoin
import asyncio
import concurrent.futures
import scraping_report
import logging
import datetime


class RecursiveConcurrentSpider:
    def __init__(self, site):
        self.site = site
        self.report = scraping_report.CrawlingSummaryReport()
        self.__loop = asyncio.get_event_loop()
        self.__executor = concurrent.futures.ThreadPoolExecutor()

    async def make_get_request(self, url, tasks_limiting_semaphore):
        async with tasks_limiting_semaphore:
            task = asyncio.ensure_future(self.__loop.run_in_executor(self.__executor, requests.get, url.geturl()))
            get_response = await asyncio.wait_for(task, None)

        return get_response.text, len(get_response.text)

    @staticmethod
    def get_next_urls(site, html_text):
        html_selector = Selector(html_text)

        all_urls = [urlparse(url) for url in html_selector.css('a::attr(href)').extract()]
        filtered_urls = {urlparse(urljoin(site, url.path)) for url in all_urls
                         if url.scheme == '' and url.path not in ('', '/')}

        return list(filtered_urls)

    async def visit_urls(self, urls, download_delay, concurrent_requests_limit):
        tasks_limiting_semaphore = asyncio.BoundedSemaphore(concurrent_requests_limit)

        tasks = []
        for url in urls:
            tasks.append(self.make_get_request(url, tasks_limiting_semaphore))
            logging.info(f"{datetime.datetime.now().time()} - Visited page: {url.geturl()}")
            await asyncio.sleep(download_delay)

        results = await asyncio.gather(*tasks)

        return results

    async def start_crawler(self, urls, urls_limit, download_delay, concurrent_requests_limit):
        if urls_limit > 0:
            urls, urls_limit = (urls[:urls_limit], 0) if len(urls) > urls_limit else (urls, urls_limit - len(urls))

            get_request_results = await self.visit_urls(urls, download_delay, concurrent_requests_limit)
            self.report.total_requests += len(urls)

            for html_text, html_page_size in get_request_results:
                self.report.bytes_downloaded += html_page_size
                return await self.start_crawler(RecursiveConcurrentSpider.get_next_urls(self.site, html_text),
                                                urls_limit, download_delay, concurrent_requests_limit)

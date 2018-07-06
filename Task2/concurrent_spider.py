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

    @staticmethod
    async def make_get_request(url, tasks_limiting_semaphore):
        async with tasks_limiting_semaphore:
            loop = asyncio.get_event_loop()
            get_method_executor = concurrent.futures.ThreadPoolExecutor()
            task = asyncio.ensure_future(loop.run_in_executor(get_method_executor, requests.get, url.geturl()))
            get_response = await asyncio.wait_for(task, None)

        return get_response.text, len(get_response.text)

    @staticmethod
    def get_next_urls(site, html_text):
        html_selector = Selector(html_text)

        all_urls = [urlparse(url) for url in html_selector.css('a::attr(href)').extract()]
        filtered_urls = {urlparse(urljoin(site, url.path)) for url in all_urls
                         if url.scheme == '' and url.path not in ('', '/')}

        return list(filtered_urls)

    @staticmethod
    async def get_html(urls, download_delay, concurrent_requests_limit):
        tasks_limiting_semaphore = asyncio.BoundedSemaphore(concurrent_requests_limit)

        tasks = []
        for url in urls:
            tasks.append(RecursiveConcurrentSpider.make_get_request(url, tasks_limiting_semaphore))
            logging.info("{} - Visited page: {}".format(datetime.datetime.now().time(), url.geturl()))
            await asyncio.sleep(download_delay)

        results = await asyncio.gather(*tasks)

        return results

    async def start_crawler(self, urls, urls_limit, download_delay, concurrent_requests_limit):
        if urls_limit > 0:
            if len(urls) > urls_limit:
                urls = urls[:urls_limit]
                urls_limit = 0
            else:
                urls_limit = urls_limit - len(urls)

            get_request_results = await RecursiveConcurrentSpider.get_html(urls, download_delay,
                                                                           concurrent_requests_limit)
            self.report.total_requests += len(urls)

            for html_text, html_page_size in get_request_results:
                self.report.bytes_downloaded += html_page_size

                return await self.start_crawler(RecursiveConcurrentSpider.get_next_urls(self.site, html_text),
                                                urls_limit, download_delay, concurrent_requests_limit)
        else:
            return self

    def run_crawler(self, url_limit, download_delay, concurrent_requests_limit):
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(self.start_crawler([urlparse(self.site)], url_limit,
                                                       download_delay, concurrent_requests_limit))
        finally:
            loop.close()

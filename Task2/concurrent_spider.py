from urllib.parse import urlparse
from urllib.parse import urljoin
from parsel import Selector
import concurrent.futures
import asyncio
import requests
import scraping_report


class RecursiveConcurrentSpider:
    def __init__(self, site_to_crawl, download_delay, concurrent_requests_limit):
        self.site_to_crawl = site_to_crawl
        self.spider_execution_report = scraping_report.CrawlingSummaryReport()
        self.download_delay = download_delay
        self.concurrent_requests_limit = concurrent_requests_limit
        self.__loop = asyncio.get_event_loop()
        self.__executor = concurrent.futures.ThreadPoolExecutor()

    async def start_crawler(self, urls, urls_limit):
        if urls_limit > 0 and urls:
            urls, urls_limit = (urls[:urls_limit], 0) if len(urls) > urls_limit else (urls, urls_limit - len(urls))

            get_request_results, total_urls_visited = await self.visit_urls(urls)
            self.spider_execution_report.total_requests += total_urls_visited

            for html_text, html_page_size in get_request_results:
                self.spider_execution_report.bytes_downloaded += html_page_size
                return await self.start_crawler(self.get_next_urls(html_text), urls_limit)

    async def visit_urls(self, urls):
        tasks_limiting_semaphore = asyncio.BoundedSemaphore(self.concurrent_requests_limit)

        total_urls_visited = 0
        tasks = []
        for url in urls:
            tasks.append(self.make_get_request(url, tasks_limiting_semaphore))
            total_urls_visited += 1
            await asyncio.sleep(self.download_delay)

        results = await asyncio.gather(*tasks)

        return results, total_urls_visited

    async def make_get_request(self, url, tasks_limiting_semaphore):
        async with tasks_limiting_semaphore:
            task = asyncio.ensure_future(self.__loop.run_in_executor(self.__executor, requests.get, url.geturl()))
            get_response = await asyncio.wait_for(task, None)

        return get_response.text, len(get_response.text)

    def get_next_urls(self, html_text):
        html_selector = Selector(html_text)

        filtered_urls = {urlparse(urljoin(self.site_to_crawl, urlparse(url).path))
                         for url in html_selector.css('a::attr(href)').extract()
                         if urlparse(url).scheme == '' and urlparse(url).path not in ('', '/')}

        return list(filtered_urls)

import asyncio
import requests
from parsel import Selector
from urllib import parse
from requests.compat import urljoin


class UrlProcessor:
    @staticmethod
    def extract_urls(start_url):
        selector = Selector(requests.get(start_url).text)
        extracted_urls = selector.css("a::attr(href)").extract()
        return extracted_urls

    @staticmethod
    def filter_urls(start_url, extracted_urls):
        domain = parse.urlparse(start_url).netloc
        filtered_urls = [urljoin(start_url, url)
                         for url in extracted_urls if parse.urlparse(url).netloc == domain]
        return filtered_urls


class ConcurrentCrawler:
    def __init__(self, start_url, download_delay, conc_requests, max_reqs):
        self.start_url = start_url
        self.download_delay = download_delay
        self.loop = asyncio.get_event_loop()
        self.semaphore = asyncio.BoundedSemaphore(conc_requests)
        self.max_reqs = max_reqs
        self.total_bytes = 0
        self.total_requests = 0
        self.visited_urls = []
        self.remaining_requests = max_reqs

    async def crawl_url(self, url):
        async with self.semaphore:
            responce = await asyncio.ensure_future(self.loop.run_in_executor(None, requests.get, url))
            await asyncio.sleep(self.download_delay)
        return responce.text

    async def create_tasks(self, filtered_urls):
        tasks = []
        for url in filtered_urls:
            tasks.append(self.crawl_url(url))
            self.visited_urls.append(url)

        results = await asyncio.gather(*tasks)
        return results

    async def process_crawler_results(self, filtered_urls):
        results = await self.create_tasks(filtered_urls[:self.remaining_requests])
        for result in results:
            self.total_bytes += len(result)
            self.total_requests += 1
            self.remaining_requests = self.max_reqs - self.total_requests

        if self.remaining_requests:
            starting_url = self.visited_urls.pop()
            extracted_urls = UrlProcessor.extract_urls(starting_url)
            filtered_urls = UrlProcessor.filter_urls(
                starting_url, extracted_urls)
            await self.process_crawler_results(filtered_urls)

    def start_crawler(self, filtered_urls):
        self.loop.run_until_complete(
            self.process_crawler_results(filtered_urls))

        self.loop.close()

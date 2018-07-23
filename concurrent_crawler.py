import asyncio
import requests


class CrawlerResults:
    def __init__(self, total_bytes=0, total_requests=0):
        self.total_bytes = total_bytes
        self.total_requests = total_requests


class ConcurrentCrawler:
    def __init__(self, download_delay, conc_requests):
        self.download_delay = download_delay
        self.loop_ = asyncio.get_event_loop()
        self.semaphore = asyncio.BoundedSemaphore(conc_requests)
        self.crawler_results = CrawlerResults()

    async def crawl_url(self, url, semaphore):
        async with semaphore:
            responce = await asyncio.ensure_future(self.loop_.run_in_executor(None, requests.get, url))
        return responce.text

    async def create_tasks(self, filtered_urls, delay):
        tasks = []
        for url in filtered_urls:
            tasks.append(self.crawl_url(url, self.semaphore))
            await asyncio.sleep(delay)
        results = await asyncio.gather(*tasks)
        return results

    async def process_crawler_results(self, filtered_urls):
        results = await self.create_tasks(filtered_urls, self.download_delay)
        for result in results:
            self.crawler_results.total_bytes += len(result)
            self.crawler_results.total_requests += 1

    def start_crawler(self, filtered_urls):
        self.loop_.run_until_complete(
            self.process_crawler_results(filtered_urls))

        self.loop_.close()

import asyncio
import requests


class ConcurrentCrawler:
    def __init__(self, download_delay, conc_requests):
        self.download_delay = download_delay
        self.loop = asyncio.get_event_loop()
        self.semaphore = asyncio.BoundedSemaphore(conc_requests)
        self.total_bytes = 0
        self.total_requests = 0

    async def crawl_url(self, url):
        async with self.semaphore:
            responce = await asyncio.ensure_future(self.loop.run_in_executor(None, requests.get, url))
            await asyncio.sleep(self.download_delay)
        return responce.text

    async def create_tasks(self, filtered_urls):
        tasks = []
        for url in filtered_urls:
            tasks.append(self.crawl_url(url))

        results = await asyncio.gather(*tasks)
        return results

    async def process_crawler_results(self, filtered_urls):
        results = await self.create_tasks(filtered_urls)
        for result in results:
            self.total_bytes += len(result)
            self.total_requests += 1

    def start_crawler(self, filtered_urls):
        self.loop.run_until_complete(
            self.process_crawler_results(filtered_urls))

        self.loop.close()

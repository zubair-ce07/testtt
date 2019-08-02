import asyncio
from urllib.parse import urlparse
from time import time

import aiohttp
from parsel import Selector


SUCCESS_RESPONSE_CODE = 200

class CrawlWorker:

    total_bytes_downloaded = 0
    download_delay = 0.1
    total_pages_to_load = 15
    cuncurrent_request_allowed = 5
    page_loaded_successfully = 0
    url_queue = None
    total_urls_requested = 0
    already_visisted_urls = []
    visiting_domain = None

    @staticmethod
    async def setup_worker(total_pages_to_load, cuncurrent_request_allowed, \
            download_delay, first_url, loop):
        CrawlWorker.download_delay = download_delay
        CrawlWorker.total_pages_to_load = total_pages_to_load
        CrawlWorker.cuncurrent_request_allowed = cuncurrent_request_allowed
        CrawlWorker.url_queue = asyncio.Queue()
        url = urlparse(first_url)
        await CrawlWorker.url_queue.put(url)

        start_time = time()
        await CrawlWorker.__run_worker(loop)
        CrawlWorker.__print_result(start_time)

    @staticmethod
    async def __run_worker(loop):
        crawl_workers = set()
        cuncurrent_task_lock = asyncio.Semaphore(
            value=CrawlWorker.cuncurrent_request_allowed
        )
        while CrawlWorker.page_loaded_successfully < CrawlWorker.total_pages_to_load:
            await cuncurrent_task_lock.acquire()
            await asyncio.sleep(CrawlWorker.download_delay)
            crawl_workers.add(loop.create_task(CrawlWorker.__create_worker(cuncurrent_task_lock)))

        await asyncio.wait(crawl_workers)

    @staticmethod
    def __print_result(start_time):

        total_bytes_downloaded = CrawlWorker.total_bytes_downloaded
        total_pages_loaded = CrawlWorker.page_loaded_successfully
        avg_page_size = total_bytes_downloaded / total_pages_loaded

        print(f"\nTotal pages loaded: {total_pages_loaded}")
        print(f"Total bytes downloaded: {total_bytes_downloaded}")
        print(f"Average page size: {avg_page_size}")
        print("Total time taken: %s" % (time() - start_time))

    @staticmethod
    async def __create_worker(cuncurrent_task_lock):
        worker = CrawlWorker()
        await worker.request()
        try:
            await cuncurrent_task_lock.release()
        except TypeError:
            pass

    def __is_valid_url(self, url):
        return (not url.geturl() in CrawlWorker.already_visisted_urls) \
            and (url.netloc == CrawlWorker.visiting_domain) \
            and url

    async def handle_response(self, response):
        CrawlWorker.page_loaded_successfully += 1
        CrawlWorker.total_bytes_downloaded += len(response)
        selector = Selector(response)
        href_links = selector.xpath('//a/@href').getall()
        for link in href_links:
            new_url = urlparse(link)
            if self.__is_valid_url(new_url):
                await CrawlWorker.url_queue.put(new_url)

    def is_request_allowed(self):
        return (CrawlWorker.url_queue.qsize() != 0) and \
            (CrawlWorker.total_urls_requested < CrawlWorker.total_pages_to_load)

    async def request(self):
        if not self.is_request_allowed():
            return
        CrawlWorker.total_urls_requested += 1
        raw_url = await CrawlWorker.url_queue.get()
        CrawlWorker.url_queue.task_done()
        if not CrawlWorker.visiting_domain:
            CrawlWorker.visiting_domain = raw_url.netloc
        url = raw_url.geturl()
        print(f"Loading URL: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == SUCCESS_RESPONSE_CODE:
                    response = await resp.text()
                    await self.handle_response(response)
                else:
                    CrawlWorker.total_urls_requested -= 1

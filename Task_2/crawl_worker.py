import asyncio
from urllib.parse import urlparse

import aiohttp
from parsel import Selector


SUCCESS_RESPONSE_CODE = 200

class CrawlWorker:

    total_bytes_downloaded = 0
    cuncurrent_request_allowed = 5
    total_pages_to_load = 15
    page_loaded_successfully = 0
    url_queue = asyncio.Queue()
    loading_request_made = 0
    already_visisted_urls = []
    download_delay = 0.1
    visiting_domain = None

    def __is_valid_url(self, url):
        return (not url.geturl() in CrawlWorker.already_visisted_urls) \
            and (url.netloc == CrawlWorker.visiting_domain) \
            and url

    async def handle_response(self, response):
        await asyncio.sleep(CrawlWorker.download_delay)
        CrawlWorker.page_loaded_successfully += 1
        CrawlWorker.total_bytes_downloaded += len(response)
        selector = Selector(response)
        href_links = selector.xpath('//a/@href').getall()
        for link in href_links:
            new_url = urlparse(link)
            if self.__is_valid_url(new_url):
                await CrawlWorker.url_queue.put(new_url)

    async def request(self):
        if (CrawlWorker.url_queue.qsize() == 0) or \
            (CrawlWorker.loading_request_made >= CrawlWorker.total_pages_to_load):
            return
        CrawlWorker.loading_request_made += 1
        raw_url = await CrawlWorker.url_queue.get()
        CrawlWorker.url_queue.task_done()
        if CrawlWorker.visiting_domain is None:
            CrawlWorker.visiting_domain = raw_url.netloc
        url = raw_url.geturl()
        print(f"Loading URL: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == SUCCESS_RESPONSE_CODE:
                    response = await resp.text()
                    await self.handle_response(response)
                    if CrawlWorker.loading_request_made < CrawlWorker.total_pages_to_load:
                        await self.request()
                else:
                    if CrawlWorker.total_pages_to_load >= CrawlWorker.loading_request_made:
                        CrawlWorker.loading_request_made -= 1
                        await self.request()

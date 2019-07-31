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

    async def request(self):
        if (CrawlWorker.url_queue.qsize() == 0) or \
            (CrawlWorker.loading_request_made >= CrawlWorker.total_pages_to_load):
            return
        CrawlWorker.loading_request_made += 1
        raw_url = await CrawlWorker.url_queue.get()
        url = raw_url.geturl()
        CrawlWorker.url_queue.task_done()
        print(f"Loading URL: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == SUCCESS_RESPONSE_CODE:
                    response = await resp.text()
                    await asyncio.sleep(CrawlWorker.download_delay)
                    CrawlWorker.page_loaded_successfully += 1
                    CrawlWorker.total_bytes_downloaded += len(response)
                    selector = Selector(response)
                    href_links = selector.xpath('//a/@href').getall()
                    try:
                        for link in href_links:
                            new_url = urlparse(link)
                            if (not new_url.geturl() in CrawlWorker.already_visisted_urls) \
                                and (new_url.netloc == raw_url.netloc) \
                                and new_url:

                                await CrawlWorker.url_queue.put(new_url)

                    except asyncio.QueueFull:
                        pass
                    finally:
                        if CrawlWorker.loading_request_made < CrawlWorker.total_pages_to_load:
                            await self.request()
                else:
                    if CrawlWorker.total_pages_to_load >= CrawlWorker.loading_request_made:
                        CrawlWorker.loading_request_made -= 1
                        await self.request()

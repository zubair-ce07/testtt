import asyncio
from statistics import mean

import aiohttp

from utils import find_urls_from_content, get_logger


class ConcurrentCrawler:
    def __init__(self, params):
        self.__crawled_urls = set([])
        self.__page_sizes = []

        self.__urls_to_visit = {params['url']}
        self.__workers_limit = params['workers']
        self.__number_of_urls_to_crawl = params['count']
        self.__download_delay = params['delay']

        self.__concurrent_requests_count = None
        self.__total_requests_made = 0

        self.__logger = get_logger('ConcurrentCrawler')

    def crawl(self):
        asyncio.run(self.__crawl_website())
        average_page_size = 0
        if len(self.__page_sizes) > 0:
            average_page_size = mean(self.__page_sizes)

        return type("CrawlStats", (object,), dict(requests_made=self.__total_requests_made,
                                                  bytes_downloaded=sum(self.__page_sizes),
                                                  average_page_size=average_page_size))

    async def __crawl_website(self):
        self.__concurrent_requests_count = asyncio.Semaphore(value=self.__workers_limit,
                                                             loop=asyncio.get_running_loop())

        while True:
            tasks = []

            for current_url in self.__urls_to_visit.copy():
                if self.__total_requests_made >= self.__number_of_urls_to_crawl:
                    if len(tasks) > 0:
                        await asyncio.gather(*tasks)
                    return

                self.__total_requests_made += 1
                if current_url not in self.__crawled_urls:
                    tasks.append(asyncio.create_task(self.send_request(current_url)))

                    self.__crawled_urls.add(current_url)
                    self.__urls_to_visit.remove(current_url)

            if len(tasks) == 0 and len(self.__urls_to_visit) == 0:
                self.__logger.warn('No more urls to crawl.')
                return

            if len(tasks) > 0:
                await asyncio.gather(*tasks)

    async def send_request(self, current_url):
        await self.__concurrent_requests_count.acquire()

        self.__logger.info(f'Sending request to {current_url}')

        if self.__download_delay > 0:
            await asyncio.sleep(self.__download_delay)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(current_url) as response:
                    html = await response.text()
                    self.__concurrent_requests_count.release()

                    if response.status != 200:
                        return

                    self.__page_sizes.append(len(html))

                    urls = find_urls_from_content(html, current_url)

                    self.__urls_to_visit = self.__urls_to_visit | urls
        except Exception:
            self.__logger.error(f'Error occurred when sending request to {current_url}')

            self.__concurrent_requests_count.release()

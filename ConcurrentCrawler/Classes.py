import asyncio
import aiohttp
import re
from parsel import Selector

class ConcurrentCrawler(object):

    def __init__(self, url_list, max_threads, url_limit, delay):

        self.urls = url_list
        self.max_threads = max_threads
        self.page_url_list = []
        self.download_delay = delay
        self.length = 0
        self.request_count = 0
        self.url_limit = url_limit

    async def get_url_body(self, url):

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:

                assert response.status == 200
                html = await response.text()
                length = len(html)
                self.length += length
                self.request_count += 1

        return html

    async def creating_threads(self, thread_id, work_queue):

        while not work_queue.empty():
            current_url = await work_queue.get()

            try:
                print(current_url)
                task_status = await self.get_results(current_url, thread_id)
                await asyncio.sleep(self.download_delay)

            except Exception as e:
                await asyncio.sleep(self.download_delay)

    async def get_results(self, url, thread_id):


        if self.request_count <= self.url_limit:
  #          print(self.request_count , self.url_limit)
            print('Thread {} Requesting'.format(thread_id))
            html = await self.get_url_body(url)
            print('Thread {} Parsing URLs'.format(thread_id))
            self.__get_urls_html(html)
            print('Thread {} Completed'.format(thread_id))
            return 'Completed'

    def __get_urls_html(self, html):

        try:
            sel = Selector(text=html)
            divs = sel.xpath('//div')
            divs = divs.xpath('.//p')
            page_url_list = divs.css('a::attr(href)').extract()
            for urls in  page_url_list:
                if re.match('http', str(urls)):
                    self.urls.append(urls)

        except Exception as e:

            raise e

    def event_loop(self):

        while self.url_limit > self.request_count:

            q = asyncio.Queue()
            [q.put_nowait(url) for url in self.urls[self.request_count:self.url_limit]]
            loop = asyncio.get_event_loop()
            tasks = [self.creating_threads(thread_id, q, ) for thread_id in range(self.max_threads)]
            loop.run_until_complete(asyncio.wait(tasks))

        loop.close()
from parsel import Selector
import aiohttp
import asyncio
import sys
import time


class Asnyccrawler:

    def __init__(self, urls, no_of_request, delay=0, max_threads=5):

        self.urls = urls
        self.results = []
        self.no_of_request = no_of_request
        self.delay = delay
        self.max_threads = max_threads
        self.page_count = 0
        self.avg_page_size = 0
        self.download_size = 0

    def calculate_size(self):
        if self.page_count > 0:
            self.avg_page_size = int(self.avg_page_size/self.page_count)
        self.download_size = sys.getsizeof(self.results)

    def __parseresults(self, url, html_text):
        try:
            selector = Selector(text=html_text)
            urls = selector.xpath('//a/@href').extract()
            return urls
        except Exception as ex:
            print("EXception occured")
            raise ex

    async def get_html(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                assert response.status == 200
                html = await response.read()
                return html

    async def get_results(self, url):
        html = await self.get_html(url)
        urls = self.__parseresults(url, str(html))
        return sys.getsizeof(html), urls

    async def tasks_handler(self, task_id, work_queue):
        while not work_queue.empty():
            url = await work_queue.get()
            try:
                task_status = await self.get_results(url)
                self.results.append(task_status[1])
                self.avg_page_size += task_status[0]
                self.page_count += 1
            except Exception as ex:
                print("Error Ocured for {} :".format(url), ex)
            time.sleep(self.delay)

    def eventloop(self):
        q = asyncio.Queue()
        [q.put_nowait(url) for url, task_id in zip(self.urls, range(self.no_of_request))]
        loop = asyncio.get_event_loop()
        tasks = [self.tasks_handler(task_id, q, ) for task_id in range(self.max_threads)]
        print(tasks)
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        self.calculate_size()

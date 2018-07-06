import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup


class ParallelCrawler:

    def __init__(self, url_list, max_threads):
        self.urls = url_list
        self.results = {}
        self.max_threads = max_threads
        self.links = []
        self.bytes_downloaded = 0

    def __parse_results(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        parse_web_links = soup.findAll('a', attrs={'href': re.compile("^https://")})[0:50]
        for link in parse_web_links:
            self.links.append(link.get('href'))

    async def __make_request(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                assert response.status == 200
                html = await response.read()
                self.bytes_downloaded = self.bytes_downloaded + response.content.total_bytes
                return response.url, html

    async def wrapper(self, url):
        url, html = await self.__make_request(url)
        self.__parse_results(url, html)
        return 'Completed'

    async def handle_tasks(self, task_id, work_queue):
        while not work_queue.empty():
            current_url = await work_queue.get()
            task_status = await self.wrapper(current_url)

    def eventloop(self):
        q = asyncio.Queue()
        [q.put_nowait(url) for url in self.urls]
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        tasks = [self.handle_tasks(task_id, q, ) for task_id in range(self.max_threads)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

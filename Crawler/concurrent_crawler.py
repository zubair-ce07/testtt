import asyncio
import aiohttp
import logging
from parsel import Selector
import parallel_crawler as crawl


class ConcurrentCrawler(object):

    def __init__(self, url_list, max_threads, url_limit, delay):
        self.urls = url_list
        self.titles = {}
        self.max_threads = max_threads
        self.page_url_list = []
        self.download_delay = delay
        self.length = 0
        self.request_count = 0
        self.url_limit = url_limit

    async def get_body(self, url):
        """ Function to get the HTML content of the given URL"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=60) as response:
                assert response.status == 200
                html = await response.text()
                length = len(html)
                self.length += length
                self.request_count +=1
                return response.url, html

    def __parse_results(self, url, html):
        """Parse the HTML Body to take out all included urls"""
        try:
            sel = Selector(text=html)
            title = sel.css('title::text').extract_first()
            divs = sel.xpath('//div')
            divs = divs.xpath('.//p')
            page_url_list = divs.css('a::attr(href)').extract()

        except Exception as e:
            raise e

        if title:
            self.titltes[url] = title

        if page_url_list:
            for element in page_url_list:
                url_temp = 'https://en.wikipedia.org' + element
                self.page_url_list.append(url_temp)

    async def get_results(self, url, task_id):
        """Wrapper Functions to call request and parse function"""
        if self.request_count <= self.url_limit:
            print('Thread {} Sending Request'.format(task_id))
            url, html = await self.get_body(url)
            print('Thread {} Parsing Results'.format(task_id))
            self.__parse_results(url, html)
            print('Thread {} Completed'.format(task_id))
            return 'Completed'

    async def handle_tasks(self, task_id, work_queue):
        while not work_queue.empty():
            current_url = await work_queue.get()

            try:
                task_status = await self.get_results(current_url, task_id)
                await asyncio.sleep(self.download_delay)

            except Exception as e:
                logging.exception('Error for {}'.format(current_url), exc_info=True)
                await asyncio.sleep(self.download_delay)

    def eventloop(self):
        q = asyncio.Queue()
        [q.put_nowait(url) for url in self.urls[0:self.url_limit]]
        loop = asyncio.get_event_loop()

        tasks = [self.handle_tasks(task_id, q, ) for task_id in range(self.max_threads)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def main():
    wiki_urls = crawl.get_urls()
    max_threads = 10
    max_urls = 100
    time_delay = 5

    concurrent_crawler = ConcurrentCrawler(wiki_urls, max_threads, max_urls, time_delay)
    concurrent_crawler.eventloop()

    average = concurrent_crawler.length / max_urls

    print('\nTotal Requests made: {}'.format(concurrent_crawler.request_count))
    print('Total Bytes Downloaded: {}'.format(sizeof_fmt(concurrent_crawler.length)))
    print('Average File Size: {}'.format(sizeof_fmt(average)))


if __name__ == '__main__':

    main()

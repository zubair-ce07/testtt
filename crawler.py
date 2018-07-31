import asyncio
import argparse
from time import time
from requests import get
from requests.compat import urljoin
from requests.compat import urlparse

from parsel import Selector


class ConcurrentCrawler:
    def __init__(self, base_url, limit, max_workers, download_delay):
        self.loop = asyncio.get_event_loop()
        self.max_workers = asyncio.Semaphore(max_workers)
        self.maximum_url_to_visit = limit
        self.download_delay = download_delay
        self.downloaded_bytes = 0
        self.visited_urls = []
        self.queued_urls = []
        self.scheduled_tasks = []
        self.event = asyncio.Event()
        self.domain = urlparse(base_url).netloc

    def validate_url(self, url):
        return urlparse(url).netloc == self.domain

    def absolute_url(self, base_url, url):
        return urljoin(base_url, url)

    def extract_links(self, response):
        return Selector(text=response.text).xpath("//a/@href").getall()

    def filter_urls(self, urls):
        return list({url for url in urls if self.validate_url(url)})

    async def make_request(self, url):
        print(f" URL :: {url}")
        return await self.loop.run_in_executor(None, get, url)

    def parse_response(self, future):
        self.event.clear()
        response = future.result()
        self.downloaded_bytes += len(response.text)
        absolute_urls = [self.absolute_url(response.url, url) for url in self.extract_links(response)]
        self.queued_urls.extend(self.filter_urls(absolute_urls))
        self.event.set()

    async def schedule_requests(self):

        while self.queued_urls or self.scheduled_tasks:
            if len(self.visited_urls) == self.maximum_url_to_visit:
                break

            if not self.queued_urls:
                await self.event.wait()
                continue

            url = self.queued_urls.pop()
            if url in self.visited_urls:
                continue

            await self.max_workers.acquire()
            self.visited_urls.append(url)
            task = asyncio.ensure_future(self.make_request(url))
            task.add_done_callback(self.parse_response)
            task.add_done_callback(lambda f: self.max_workers.release())
            task.add_done_callback(lambda f: self.scheduled_tasks.remove(f))
            self.scheduled_tasks.append(task)
            await asyncio.sleep(self.download_delay)

        await asyncio.gather(*self.scheduled_tasks)

    def run(self, base_url):
        try:
            self.queued_urls.append(base_url.strip())
            self.loop.run_until_complete(self.schedule_requests())
        except asyncio.InvalidStateError:
            print(" Error:: Some Fatal problem occur in  in Event loop")
        finally:
            self.loop.close()

    def generate_report(self):
        print(f'Total Downloaded Bytes :: {self.downloaded_bytes} bytes')
        print(f'Total Request Made :: {len(self.visited_urls)}')
        print(f'Average Page Size:: {round(self.downloaded_bytes/len(self.visited_urls),2)}')


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s --base_url', dest='base_url', action="store",
                        default="https://arbisoft.com/", help="Base Url", type=str)
    parser.add_argument('-m --max_urls', dest='max_url_to_visit', help="Maximum Url to Visit",
                        action="store", default=20, type=int)
    parser.add_argument('-r --max_worker', dest='max_num_of_request',
                        help="Maximum Number of Request",
                        action="store", default=5, type=int)
    parser.add_argument('-d -- download_delay', dest='download_delay', help="Download Delay",
                        action="store", default=1, type=int)
    return parser.parse_args()


def main():
    arguments = parse_arguments()

    start_time = time()
    crawler = ConcurrentCrawler(arguments.base_url, arguments.max_url_to_visit,
                                arguments.max_num_of_request,
                                arguments.download_delay)
    crawler.run(arguments.base_url)
    print(f"\nTotal Time Taken :: {round((time() - start_time),2)} s")
    crawler.generate_report()


if __name__ == "__main__":
    main()

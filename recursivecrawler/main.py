import argparse
import asyncio
import parsel
import requests
import time

from concurrent.futures import ProcessPoolExecutor
from urllib.parse import urljoin


class RecursiveCrawler:
    def __init__(self, args):
        self.args = args
        self.total_bytes = 0
        self.total_requests = 0
        self.urls = self._fetch_urls(self.args.url, max_count=self.args.max_urls_count)

    def _request_and_increase_count(self, url: str) -> requests.Response or None:
        try:
            response = requests.get(url)
            self.total_requests += 1
            return response
        except Exception as e:
            print(f'Unable to process URL: {url}')
            return None

    def _fetch_urls(self, input_url: str, max_count: int) -> list:
        response = self._request_and_increase_count(input_url)
        selector = parsel.Selector(text=response.text)
        urls = [urljoin(input_url, url) for url in selector.css('a::attr(href)').getall()]

        if len(urls) < max_count:
            urls.extend(self._fetch_urls(urls[0], max_count=max_count - len(urls)))

        return urls[:max_count]

    def _list_to_async_queue(self, inputs: list) -> asyncio.Queue:
        queue = asyncio.Queue(maxsize=len(inputs))
        for value in inputs:
            queue.put_nowait(value)
        return queue

    async def _async_url_worker(self, index: int, queue: asyncio.Queue, download_delay: int) -> None:
        while not queue.empty():
            url = await queue.get()
            print(f'Worker {index} got url {url}')
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, self._request_and_increase_count, url)

            if response:
                print(f'Worker {index} read {len(response.content)} bytes')
                self.total_bytes += len(response.content)

            queue.task_done()
            print(f'Urls left: {queue.qsize()}')
            await asyncio.sleep(download_delay)

    def _parallel_url_worker(self, args: tuple) -> int:
        time.sleep(args[0])
        print(f'Working on URL {args[1]}')
        response = self._request_and_increase_count(args[1])
        return len(response.content) if response else 0

    async def execute(self) -> tuple:
        if self.args.parallel:
            executor = ProcessPoolExecutor(max_workers=self.args.concurrent_requests)
            process_args = ((self.args.download_delay, url) for url in self.urls)
            results = executor.map(self._parallel_url_worker, process_args)

            for result in results:
                self.total_requests += 1
                self.total_bytes += result

        else:
            urls_queue = self._list_to_async_queue(self.urls)
            tasks = []

            for task_index in range(self.args.concurrent_requests):
                tasks.append(asyncio.create_task(self._async_url_worker(task_index, queue=urls_queue,
                                                                        download_delay=self.args.download_delay)))

            await urls_queue.join()
            await asyncio.gather(*tasks)

        return self.total_requests, self.total_bytes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', '-u', type=str, required=True)
    parser.add_argument('--parallel', action='store_true')
    parser.add_argument('-concurrent_requests', '-ccr', type=int, default=5)
    parser.add_argument('-max_urls_count', '-uc', type=int, default=500)
    parser.add_argument('-download_delay', '-d', type=int, default=0)

    args = parser.parse_args()
    crawler = RecursiveCrawler(args)
    total_requests, total_bytes = asyncio.run(crawler.execute())

    print(f'Total Requests: {total_requests}')
    print(f'Total data read: {total_bytes} bytes')
    print(f'Average page size: {total_bytes / args.max_urls_count} bytes')


if __name__ == '__main__':
    start_time = time.monotonic()
    main()
    print(f'Finished in {round(time.monotonic() - start_time, 1)} seconds')

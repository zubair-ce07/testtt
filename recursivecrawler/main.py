import argparse
import asyncio
import parsel
import requests

from concurrent.futures import ProcessPoolExecutor


class CrawlerRecord:
    def __init__(self, total_bytes_read, total_requests):
        self.total_bytes_read = total_bytes_read
        self.total_requests = total_requests


final_record = CrawlerRecord(total_bytes_read=0, total_requests=0)


def request_and_increase_count(url):
    response = requests.get(url)
    final_record.total_requests += 1
    return response


def fetch_urls(url: str, max_count: int, total_urls: list = [], recursive_call=False, return_list=False):
    """
    Recursively calls itself until the max_count requirement is met
    """
    response = request_and_increase_count(url)
    selector = parsel.Selector(text=response.text)

    a_tags = selector.css('a')
    urls = [f'http:{a_tag.attrib["href"]}' for a_tag in a_tags if a_tag.attrib.get('href')]
    # total_urls.extend(urls)
    if len(total_urls) < max_count:
        fetch_urls(urls[0],
                   max_count=max_count - len(total_urls),
                   total_urls=total_urls, recursive_call=True)
    elif recursive_call:
        return None

    if return_list:
        return total_urls[:max_count]

    queue = asyncio.Queue(maxsize=max_count)
    total_urls = total_urls[:max_count]
    for url in total_urls:
        queue.put_nowait(url)
    return queue


async def async_worker(index:int, queue: asyncio.Queue, download_delay: int) -> None:
    while True:
        url = await queue.get()
        print(f'Worker {index} got url {url}')
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, request_and_increase_count, url)
        print(f'Worker {index} read {len(response.content)} bytes')
        final_record.total_bytes_read += len(response.content)
        queue.task_done()
        print(f'Urls left: {queue.qsize()}')
        await asyncio.sleep(download_delay)


def parallel_worker(url:str):
    print(f'Working on URL {url}')
    response = requests.get(url)
    return len(response.content)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', '-u', type=str)
    parser.add_argument('--parallel', action='store_true')
    parser.add_argument('-concurrent_requests', '-ccr', type=int, required=False, default=5)
    parser.add_argument('-max_urls_count', '-uc', type=int, required=False, default=500)
    parser.add_argument('-download_delay', '-d', type=int, required=False, default=0)

    args = parser.parse_args()
    if args.parallel:
        urls = fetch_urls(url=args.url, max_count=args.max_urls_count, return_list=True)
        executor = ProcessPoolExecutor(max_workers=args.concurrent_requests)
        results = executor.map(parallel_worker, urls)
        for result in results:
            result.total_bytes_read += result
            result.total_requests += 1
    else:
        urls_queue = fetch_urls(url=args.url, max_count=args.max_urls_count)
        tasks = []
        for task_index in range(args.concurrent_requests):
            tasks.append(asyncio.create_task(async_worker(task_index, queue=urls_queue,
                                                          download_delay=args.download_delay)))
        await urls_queue.join()

    print(f'Total Requests: {final_record.total_requests}')
    print(f'Total data read: {final_record.total_bytes_read} bytes')
    print(f'Average page size: {final_record.total_bytes_read / args.max_urls_count} bytes')


if __name__ == '__main__':
    asyncio.run(main())

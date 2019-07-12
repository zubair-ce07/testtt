import argparse
import asyncio
import parsel
import requests
import time

from concurrent.futures import ProcessPoolExecutor
from crawlrecord import CrawlerRecord


final_record = CrawlerRecord(total_bytes_read=0, total_requests=0)


def request_and_increase_count(url: str) -> requests.Request or None:
    try:
        response = requests.get(url)
        final_record.total_requests += 1
        return response
    except Exception as e:
        print(f'Unable to process URL: {url}')
        return None


def url_validator(url: str) -> str:
    if url.startswith('//'):
        url = f'https:{url}'
    elif not(url.startswith('http://') or url.startswith('https://')):
        url = f'https://{url}'
    return url


def fetch_urls(url: str, max_count: int) -> list:
    response = request_and_increase_count(url)
    selector = parsel.Selector(text=response.text)
    a_tags = selector.css('a')
    urls = [url_validator(a_tag.attrib['href']) for a_tag in a_tags if a_tag.attrib.get('href')]
    if len(urls) < max_count:
        urls.extend(fetch_urls(urls[0], max_count=max_count - len(urls)))
    return urls[:max_count]


def list_to_async_queue(inputs: list) -> asyncio.Queue:
    queue = asyncio.Queue(maxsize=len(inputs))
    for input in inputs:
        queue.put_nowait(input)
    return queue


async def async_url_worker(index:int, queue: asyncio.Queue, download_delay: int) -> None:
    while True:
        url = await queue.get()
        print(f'Worker {index} got url {url}')
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, request_and_increase_count, url)
        if response:
            print(f'Worker {index} read {len(response.content)} bytes')
            final_record.total_bytes_read += len(response.content)
        queue.task_done()
        print(f'Urls left: {queue.qsize()}')
        await asyncio.sleep(download_delay)


def parallel_url_worker(args: tuple) -> int:
    time.sleep(args[0])
    print(f'Working on URL {args[1]}')
    response = request_and_increase_count(args[1])
    return len(response.content) if response else 0


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', '-u', type=str, required=True)
    parser.add_argument('--parallel', action='store_true')
    parser.add_argument('-concurrent_requests', '-ccr', type=int, default=5)
    parser.add_argument('-max_urls_count', '-uc', type=int, default=500)
    parser.add_argument('-download_delay', '-d', type=int, default=0)

    args = parser.parse_args()
    urls = fetch_urls(url=args.url, max_count=args.max_urls_count)

    if args.parallel:
        executor = ProcessPoolExecutor(max_workers=args.concurrent_requests)
        process_args = ((args.download_delay, url) for url in urls)
        results = executor.map(parallel_url_worker, process_args)

        for result in results:
            final_record.total_bytes_read += result
            final_record.total_requests += 1

    else:
        urls_queue = list_to_async_queue(urls)
        tasks = []

        for task_index in range(args.concurrent_requests):
            tasks.append(asyncio.create_task(async_url_worker(task_index, queue=urls_queue,
                                                              download_delay=args.download_delay)))

        await urls_queue.join()

    print(f'Total Requests: {final_record.total_requests}')
    print(f'Total data read: {final_record.total_bytes_read} bytes')
    print(f'Average page size: {final_record.total_bytes_read / args.max_urls_count} bytes')


if __name__ == '__main__':
    start_time = time.monotonic()
    asyncio.run(main())
    print(f'Finished in {time.monotonic() - start_time} seconds')

import asyncio
from time import time
from urllib.parse import urlparse
import argparse

from crawl_worker import CrawlWorker

def setup_arguments():
    parser = argparse.ArgumentParser(description='URL data monitor.')

    parser.add_argument('-download_delay', type=int, default=100, \
        help='Time delay in ms for each worker to hit URL.')

    parser.add_argument('-page_count', type=int, default=15, \
        help='Total number of URLs to hit.')

    parser.add_argument('-c_requests', type=int, default=5, \
        help='Total number of cuncurrent requests')

    return parser.parse_args()

async def create_worker():
    worker = CrawlWorker()
    await worker.request()

async def main():

    commandline_arguments = setup_arguments()
    CrawlWorker.cuncurrent_request_allowed = commandline_arguments.c_requests
    CrawlWorker.download_delay = commandline_arguments.download_delay / 1000
    CrawlWorker.total_pages_to_load = commandline_arguments.page_count

    url = urlparse("https://arbisoft.com/")
    await CrawlWorker.url_queue.put(url)
    crawl_workers = set()

    start_time = time()
    while CrawlWorker.page_loaded_successfully < CrawlWorker.total_pages_to_load:
        if CrawlWorker.loading_request_made < CrawlWorker.total_pages_to_load:
            if len(crawl_workers) >= CrawlWorker.cuncurrent_request_allowed:
                _done, crawl_workers = await asyncio.wait(
                    crawl_workers, return_when=asyncio.FIRST_COMPLETED)
            await asyncio.sleep(CrawlWorker.download_delay)
            crawl_workers.add(loop.create_task(create_worker()))
        else:
            await asyncio.wait(crawl_workers, return_when=asyncio.FIRST_COMPLETED)

    await asyncio.wait(crawl_workers)

    total_bytes_downloaded = CrawlWorker.total_bytes_downloaded
    total_pages_loaded = CrawlWorker.page_loaded_successfully
    avg_page_size = total_bytes_downloaded / total_pages_loaded

    print(f"\nTotal pages loaded: {total_pages_loaded}")
    print(f"Total bytes downloaded: {total_bytes_downloaded}")
    print(f"Average page size: {avg_page_size}")
    print(f"Total time taken: {(time() - start_time)} seconds\n")


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
    loop.run_until_complete(loop.shutdown_asyncgens())
finally:
    loop.close()

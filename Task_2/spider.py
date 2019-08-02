import asyncio
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

async def main():

    commandline_arguments = setup_arguments()
    worker = CrawlWorker(
        commandline_arguments.page_count,
        commandline_arguments.c_requests,
        commandline_arguments.download_delay / 1000,
        "https://arbisoft.com/",
        loop
    )
    await worker.start_crawling()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
    loop.run_until_complete(loop.shutdown_asyncgens())
finally:
    loop.close()

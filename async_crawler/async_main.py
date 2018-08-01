import argparse
import asyncio
from async_crawler.crawler import Crawler


def main(argv):
    crawler = Crawler(argv.url, argv.workers, argv.delay, argv.max_urls)
    future = asyncio.Task(crawler.crawl())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(future)
    loop.close()
    total_data, total_urls = future.result()
    print("Crawler Crawled {} bytes of total data and {} URLs".format(total_data, total_urls))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="Website url to _request")
    parser.add_argument('-w', "--workers", type=int, default=1, help="Number of worker threads")
    parser.add_argument('-d', "--delay", type=int, default=0, help="Download delay for making two concurrent requests")
    parser.add_argument('-m', "--max-urls", type=int, default=0, help="Maximum urls to visit")
    args = parser.parse_args()
    main(args)

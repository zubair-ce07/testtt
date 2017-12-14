import asyncio
import argparse
from datetime import datetime

import requests
from parsel import Selector


class ConcurrentSpider:
    def __init__(self, base_url, max_urls=50, concurrent_req=20, delay=0):
        self.base_url = base_url
        self.max_urls = max_urls
        self.concurrent_req = concurrent_req
        self.delay = delay
        self.total_size = 0

    def get_links(self):
        res = requests.get(self.base_url)
        text = res.text

        sel = Selector(text=text)
        links = sel.css('a[href^=http]').xpath('@href').extract()
        del links[self.max_urls:]
        # print(len(links))
        # print(links)
        return links

    async def spider_worker(self, loop, links):
        futures = []
        if len(links) < self.concurrent_req:
            self.concurrent_req = len(links)

        for i in range(self.concurrent_req):
            futures.append(loop.run_in_executor(None, requests.get, links.pop(0)))

        for response in await asyncio.gather(*futures):
            await asyncio.sleep(self.delay)
            page_size = response.headers.get('content-length')
            if page_size:
                self.total_size += int(page_size)
        if links:
            await self.spider_worker(loop, links)
        else:
            return 0

    def run_spider(self):
        start_time = datetime.now()

        print('running spider...')
        links = self.get_links()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.spider_worker(loop, links))
        loop.close()

        time_taken = datetime.now() - start_time
        print('total request made: ', self.max_urls)
        print('total bytes downloaded: ', self.total_size, 'Bytes')
        print('Average page size: ', self.total_size / self.max_urls)
        print('time taken: ', time_taken.total_seconds(), 'sec')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--maxurls',
                        help='maximum pages to crawl'
                        )

    parser.add_argument('-c', '--conreq',
                        help='No of concurrent requests'
                        )

    parser.add_argument('-d', '--delay',
                        help='download delay per page'
                        )

    parser.add_argument('-b', '--base_url',
                        help='Base url to crawl')

    args = parser.parse_args()
    max_urls = int(args.maxurls) if args.maxurls else 50
    con_req = int(args.conreq) if args.conreq else 20
    delay = int(args.delay) if args.delay else 0
    base_url = args.base_url if args.base_url \
        else r'https://en.wikipedia.org/wiki/Python_(programming_language)'

    spider = ConcurrentSpider(base_url, max_urls, con_req, delay)
    spider.run_spider()


if __name__ == "__main__":
    main()


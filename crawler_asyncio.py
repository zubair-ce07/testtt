import asyncio
from urllib import parse

import requests
import parsel


class Crawler:

    def __init__(self, web_url):
        self.website = web_url
        self.bytes_downloaded = 0
        self.visited_urls = set()

    async def fetch_page(self, url, delay):
        print(f"Requesting :{url}")
        await asyncio.sleep(delay)
        response = requests.get(url)
        self.bytes_downloaded = self.bytes_downloaded + len(response.content)
        return response.text

    async def extract_urls(self, url, delay):
        url_complete = parse.urljoin(self.website, url)
        page_text = await self.fetch_page(url_complete, delay)
        selector = parsel.Selector(text=page_text)
        found_urls = selector.css("a::attr(href)").extract()
        found_urls = set(found_urls)
        filtered_urls = self.filter_absolute_urls(found_urls)
        print(f"Extracted {len(filtered_urls)} urls from {url_complete}")
        return filtered_urls

    def filter_absolute_urls(self, urls):
        filtered_urls = set(filter(lambda url: not parse.urlparse(url).netloc
                            and not parse.urlparse(url).scheme == 'mailto', urls))
        return filtered_urls

    async def crawl_async(self, url_limit, request_limit, download_delay):
        found_urls = set('/')
        future_requests = []
        self.visited_urls = set()
        while True:
            for request_no in range(request_limit):
                if found_urls:
                    current_url = found_urls.pop()
                    future_requests.append(self.extract_urls(current_url, download_delay))
                    self.visited_urls = self.visited_urls.union({current_url})
                    if len(self.visited_urls) == url_limit:
                        break
            for request in asyncio.as_completed(future_requests):
                found_urls = found_urls.union(await request)
            found_urls = found_urls.difference(self.visited_urls)
            future_requests = []
            if len(self.visited_urls) == url_limit:
                break

    def crawl_report(self):
        print(f"Number of requests: {len(self.visited_urls)}.")
        print(f"Bytes downloaded: {self.bytes_downloaded}B.")
        print(f"Average page size : {self.bytes_downloaded//len(self.visited_urls)}B.")


def main():
    loop = asyncio.get_event_loop()
    arbisoft_crawler = Crawler('http://arbisoft.com/')
    loop.run_until_complete(arbisoft_crawler.crawl_async(20, 5, 0.1))
    arbisoft_crawler.crawl_report()
    loop.close()


if __name__ == '__main__':
    main()

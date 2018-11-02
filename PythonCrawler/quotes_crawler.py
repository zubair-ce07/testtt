import json
import asyncio
import requests
from parsel import Selector
from threading import RLock
from urllib.parse import urljoin
from concurrent.futures import ProcessPoolExecutor


class QuotesSpider:
    """
    Spider class to crawl quote items without using scrapy
    """
    def __init__(self, start_url, output="data.json", max_requests=2, delay=0.5, urls=200):
        """
        Initializing class variables and result holders
        :param start_url: url to parse
        :param max_requests: max concurrent requests allowed
        :param delay: download delay between requests
        :param urls: maximum no of urls to visit
        """
        # user controllable settings
        self.max_concurrent_requests = max_requests
        self.download_delay = delay
        self.output_file = output
        self.max_urls = urls

        # To report in end
        self.total_bytes = 0
        self.total_requests = 0
        self.average_page_size = 0
        self.total_items_scrapped = 0

        # class variables to use for parallel execution
        self.executor = ProcessPoolExecutor(max_workers=max_requests)
        self.loop = asyncio.get_event_loop()
        self.start_url = start_url
        self.lock = RLock()

    def run(self):
        """
        Runs the parse function with given start url in constructor
        :return: None
        """
        self.loop.run_until_complete(self.parse(self.start_url))
        self.report_results()
        self.loop.close()

    async def request(self, url):
        """
        Asynchronously fetching data from url by GET request
        :param url: url to fetch
        :return: Selector for url response data
        """
        if self.total_requests < self.max_urls:
            await asyncio.sleep(self.download_delay)
            request_future = self.executor.submit(requests.get, url)
            response = request_future.result().text
            if response:
                self.total_bytes += len(response)
                self.total_requests += 1
                return Selector(text=response)
        else:
            print("MAX URL Limit {} reached".format(self.max_urls))
            self.report_results()
            exit(0)

    async def parse(self, url):
        """
        Parsing quotes from page, and creating requests for next items
        :param url: page url to parse quotes from
        :return: None
        """
        sel = await self.request(url)
        quotes = sel.css("div.quote")
        tasks = []
        for quote in quotes:
            quote_body = quote.css("span.text::text").get()
            tags = quote.css("a.tag::text").getall()
            author_link = quote.css("small.author+a::attr(href)").get()
            quote_item = {
                'text': quote_body.strip(),
                'tags': tags,
            }
            author_url = urljoin(url, author_link)
            future_task = asyncio.ensure_future(
                self.parse_author(author_url, quote_item))
            tasks.append(future_task)

        await asyncio.gather(*tasks)
        next_page = sel.css("li.next>a::attr(href)").get()
        if next_page:
            next_page_url = urljoin(url, next_page)
            await self.parse(next_page_url)
        else:
            self.report_results()

    async def parse_author(self, author_url, quote_item):
        """
        Parsing author information and
        writing quote item to output file
        :param author_url: author profile url
        :param quote_item: quote item to append author information
        :return: None
        """
        sel = await self.request(author_url)
        title = sel.css("h3::text").get()
        birth_date = sel.css("span.author-born-date::text").get()
        birth_location = sel.css("span.author-born-location::text").get()
        description = sel.css("div.author-description::text").get()
        quote_item.update({'author': {
            'name': title.strip(),
            'birth-date': birth_date,
            'birth-location': birth_location,
            'description': description.strip(),
        }})
        self.total_items_scrapped += 1
        # write item to file
        print(quote_item)
        self.write_to_file(quote_item)

    def write_to_file(self, quote_item):
        """
        writing the quote_item to output file
        :param quote_item: item to write
        :return: None
        """
        with self.lock:
            with open(self.output_file, 'a') as output:
                json.dump(quote_item, output, ensure_ascii=False)

    def report_results(self):
        """
        Calculating and Reporting result values
        :return: None
        """
        self.average_page_size = self.total_bytes/self.total_requests
        print("Total quotes: {}".format(self.total_items_scrapped))
        print("Total requests: {}".format(self.total_requests))
        print("Total Bytes: {}".format(self.total_bytes))
        print("Average Page Size: {} bytes".format(self.average_page_size))


spider = QuotesSpider("http://quotes.toscrape.com/")
spider.run()

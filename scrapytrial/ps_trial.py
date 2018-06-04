import re

from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from ..items import ScrapyTrialItem
from scrapy.loader import ItemLoader


class PSTrial(CrawlSpider):
    name = 'ps_trial'
    allowed_domains = ['pstrial-2018-05-21.toscrape.com']
    start_urls = ['http://pstrial-2018-05-21.toscrape.com/browse/summertime',
                  'http://pstrial-2018-05-21.toscrape.com/browse/insunsh']

    start_dict = [
        {
            'url': 'http://pstrial-2018-05-21.toscrape.com/browse/summertime',
            'category': 'summertime'
        },
        {
            'url': 'http://pstrial-2018-05-21.toscrape.com/browse/insunsh',
            'category': 'insunsh'
        }
    ]

    def start_requests(self):
        for dict in self.start_dict:
            request = Request(dict.get('url'), callback=self.parse)
            request.meta['category'] = dict.get('category')
            yield request

    def parse(self, response):
        sub_urls = response.xpath('//*[@id="subcats"]//a[h3]')
        for sub_url in sub_urls:
            url = sub_url.css('a::attr(href)').extract_first()
            category = sub_url.css('h3::text').extract_first()
            request = Request(response.urljoin(url), callback=self.parse)
            request.meta['category'] = "{}//{}".format(response.meta.get('category'), category)
            yield request

        if not sub_urls:
            yield self.pagination(response)
            item_urls = response.xpath('//*[contains(@href, "item")]//@href').extract()
            for item_url in item_urls:
                request = Request(response.urljoin(item_url), callback=self.parse_item)
                request.meta['category'] = response.meta.get('category')
                yield request

    def pagination(self, response):
        next_url = response.xpath('//a[contains(text(), "Next")]//@href').extract_first()
        request = Request(response.urljoin(next_url), callback=self.parse)
        request.meta['category'] = response.meta.get('category')
        return request

    def parse_item(self, response):
        loader = ItemLoader(item=ScrapyTrialItem(), response=response)

        loader.add_value('url', response.url)
        loader.add_xpath('artist', '//*[@itemprop="artist"]//text()')
        loader.add_xpath('title', '//*[@itemprop="name"]//text()')
        loader.add_xpath('description', '//*[@itemprop="description"]//text()')

        image_url = response.urljoin(response.xpath('//img/@src').extract_first())
        loader.add_value('image', image_url)

        raw_dimension = response.xpath('//dl//dt[text()="Dimensions"]/following::dd[1]/text()').extract_first()
        if raw_dimension:
            raw_area = re.findall('\(.*cm?\)', raw_dimension)
            if raw_area:
                dimension = re.findall('([+-]?[0-9]*[.]?[0-9]+)',raw_area[0])
                if len(dimension) == 2:
                    loader.add_value('height', float(dimension[0]))
                    loader.add_value('width', float(dimension[1]))
                elif len(dimension) == 1:
                    loader.add_value('height', float(dimension[0]))

        loader.add_value('path', response.meta.get('category').split("//"))

        yield loader.load_item()

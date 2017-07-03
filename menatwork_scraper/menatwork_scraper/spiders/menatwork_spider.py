import scrapy
import w3lib.url
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule

from menatwork_scraper.items import Product


class MySpider(CrawlSpider):
    name = 'menatwork'
    start_urls = ['https://www.menatwork.nl']
    rules = (
        Rule(
            LinkExtractor(allow='.*nl_NL/dames/.*', process_value=w3lib.url.url_query_cleaner)
        ),
        Rule(
            LinkExtractor(allow='.+\d{18}.html.+'),
            callback='parse_product_page'
        ),
    )

    def parse_product_page(self, response):

        a_product = Product()
        a_product['name'] = response.xpath('//h1[@class="product-name"]/text()').extract_first()
        a_product['size'] = {}

        product_color = response.css('li.selected-value::text').extract_first()
        size_variants = response.xpath('//select[@class="variation-select "]/option/text()').extract()
        size_variants = list(map(str.strip, size_variants))

        a_product['size'][product_color] = size_variants

        more_size_urls = response.xpath('//ul[contains(@class,"color")]/li[@class="selectable"]/a/@href').extract()
        if more_size_urls:
            size_url = more_size_urls.pop()
            yield scrapy.Request(url=size_url, callback=self.get_product_size,
                                 meta={'product': a_product, 'urls': more_size_urls})
        else:
            yield a_product

    def get_product_size(self, response):
        a_product = response.meta['product']
        more_size_urls = response.meta['urls']

        product_color = response.css('li.selected-value::text').extract_first()
        size_variants = response.xpath('//select[@class="variation-select "]/option/text()').extract()
        size_variants = list(map(str.strip, size_variants))
        a_product['size'][product_color] = size_variants

        if more_size_urls:
            size_url = more_size_urls.pop()
            yield scrapy.Request(url=size_url, callback=self.get_product_size,
                                 meta={'product': a_product, 'urls': more_size_urls})
        else:
            yield a_product

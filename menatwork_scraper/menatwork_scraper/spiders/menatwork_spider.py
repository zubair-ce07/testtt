from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule

from menatwork_scraper.items import Product


class MySpider(CrawlSpider):
    name = 'menatwork'
    start_urls = ['https://www.menatwork.nl']
    rules = (
        Rule(
            LinkExtractor(allow='.*nl_NL/dames/nieuwe-collectie.*')
        ),
        Rule(
            LinkExtractor(allow='.+\d{18}.html.+'),
            callback='parse_product_page'
        ),
    )

    def parse_product_page(self, response):
        # yield product item here
        a_prodect = Product()
        a_prodect['name'] = response.xpath('//h1[@class="product-name"]/text()').extract_first()
        yield a_prodect

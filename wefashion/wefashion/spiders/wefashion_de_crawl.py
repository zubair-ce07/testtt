from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from wefashion.wefashion_de_parse import ProductParser


class WefashionDeCrawlSpider(CrawlSpider):
    name = 'wefashion-de-crawl'
    parser = ProductParser()
    allowed_domains = ['www.wefashion.de']
    start_urls = [
        # 'http://www.wefashion.de/'
        'https://www.wefashion.de/de_DE/herren/t-shirts/printed-t-shirts/'
    ]

    rules = (
        # Rule(LinkExtractor(restrict_css=['.header-top-level-menu', '#category-level-0']),
        #      follow=True,
        #      callback='parse_category_page'),
        Rule(LinkExtractor(restrict_css=['.header-top-level-menu']), callback='parse'),
        Rule(LinkExtractor(restrict_css='.product-image'), callback='parse_item'),
    )

    def parse(self, response):

        for request in super(WefashionDeCrawlSpider, self).parse(response):
            print(f"HAMZA {response.css('.image-holder::attr(data-color-id)').extract_first()}")
            yield request

    # def parse_item(self, response):
    #     return self.parser.parse(response)

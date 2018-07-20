import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArtsperSpider(CrawlSpider):
    name = 'artsper'
    allowed_domains = ['artsper.com']
    download_delay = 3

    rules = (
        Rule(LinkExtractor(restrict_css=['#desktop-menu .container ul',
                                         '#facets.empty.clearfix li',
                                         '.all-pages'], allow='contemporary-artworks')),
        Rule(LinkExtractor(restrict_css='.container.artwork figure [data-item-artwork]'), callback='parse_products')
    )

    def start_requests(self):
        yield Request('https://www.artsper.com/en/profile/currency/3', callback=self.main_link)

    def main_link(self, response):
        yield Request('https://www.artsper.com/en/', callback=self.parse)

    def parse_products(self, response):
        item = {
            'product_name': self.extract_product_name(response),
            'category': self.extract_category(response),
            'currency': self.extract_currency(response),
            'price': self.extract_price(response),
            'sku': self.extract_sku_id(response),
            'stock': self.extract_stock(response),
            'size': self.extract_size(response),
            'tags': self.extract_tag(response),
            'care': self.extract_about(response),
            'description': self.extract_description(response),
            'image_urls': self.extract_image_urls(response),
            'url': response.url,
        }
        yield item

    def extract_tag(self, response):
        return response.css('#tags .pointer h2::text').extract()

    def extract_currency(self, response):
        return response.css('#currency .active::text').extract()

    def extract_price(self, response):
        price = response.css('#sticky .relative p::attr(class)').extract_first()
        return response.css('#sticky .relative p::text').extract_first()[1:] if 'price' in price else 'sold out'

    def extract_stock(self, response):
        return 'Not available' if self.extract_price(response) == 'sold out' else 'Available'

    def extract_image_urls(self, response):
        return response.css('#img_original::attr(src)').extract_first()

    def extract_size(self, response):
        return response.css('.category.artwork-measure-sticky::text').extract_first()

    def extract_product_name(self, response):
        return response.css('.primary-title::text').extract()[0]

    def extract_about(self, response):
        return self.clean_spaces(''.join(care for care in response.css('.content-tab .description::text').extract()))

    def extract_category(self, response):
        return response.css('.category::text').extract_first()

    def extract_description(self, response):
        return self.clean_spaces(response.css('.secondary-title::text').extract_first())

    def extract_sku_id(self, response):
        return response.css('#sticky span::attr(data-id)').extract()[0]

    def clean_spaces(self, string):
        return ' '.join(re.split("\s+", string, flags=re.UNICODE))

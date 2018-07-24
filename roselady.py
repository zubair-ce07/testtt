from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class RoseladySpider(CrawlSpider):
    name = 'roselady'
    allowed_domains = ['theroselady.com']
    start_urls = ['https://www.theroselady.com/17/home.htm']

    rules = (
        Rule(LinkExtractor(allow=['/cat-', '/Cat-', 'SortOrder='])),
        Rule(LinkExtractor(allow=['/Prod', '/prod']), callback='parse_products'),
    )

    def parse_products(self, response):
        item = {
            'url': response.url,
            'stock': self.extract_stock(response),
            'price': self.extract_price(response),
            'sku': self.extract_item_number(response),
            'title': self.extract_product_name(response),
            'image_url': self.extract_image_urls(response),
            'disclosure': self.extract_disclosure(response),
            'description': self.extract_description(response),
        }
        yield item

    def extract_price(self, response):
        price = response.css('#head meta[property="og:price:amount"]::attr(content)').extract_first().encode('utf-8')
        return '{0} {1}'.format(price, self.extract_currency(response))

    def extract_currency(self, response):
        return response.css('#head meta[property="og:price:currency"]::attr(content)').extract_first()

    def extract_stock(self, response):
        return response.css('#head meta[property="og:availability"]::attr(content)').extract_first()

    def extract_image_urls(self, response):
        return response.css('#head meta[property="og:image:url"]::attr(content)').extract_first()

    def extract_product_name(self, response):
        return response.css('#head meta[property="og:title"]::attr(content)').extract_first()

    def extract_description(self, response):
        return self.extract_description_disclosure(response).split('<br>')[0]

    def extract_item_number(self, response):
        return response.css('#ProductItemCode b::text').extract()[0]

    def extract_disclosure(self, response):
        if '<br>' in self.extract_description_disclosure(response):
            return self.extract_description_disclosure(response).split('<br>')[-1]
        return None

    def extract_description_disclosure(self, response):
        return response.css('#head meta[property="og:description"]::attr(content)').extract_first()

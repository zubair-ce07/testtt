import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request

from tradesy_crawler.items import TradesyCrawlerItem


class TradesyCrawler(CrawlSpider):

    name = 'tradesy-ca-crawl'
    allowed_domains = ['tradesy.com']
    start_urls = ['https://www.tradesy.com/']

    GENDER_MAP = {' men': 'men', " men's": 'men',
                  ' Men': 'men', " Men's": 'men'}

    listings_css = ['.trd-default-nav', '#pagination']
    products_css = ['.item-image']

    rules = (Rule(LinkExtractor(restrict_css=listings_css,
                                deny=('com/designers/', 'com/login/')), callback='parse'),
             Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'))

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers=headers,
                          cookies={'preferred-locale': 'en-CA', 'preferred-currency': 'CAD'})

    def parse_product(self, response):
        item = TradesyCrawlerItem()
        raw_product = self.raw_product(response)

        item['lang'] = 'en'
        item['market'] = 'CA'
        item['url'] = self.product_url(response)
        item['name'] = self.product_name(raw_product)
        item['brand'] = self.product_brand(raw_product)
        item['skus'] = self.skus(response, raw_product)
        item['gender'] = self.product_gender(raw_product)
        item['image_urls'] = self.parse_image_urls(response)
        item['category'] = self.product_category(raw_product)
        item['description'] = self.product_description(raw_product)
        item['retailer_sku'] = self.product_retailer_sku(raw_product)

        return item

    def product_url(self, response):
        return response.url

    def product_name(self, raw_product):
        return raw_product['defaults']['title']

    def product_brand(self, raw_product):
        return self.clean(raw_product['defaults']['brand'])

    def product_retailer_sku(self, raw_product):
        return raw_product['segmentProductIdentity']['sku']

    def product_category(self, raw_product):
        return self.clean(raw_product['defaults']['category'])

    def parse_image_urls(self, response):
        return response.css('.inner li img ::attr(src)').extract()

    def product_description(self, raw_product):
        return raw_product['fb']['fbDescription'].replace('\\', '')

    def clean(self, raw_text):
        return raw_text.replace('\n', '').replace('\t', '').replace(' ', '')

    def raw_product(self, response):
        css = 'script:contains("eventTrackingQueue") ::text'
        raw_product = response.css(css).re_first('productpage\s*=\s*({.*})')
        return json.loads(raw_product)

    def product_care(self, response):
        return response.css('.product-details-bullet-list > li::text').extract()

    def product_pricing(self, response):
        prev_prices = []
        price_css = '.item-price ::text'
        retail_price_css = '.item-price-retail ::text'
        list_price_css = '.item-price-original-list > span::text'

        price = self.clean(response.css(price_css).extract_first())
        prev_listing_price = response.css(list_price_css).extract_first()
        prev_retail_price = response.css(retail_price_css).extract_first()

        pricing = {'price': re.findall('(.?\d+\.\d*)', str(price))[0]}

        if prev_listing_price:
            prev_listing_price = self.clean(prev_listing_price)
            prev_prices.append(re.findall('(.?\d+\.\d*)', str(prev_listing_price))[0])

        if prev_retail_price:
            prev_retail_price = self.clean(prev_retail_price)
            prev_prices.append(re.findall('(.?\d+\.\d*)', str(prev_retail_price))[0])

        if prev_prices:
            pricing['previous_price'] = prev_prices

        return pricing

    def skus(self, response, raw_product):
        sku = self.product_pricing(response)
        currency = raw_product['segmentProductIdentity']['currency']
        sku['colour'] = raw_product['defaults']['color']
        sku['size'] = raw_product['defaults']['size']
        sku['currency'] = currency
        return sku

    def product_gender(self, raw_product):
        gender = 'women'
        description = self.product_description(raw_product)
        name = self.product_name(raw_product)

        for key, value in self.GENDER_MAP.items():
            if key in description:
                return value
            if key in name:
                return value
        return gender

import re

from scrapy.linkextractor import LinkExtractor
from scrapy.spider import Rule, CrawlSpider

from task3.items import DecimasItem


class DecimasSpider(CrawlSpider):
    FEED_EXPORT_ENCODING = "utf-8"
    name = "decimas"
    allowed_domains = ['decimas.es']
    start_urls = ['https://www.decimas.es/']

    rules = (Rule(LinkExtractor(restrict_css='.view_all')),
             Rule(LinkExtractor(restrict_css='.ambrands-list a')),
             Rule(LinkExtractor(restrict_css='.next.i-next')),
             Rule(LinkExtractor(restrict_css='.category-products .product-image'), callback='parse_item'))

    def parse_item(self, response):
        item = DecimasItem()
        sizes = self.get_sizes(response)
        item['name'] = self.get_title(response)
        item['categories'] = self.get_categories(self.get_title(response),
                                                 self.get_brand(response), self.get_gender(response))
        item['url'] = self.get_url(response)
        item['gender'] = self.get_gender(response)
        item['brand'] = self.get_brand(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        price = self.get_price(response)
        item['image_urls'] = self.get_image_urls(response)
        item['description'] = self.get_description(response)
        availability = self.get_availability(response)
        item['skus'] = self.get_skus(price, sizes, availability, self.get_retailer_sku(response))
        yield item

    def get_title(self, response):
        return response.css('h1::text').extract_first()

    def get_gender(self, response):
        if re.match(".*hombre.*", response.request.url):
            return "male"
        elif re.match(".*nino.*", response.request.url):
            return "boy"
        elif re.match(".*ninoa.*", response.request.url):
            return "girl"
        else:
            return "female"

    def get_brand(self, response):
        brands = ['arena', 'reebok', 'nike', 'head', 'tenth', 'adidas', 'cougar', 'plns', 'asics', 'new-balance',
                  'ipanema', 'joma', 'le-coq-sportif', 'polinesia', 'puma', 'rider', '47-brand']
        for key in brands:
            if re.match('.*' + key + '.*', response.request.url):
                return key

    def get_price(self, response):
        if response.css('.regular-price').extract():
            currency = response.css('.regular-price span::attr(content)').extract_first()
            regular_price = response.css('.regular-price::attr(content)').extract_first()
            regular_price = int(float(regular_price) * 100)
            return [currency, regular_price]
        else:
            currency = response.css('.special-price .price span::attr(content)').extract_first()
            old_price = response.css('.old-price .price::text').extract_first().strip()
            special1 = u"\u00a0"
            special2 = u"\u20ac"
            old_price = old_price.replace(special1, '')
            old_price = old_price.replace(special2, '')
            old_price = old_price.replace(',', '.')
            old_price = int(float(old_price) * 100)
            new_price = response.css('.special-price .price::attr(content)').extract_first()
            new_price = int(float(new_price) * 100)
            return [currency, old_price, new_price]

    def get_image_urls(self, response):
        return response.css('.thumb-link img::attr(src)').extract()

    def get_retailer_sku(self, response):
        return response.css('.skuProducto > span::text').extract_first().split(' ')[1]

    def get_url(self, response):
        return response.request.url

    def get_description(self, response):
        description = response.css('.descripcionProducto > div > p::text').extract_first()
        if description:
            description = description.strip()
            return description.split('.')

    def get_categories(self, title, brand, gender):
        return [title.split(' ')[0], gender, brand]

    def get_sizes(self, response):
        return response.css('#configurable_swatch_talla a::attr(name)').extract()

    def get_availability(self, response):
        return response.css('.extra-info .value::text').extract_first() == 'En existencia'

    def get_skus(self, prices, sizes, availability, sku_id):
        skus = []
        for size in sizes:
            sku = {}
            sku['size'] = size
            if len(prices) > 2:
                sku['price'] = prices[2]
                sku['old-price'] = prices[1]
            else:
                sku['price'] = prices[1]
            sku['currency'] = prices[0]
            if not availability:
                sku['out_of_stock'] = 'true'
            sku['sku_id'] = sku_id + '_' + size
            skus.append(sku)
        return skus

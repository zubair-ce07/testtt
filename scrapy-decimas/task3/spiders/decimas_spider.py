from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from task3.items import DecimasItem


class DecimasSpider(CrawlSpider):
    name = "decimas"
    allowed_domains = ['decimas.es']
    start_urls = ['https://www.decimas.es/']
    brands = set()

    rules = (Rule(LinkExtractor(restrict_css='.view_all')),
             Rule(LinkExtractor(restrict_css='.ambrands-list'), callback='parse_brands', follow=True),
             Rule(LinkExtractor(restrict_css='.next.i-next')),
             Rule(LinkExtractor(restrict_css='.category-products .product-image'), callback='parse_item'))

    def parse_brands(self, response):
        brand = response.request.url.split('/')[3].split('.')[0]
        DecimasSpider.brands.add(brand)

    def parse_item(self, response):
        item = DecimasItem()
        item['name'] = self.get_title(response)
        item['categories'] = self.get_categories(self.get_title(response),
                                                 self.get_brand(response), self.get_gender(response))
        item['url'] = self.get_url(response)
        item['gender'] = self.get_gender(response)
        item['brand'] = self.get_brand(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['image_urls'] = self.get_image_urls(response)
        item['description'] = self.get_description(response)
        item['skus'] = self.get_skus(response)
        yield item

    def get_title(self, response):
        return response.css('[itemprop="name"]::text').extract_first()

    def get_gender(self, response):
        genders = {'hombre': 'male', 'ninoa': 'girl', 'nino': 'boy', 'mujer': 'female'}
        for key in genders.keys():
            if key in response.url:
                return genders.get(key)

    def get_brand(self, response):
        for key in DecimasSpider.brands:
            if key in response.request.url:
                return key

    def get_price(self, response):
        prices = [r.strip() for r in response.css('.product-shop .price::text').extract()]
        prices = list(filter(None, prices))
        return [self.format_price(p) for p in prices]

    def format_price(self, price):
        special1 = u"\u00a0"
        special2 = u"\u20ac"
        price = price.replace(special1, '')
        price = price.replace(special2, '')
        price = price.replace(',', '.')
        return int(float(price) * 100)

    def get_image_urls(self, response):
        return response.css('.thumb-link img::attr(src)').extract()

    def get_retailer_sku(self, response):
        return response.css('.skuProducto > span::text').extract_first().split(' ')[1]

    def get_url(self, response):
        return response.url

    def get_description(self, response):
        description = response.css('[itemprop="description"]::text').extract()
        return [d.strip().split('.') for d in description]

    def get_categories(self, title, brand, gender):
        return [title.split(' ')[0], gender, brand]

    def get_sizes(self, response):
        return [r.strip() for r in response.css('.swatch-label::text').extract()]

    def get_availability(self, response):
        return response.css('.extra-info .value::text').extract_first() == 'En existencia'

    def get_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()

    def get_skus(self, response):
        sku_id = self.get_retailer_sku(response)
        availability = self.get_availability(response)
        prices = sorted(self.get_price(response))
        sizes = self.get_sizes(response)
        currency = self.get_currency(response)
        skus = []
        sku = {}
        if len(prices) > 1:
            sku['old-price'] = prices[1]
        sku['price'] = prices[0]
        sku['currency'] = currency
        if not availability:
            sku['out_of_stock'] = 'true'
        for size in sizes:
            sku.update({'size': size, 'sku_id': f'{sku_id}_{size}'})
            skus.append(sku.copy())
        return skus

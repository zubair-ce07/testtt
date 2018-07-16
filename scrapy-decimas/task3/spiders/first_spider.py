import re

from scrapy.linkextractor import LinkExtractor
from scrapy.spider import Rule, CrawlSpider

from task3.items import Task3Item


class DecimasSpider(CrawlSpider):
    DOWNLOAD_DELAY = 0
    name = "decimas"
    allowed_domains = ['decimas.es']
    start_urls = ['https://www.decimas.es/']

    rules = (Rule(LinkExtractor(restrict_css='a.view_all'),
                  follow=True),
             Rule(LinkExtractor(restrict_css='div.ambrands-list a'),
                  follow=True),
             Rule(LinkExtractor(restrict_css='div.category-products a.product-image'),
                  follow=False, callback='parse_item'))

    def parse_item(self, response):
        sizes = self.get_sizes(response)
        Task3Item.item['name'] = self.get_title(response)
        Task3Item.item['categories'] = self.get_categories(self.get_title(response),
                                                           self.get_brand(response), self.get_gender(response))
        Task3Item.item['url'] = self.get_url(response)
        Task3Item.item['gender'] = self.get_gender(response)
        Task3Item.item['brand'] = self.get_brand(response)
        Task3Item.item['retailer_sku'] = self.get_retailer_sku(response)
        price = self.get_price(response)
        Task3Item.item['image_urls'] = self.get_image_urls(response)
        Task3Item.item['description'] = self.get_description(response)
        availability = self.get_availability(response)
        Task3Item.item['skus'] = self.get_skus(price, sizes, availability, self.get_retailer_sku(response))
        yield Task3Item.item

    def get_title(self, response):
        return response.css('h1::text').extract_first()

    def get_gender(self, response):
        if re.match(".*hombre.*", response.request.url):
            return "masculino"
        elif re.match(".*nino.*", response.request.url):
            return "nino"
        elif re.match(".*ninoa.*", response.request.url):
            return "nina"
        else:
            return "hembra"

    def get_brand(self, response):
        brands = ['arena', 'reebok', 'nike', 'head', 'tenth', 'adidas', 'cougar', 'plns', 'asics', 'new-balance',
                      'ipanema', 'joma', 'le-coq-sportif', 'polinesia', 'puma', 'rider', '47-brand']
        for key in brands:
            if re.match('.*' + key + '.*', response.request.url):
                return key

    def get_price(self, response):
        if response.css('span.regular-price').extract():
            curr = response.css('span.regular-price span::attr(content)').extract_first()
            return [curr, int(float(response.css('span.regular-price::attr(content)').extract_first()) * 100)]
        else:
            curr = response.css('p.special-price span.price span::attr(content)').extract_first()
            old_price = response.css('p.old-price span.price::text').extract_first().strip()
            counter = 0
            for char in old_price:
                if char == '\\':
                    break
                counter += 1
            old_price = int(float(old_price[0:counter].replace(',', '.')) * 100)
            new_price = int(float(response.css('p.special-price span.price::attr(content)').extract_first()) * 100)
            return [curr, old_price, new_price]

    def get_image_urls(self, response):
        return response.css('a.thumb-link img::attr(src)').extract()

    def get_retailer_sku(self, response):
        return response.css('div.skuProducto > span::text').extract_first().split(' ')[1]

    def get_url(self, response):
        return response.request.url

    def get_description(self, response):
        description = response.css('div.descripcionProducto > div > p::text').extract_first().strip()
        return description.split('.')

    def get_categories(self, title, brand, gender):
        return [title.split(' ')[0], gender, brand]

    def get_sizes(self, response):
        return response.css('#configurable_swatch_talla a::attr(name)').extract()

    def get_availability(self, response):
        return response.css('div.extra-info span.value::text').extract_first() == 'En existencia'

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


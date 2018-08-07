import json
import time
import datetime

from ..items import ProductItem


class ProductParser:

    gender_map = {
        "homem": "men",
        "mulher": "women"
    }

    def parse(self, response):
        product = ProductItem()

        product['retailer_sku'] = self.product_id(response)
        product['lang'] = 'pt'
        product['uuid'] = None
        product['trail'] = response.meta.get('trail', [])
        product['gender'] = self.gender(response)
        product['category'] = self.category(response)
        product['industry'] = None
        product['brand'] = self.brand(response)
        product['url'] = response.url
        product['date'] = int(time.time())
        product['market'] = 'BR'
        product['retailer'] = 'levi-br'
        product['crawl_id'] = self.crawl_id()
        product['url_original'] = response.url
        product['name'] = self.product_name(response)
        product['description'] = self.description(response)
        product['care'] = self.care(response)
        product['image_urls'] = self.image_urls(response)
        if self.availability(response):
            product['skus'] = self.skus(response)
            product['price'] = self.price(response)
            product['currency'] = 'BRL'
        else:
            product['skus'] = []
            product['out_of_stock'] = True
        product['spider_name'] = 'levis-br-crawl'

        return product

    def raw_skus(self, response):
        sku_re = "skuJson_0\s=\s(.*});"
        sku_css = "head script:not([type]):not([language])"
        raw_sku = json.loads(response.css(sku_css).re_first(sku_re))
        return raw_sku

    def availability(self, response):
        return self.raw_skus(response)['available']

    def product_name(self, response):
        return response.css(".productName::text").extract_first()

    def product_id(self, response):
        return response.css(".product-user-review-product-id::attr('value')").extract_first()

    def skus(self, response):
        raw_skus = self.raw_skus(response)
        color = self.color(response)

        skus = dict()
        for sku in raw_skus['skus']:
            if sku['available']:
                sku_id = sku['sku']
                skus[sku_id] = {}
                skus[sku_id]['price'] = sku['bestPrice']
                skus[sku_id]['currency'] = 'BRL'
                if sku['listPrice']:
                    skus[sku_id]['previous_prices'] = [sku['listPrice']]
                skus[sku_id]['colour'] = color
                skus[sku_id]['size'] = sku['dimensions'].get('Tamanho', sku['dimensions'].get('TAMANHO'))

        return skus

    def color(self, response):
        return response.css(".value-field.Cor::text").extract_first()

    def price(self, response):
        price = response.css(".skuBestPrice").re_first("\d+,\d+")
        return int(price.replace(',', ''))

    def image_urls(self, response):
        return response.css(".thumbs a::attr('zoom')").extract()

    def care(self, response):
        return response.css('.Composicao.value-field::text').extract()

    def description(self, response):
        return response.css(".productDescription::text").extract()

    def crawl_id(self):
        date_now = datetime.datetime.now()
        epoch_time = int(time.time())
        return f"levi-br-{date_now:%Y%m%d}-{epoch_time}-omfp"

    def brand(self, response):
        return response.css("#brand a::text").extract_first()

    def category(self, response):
        return response.css(".bread-crumb a::text").extract()

    def gender(self, response):
        categories = self.category(response)
        categories = [category.lower() for category in categories]
        for gender in self.gender_map:
            if gender in categories:
                return self.gender_map[gender]
        return gender

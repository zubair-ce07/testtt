import json

from scrapy import Spider

from rebellious.items import RebelliousItem


class RebelliousParseSpider(Spider):
    name = 'rebellious_parse_spider'
    raw_product_xpath = '//script[contains(text(), "ec:addProduct")]/text()'
    BRAND = 'Rebellious'
    CURRENCY = 'USD'
    GENDER = 'women'

    def parse_product(self, response):
        product = RebelliousItem()
        product['url'] = response.url
        product['brand'] = self.BRAND
        product['gender'] = self.GENDER
        product['skus'] = self.product_sku(response)
        product['name'] = self.product_name(response)
        product['category'] = self.product_category(response)
        product['image_urls'] = self.product_image_urls(response)
        product['description'] = self.product_description(response)
        product['retailer_sku'] = self.product_retailer_sku(response)

        yield product

    def product_image_urls(self, response):
        css = '.more-views ::attr(href)'
        return response.css(css).extract()

    def product_description(self, response):
        css = '.short-description > p::text'
        return response.css(css).extract()

    def product_sku(self, response):
        raw_sku = self.raw_sku(response)
        skus = {}
        sku_currency_price = self.sku_currency_price(raw_sku)

        for size in raw_sku.get('attributes').get('967').get('options'):
            skus[size.get('label')] = sku = {'size': size.get('label')}
            sku.update(sku_currency_price)

        return skus

    def sku_currency_price(self, raw_sku):
        sku_currency_price = {
            'currency': self.CURRENCY,
            'price': raw_sku.get('basePrice'),
        }

        if raw_sku.get('oldPrice'):
            sku_currency_price['previous_price'] = raw_sku.get('oldPrice')

        return sku_currency_price

    def raw_sku(self, response):
        xpath = '//script[contains(text(), "Product.Config")]/text()'
        return json.loads(response.xpath(xpath).re_first('{.*}'))

    def product_name(self, response):
        css = '.product-name h1::text'
        return response.css(css).extract_first()

    def product_category(self, response):
        category_r = "'category': '(.*)'"
        return response.xpath(self.raw_product_xpath).re_first(category_r)

    def product_retailer_sku(self, response):
        id_r = "'id': '(.*)'"
        return response.xpath(self.raw_product_xpath).re_first(id_r)

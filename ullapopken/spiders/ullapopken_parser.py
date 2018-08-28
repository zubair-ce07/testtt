import json

from scrapy import Request, Selector

from ullapopken.items import Item


class UllapopkenParser:
    genders = [
        ('HERREN', 'Male'),
        ('DAMEN', 'Female')
    ]

    product_url_t = 'https://www.ullapopken.de/produkt/{}/'
    article_url_t = 'https://www.ullapopken.de/api/res/article/{}'
    image_url_t = 'https://up.scene7.com/is/image/UP/{}?fit=constrain,1&wid=1400&hei=2100'

    def parse_item(self, response):
        raw_item = json.loads(response.text)
        categories = response.meta.get('categories')
        variants = response.meta.get('variants')
        item = Item()

        item['retailer_sku'] = raw_item['code']
        item['name'] = raw_item['name']
        item['description'] = self.description(raw_item)
        item['care'] = self.care(raw_item)
        item['brand'] = 'Ullapopken'
        item['url'] = self.url(raw_item)
        item['categories'] = categories
        item['gender'] = self.gender(categories)
        item['image_urls'] = self.image_urls(raw_item)
        item['skus'] = self.skus(raw_item)
        item['requests'] = self.color_requests(variants)

        return self.next_request_or_item(item)

    def parse_color(self, response):
        raw_item = json.loads(response.text)
        item = response.meta.get('item')

        item['image_urls'] += self.image_urls(raw_item)
        item['skus'] += self.skus(raw_item)

        return self.next_request_or_item(item)

    def color_requests(self, variants):
        return [Request(url=self.article_url_t.format(variant), callback=self.parse_color)
                for variant in variants]

    def next_request_or_item(self, item):
        if not item['requests']:
            del item['requests']
            return item

        request = item['requests'].pop()
        request.meta['item'] = item

        return request

    def image_urls(self, raw_item):
        picture_codes = self.picture_codes(raw_item)
        return [self.image_url_t.format(picture_code) for picture_code in picture_codes]

    def picture_codes(self, raw_item):
        raw_pictures = raw_item['pictureMap']
        return [raw_pictures['code']] + raw_pictures['detailCodes']

    def skus(self, raw_item):
        sku_common = self.sku_common(raw_item)
        skus = []

        for raw_sku in raw_item['skuData']:
            sku = sku_common.copy()
            sku['size'] = self.size(raw_sku)

            if raw_sku['stockLevelStatus'] != 'AVAILABLE':
                sku['is_out_of_stock'] = True

            sku['sku_id'] = f'{sku["color"]}_{sku["size"]}'
            skus.append(sku)

        return skus

    def sku_common(self, raw_item):
        sku_common = {'color': raw_item['colorLocalized']}
        sku_common.update(self.pricing(raw_item))

        return sku_common

    def size(self, raw_sku):
        return f'{raw_sku["sizeCharacteristic"]["sizeTypeValue"]}/{raw_sku["displaySize"]}' \
            if raw_sku["sizeCharacteristic"] else raw_sku["displaySize"]

    def pricing(self, raw_item):
        pricing = dict()

        price = raw_item['reducedPrice'] or raw_item['originalPrice']
        pricing['currency'] = price['currencyIso']
        pricing['price'] = self.formatted_price(price['value'])
        pricing['previous_prices'] = [self.formatted_price(raw_item['crossedOutPrice']['value'])] \
            if raw_item['crossedOutPrice'] else []

        return pricing

    def formatted_price(self, price):
        return int(float(price) * 100)

    def description(self, raw_item):
        selector = Selector(text=list(raw_item['description'].values())[0])
        return selector.css('*::text').re_first('.*[\S].*').strip().split('. ')

    def care(self, raw_item):
        care = list(raw_item['careInstructions'].values())[0]
        return [c['description'] for c in care]

    def gender(self, categories):
        for gender_token, gender in self.genders:
            if gender_token in categories:
                return gender

    def url(self, raw_item):
        return self.product_url_t.format(raw_item['code'])

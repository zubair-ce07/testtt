import json

from scrapy import Request, Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import Item
from ..utilities import pricing, detect_gender, detect_merch_info


class Mixin:
    retailer = 'rakuten'
    cookie_url = 'https://www.rakuten.com/eCa432UiJrqnJsU3'

    allowed_domains = ['rakuten.com']
    start_urls = [
        'https://www.rakuten.com/shop/?scid=ebates-home-3&l-id=ebates-home-3'
    ]


class RakutenParseSpider(Mixin, Spider):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        raw_product = self.extract_raw_product(response)

        item = Item()
        item['retailer_sku'] = self.extract_retailer_sku(raw_product)
        item['name'] = self.extract_name(raw_product)
        item['brand'] = self.extract_brand(raw_product)
        item['care'] = self.extract_care(raw_product)
        item['category'] = self.extract_category(raw_product)
        item['description'] = self.extract_description(raw_product)
        item['skus'] = self.extract_skus(raw_product)
        item['image_urls'] = self.extract_image_urls(raw_product)
        item['gender'] = self.extract_gender(raw_product, item)
        item['merch_info'] = self.extract_merch_info(item)
        item['url'] = response.url

        return item

    def extract_raw_product(self, response):
        css = '[data-component-name="Product"]::text'
        return json.loads(response.css(css).extract_first())['main']['product']

    def extract_retailer_sku(self, raw_product):
        return raw_product['item']['baseSku']

    def extract_name(self, raw_product):
        return raw_product['item']['itemName']

    def extract_brand(self, raw_product):
        return raw_product['spec']['brand']

    def extract_care(self, raw_product):
        sel = self.extract_raw_description(raw_product)
        return ' '.join(c.strip() for c in sel.css('.b-features ::text').extract())

    def extract_category(self, raw_product):
        return [raw_product['item']['categoryName']]

    def extract_gender(self, raw_product, item):
        raw_gender = raw_product['item'].get('variants', {})
        gender = raw_gender.get('variantsViewLabels', {}).get('Age Gender')
        soup = item['care'] + item['description'] + item['name']

        return gender or detect_gender(soup)

    def extract_description(self, raw_product):
        sel = self.extract_raw_description(raw_product)
        return ' '.join(d.strip() for d in sel.css('.b-description ::text').extract())

    def extract_image_urls(self, raw_product):
        return [url['location'] for url in raw_product['item'].get('images') if url.get('location')]

    def extract_money_strings(self, raw_product):
        raw_price_map = raw_product.get('price') or raw_product
        price_keys = ['listPrice', 'price', 'originalPrice', 'itemListPrice',
                      'itemPrice', 'itemOriginalPrice']
        return [p for k in price_keys for p in raw_price_map.get(k, [])]

    def extract_currency(self, raw_product):
        raw_price = raw_product.get('price', {})
        return [raw_price.get('currencyCode')] or [raw_product['defaultPointMoney'][0]]

    def extract_merch_info(self, item):
        item_details = item['care'] + item['name'] + item['description']
        return detect_merch_info(item_details)

    def extract_skus(self, raw_product):
        skus = {}
        raw_skus = raw_product['item'].get('variants', {})
        raw_skus_details = raw_skus.get('variantsInfo', {})

        raw_variants = self.create_detail_maps(raw_skus)

        for sku_id, raw_sku in raw_skus_details.items() or [('One Size', raw_product['item'])]:
            sku = pricing(self.extract_money_strings(raw_sku) + self.extract_currency(raw_sku))

            if raw_sku.get('soldOut') or raw_sku.get('isSoldOut'):
                sku['out_of_stock'] = True

            raw_sku = raw_sku.get('value', [])
            sizes = []
            for index, attribute_value in enumerate(raw_sku):
                attribute, attribute_map = raw_variants[index]

                if 'color' in attribute.lower():
                    sku['colour'] = attribute_map.get(attribute_value)
                elif 'size' in attribute.lower() or 'width' in attribute.lower():
                    sizes.append(attribute_map.get(attribute_value))

            sku['size'] = '_'.join(sizes) if sizes else 'One Size'
            skus[sku_id] = sku

        return skus

    def extract_raw_description(self, raw_product):
        return Selector(text=raw_product['info']['description'])

    def create_detail_maps(self, raw_skus):
        raw_maps = raw_skus.get('variantsObjectWithKey')
        return [(name, self.reverse_dictionary(raw_map)) for name, raw_map in raw_maps.items()]

    def reverse_dictionary(self, dictionary={}):
        return {v: k for k, v in dictionary.items()}


class RakutenCrawlSpider(Mixin, CrawlSpider):
    name = Mixin.retailer + '-crawl'

    listings_css = ['.r-categories__list', '.r-pagination',
                    '.r-search-page__category-item']
    products_css = ['.r-product__main-block']
    products_deny = ['TRENDING', 'DEALS', 'redirect']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css,
                           deny=products_deny), callback='parse_product'),
    )

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) '
                      'Gecko/20100101 Firefox/63.0',
    }

    product_parser = RakutenParseSpider()

    def start_requests(self):
        return [Request(self.cookie_url, callback=self.parse_start_url)]

    def parse_start_url(self, response):
        callback = super().parse
        return [Request(url, callback=callback) for url in self.start_urls]

    def parse(self, response):
        if self.deny_category(response):
            return

        for request_or_item in super().parse(response):
            if isinstance(request_or_item, Request):
                request_or_item.meta['trail'] = self.make_trail(response)
            yield request_or_item

    def parse_product(self, response):
        return self.product_parser.parse(response)

    def deny_category(self, response):
        deny = ['electronics', 'home', 'outdoor', 'beauty', 'personal', 'care', 'health',
                'sports', 'fitness', 'toys', 'toddlers', 'baby', 'pet', 'supplies', 'media',
                'food', 'beverage', 'automotive', 'parts', 'everything', 'else', 'luggage']
        return any(category in response.url for category in deny)

    def make_trail(self, response):
        link_text = response.meta.get('link_text', '').strip()
        return response.meta.get('trail', []) + [(link_text, response.url)]

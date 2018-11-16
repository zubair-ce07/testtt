import json

from scrapy import Request, Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import Item
from ..utilities import pricing, map_currency_code


class RakutenParseSpider(Spider):
    name = 'rakuten-parse'
    cookie_url = 'https://www.rakuten.com/eCa432UiJrqnJsU3'

    def parse_cookie(self, response):
        return Request(response.meta['url'], callback=self.parse, dont_filter=True)

    def parse(self, response):
        if not self.check_valid_response(response):
            return Request(self.cookie_url, callback=self.parse_cookie,
                           meta={'url': response.url}, dont_filter=True)
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
        item['url'] = self.extract_url(response)
        
        item['gender'] = self.extract_gender(raw_product, item)

        if self.is_limited_item(item):
            item['merch_info'] = 'Limited'

        return item

    def check_valid_response(self, response):
        css = 'div#rat'
        return response.css(css).extract()

    def extract_raw_product(self, response):
        css = 'script[data-component-name="Product"]::text'
        return json.loads(response.css(css).extract_first())['main']['product']

    def extract_retailer_sku(self, raw_product):
        return raw_product['item']['baseSku']

    def extract_name(self, raw_product):
        return raw_product['item']['itemName']

    def extract_brand(self, raw_product):
        return raw_product['spec']['brand']

    def extract_care(self, raw_product):
        sel = Selector(text=raw_product['info']['description'])
        css = 'div.b-features *::text'
        return ' '.join(c.strip() for c in sel.css(css).extract())

    def extract_category(self, raw_product):
        return raw_product['item']['categoryName']

    def extract_gender(self, raw_product, item):
        gender = raw_product['item'].get('variants', {}).get(
            'variantsViewLabels', {}).get('Age Gender')
        if gender:
            return gender
        raw_strings = item['care'] + item['description'] + item['name']
        if 'women' in raw_strings:
            return 'Women'
        elif 'men' in raw_strings:
            return 'Men'
        elif any(['kids' in raw_strings, 'boy' in raw_strings, 'girl' in raw_strings]):
            return 'Kids'
        else:
            return 'One gender'

    def extract_description(self, raw_product):
        sel = Selector(text=raw_product['info']['description'])
        css = 'div.b-description *::text'
        return ' '.join(d.strip() for d in sel.css(css).extract())

    def extract_image_urls(self, raw_product):
        return [image.get('location') for image in raw_product['item'].get('images')]

    def extract_url(self, response):
        return response.url

    def extract_money_strings(self, raw_product):
        raw_price =  raw_product.get('price')
        if raw_price:
            return raw_price['listPrice'] + raw_price['price'] + raw_price['originalPrice']
        return raw_product['itemPrice'] + raw_product['itemListPrice'] + \
               raw_product['itemOriginalPrice']

    def extract_currency(self, raw_product):
        raw_price = raw_product.get('price', {})
        return raw_price.get('currencyCode', raw_product['defaultPointMoney'][0])

    def is_limited_item(self, item):
        raw_string = item.get('care').lower() + item['name'].lower() +\
                      item.get('description').lower()
        if 'limited' in raw_string:
            return True

    def extract_skus(self, raw_product):
        skus = {}
        raw_skus = raw_product['item'].get('variants', {})
        raw_skus_details = raw_skus.get('variantsInfo', {})

        for raw_sku in raw_skus_details.values() or [raw_product['item']]:
            sku = pricing(self.extract_money_strings(raw_sku))
            sku['currency'] = map_currency_code(self.extract_currency(raw_sku))

            if raw_sku.get('soldOut') or raw_sku.get('isSoldOut'):
                sku['out_of_stock'] = True

            sku.update(self.extract_colours_and_sizes(raw_skus, raw_sku.get('value')))
                
            sku_id = '_'.join(sc for sc in [sku.get("colour"), sku["size"]] if sc)
            skus[sku_id] = sku
        return skus

    def extract_colours_and_sizes(self, raw_skus, sku_specs):
        colour, sizes = '', []
        specs_details = raw_skus.get('variantsObjectWithKey',{})

        for spec, specs_detail in zip(sku_specs or [], specs_details.items()):
            spec_type = specs_detail[0]
            if 'color' in spec_type.lower():
                colour = self.get_key_from_value(specs_detail[1], spec)
            elif not 'gender' in spec_type.lower() and not 'outerwear' in spec_type.lower():
                sizes.append(self.get_key_from_value(specs_detail[1], spec))

        common_sku = {}
        if colour:
            common_sku['colour'] = colour
        common_sku['size'] = '_'.join(sizes) if sizes else 'One Size'
        
        return common_sku

    def get_key_from_value(self, dictionary, value):
        return list(dictionary.keys())[list(dictionary.values()).index(value)]


class RakutenCrawlSpider(CrawlSpider):
    name = 'rakuten-crawl'
    cookie_url = 'https://www.rakuten.com/eCa432UiJrqnJsU3'

    allowed_domains = ['rakuten.com']
    start_urls = ['https://www.rakuten.com/shop/?scid=ebates-home-3&l-id=ebates-home-3']

    listings_css = ['div.r-categories__list','nav.r-pagination'
                    'li.r-search-page__category-item.is-parent ul']
    products_css = ['div.r-product__main-block']
    products_deny = ['TRENDING', 'DEALS', 'redirect']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_category'),
        Rule(LinkExtractor(restrict_css=products_css,
                           deny=products_deny), callback='parse_product'),
    )

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) '
                      'Gecko/20100101 Firefox/63.0',
    }

    product_parser = RakutenParseSpider()

    def start_requests(self):
        return [Request(self.cookie_url, callback=self.parse)]

    def parse(self, response):
        return Request(self.start_urls[0], callback=super().parse)

    def parse_category(self, response):
        if self.verify_category(response):
            return

        for request_or_item in super().parse(response):
            if isinstance(request_or_item, Request):
                request_or_item.meta['trail'] = self.make_trail(response)
            yield request_or_item

    def parse_product(self, response):
        return self.product_parser.parse(response)

    def verify_category(self, response):
        deny = ['electronics', 'home', 'outdoor', 'beauty', 'personal', 'care', 'health',
            'sports', 'fitness', 'toys', 'toddlers', 'baby', 'pet', 'supplies', 'media',
            'food', 'beverage', 'automotive', 'parts', 'everything', 'else', 'luggage']
        return any(category in response.url for category in deny)

    def make_trail(self, response):
        link_text = response.meta.get('link_text', '').strip()
        return response.meta.get('trail', []) + [(link_text, response.url)]

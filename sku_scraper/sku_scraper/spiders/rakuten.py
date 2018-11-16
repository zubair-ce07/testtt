
import json
import itertools

from scrapy import Request, Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import Item
from ..utilities import pricing, map_currency_code, map_gender


class RakutenParseSpider(Spider):
    name = 'rakuten-parse'
    cookie_url = 'https://www.rakuten.com/eCa432UiJrqnJsU3'

    def parse_cookie(self, response):
        return Request(response.meta['url'], callback=self.parse, dont_filter=True)

    def parse(self, response):
        if not response.css('div#rat'):
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
        item['merch_info'] = self.extract_merch_info(item)
        item['gender'] = self.extract_gender(raw_product, item)
        item['url'] = response.url

        return item

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
        css = 'div.b-features ::text'
        return ' '.join(c.strip() for c in sel.css(css).extract())

    def extract_category(self, raw_product):
        return raw_product['item']['categoryName']

    def extract_gender(self, raw_product, item):
        gender = raw_product['item'].get('variants', {}).get(
            'variantsViewLabels', {}).get('Age Gender')
        if gender:
            return gender

        return map_gender(item['care'] + item['description'] + item['name'])

    def extract_description(self, raw_product):
        sel = Selector(text=raw_product['info']['description'])
        css = 'div.b-description ::text'
        return ' '.join(d.strip() for d in sel.css(css).extract())

    def extract_image_urls(self, raw_product):
        return [url['location'] for url in raw_product['item'].get('images') if url.get('location')]

    def extract_money_strings(self, raw_product):
        raw_price_map =  raw_product.get('price') or raw_product
        price_keys = ['listPrice', 'price', 'originalPrice', 'itemListPrice',
                      'itemPrice', 'itemOriginalPrice']
        return [p for k in price_keys for p in raw_price_map.get(k,[])]

    def extract_currency(self, raw_product):
        raw_price = raw_product.get('price', {})
        return raw_price.get('currencyCode') or raw_product['defaultPointMoney'][0]

    def extract_merch_info(self, item):
        item_details = item.get('care').lower() + item['name'].lower() + \
                       item.get('description').lower()
        if 'limited' in item_details:
            return 'Limited'
        return []

    def extract_skus(self, raw_product):
        skus = {}
        raw_skus = raw_product['item'].get('variants', {})
        raw_skus_details = raw_skus.get('variantsInfo', {})

        for raw_sku in raw_skus_details.values() or [raw_product['item']]:
            sku = pricing(self.extract_money_strings(raw_sku))
            sku['currency'] = map_currency_code(self.extract_currency(raw_sku))

            if raw_sku.get('soldOut') or raw_sku.get('isSoldOut'):
                sku['out_of_stock'] = True

            sku.update(self.extract_colours_and_sizes(raw_skus, raw_sku.get('value', [])))
                
            sku_id = '_'.join(sc for sc in [sku.get("colour"), sku["size"]] if sc)
            skus[sku_id] = sku
        return skus

    def extract_colours_and_sizes(self, raw_skus, sku_specs):
        colour, sizes = '', []
        specs_details = raw_skus.get('variantsObjectWithKey',{})

        for spec, specs_detail in zip(sku_specs, specs_details.items()):
            spec_type = specs_detail[0]
            specs_detail_reversed = self.reverse_dictionary(specs_detail[1])
            if 'color' in spec_type.lower():
                colour = specs_detail_reversed.get(spec)
            elif not 'gender' in spec_type.lower() and not 'outerwear' in spec_type.lower():
                sizes.append(specs_detail_reversed.get(spec))

        common_sku = {}
        if colour:
            common_sku['colour'] = colour
        common_sku['size'] = '_'.join(sizes) if sizes else 'One Size'
        
        return common_sku

    def reverse_dictionary(self, dictionary):
        reversed_dict = {}
        for item in dictionary.items():
            reversed_dict[item[1]] = item[0]
        return reversed_dict


class RakutenCrawlSpider(CrawlSpider):
    name = 'rakuten-crawl'
    cookie_url = 'https://www.rakuten.com/eCa432UiJrqnJsU3'

    allowed_domains = ['rakuten.com']
    start_urls = ['https://www.rakuten.com/shop/?scid=ebates-home-3&l-id=ebates-home-3']

    listings_css = ['.r-categories__list','.r-pagination',
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
        return Request(self.start_urls[0], callback=super().parse)

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

import re
import json
import itertools

from w3lib.url import url_query_cleaner
from scrapy import Request, Spider
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from task7_romans.items import Item


class RoamansParser(Spider):
    name = 'roamans_parser'
    brand_regex = re.compile(r"^(.+?®[^$])|by(.+)")
    prices_css = '.product-price ::text'

    size_families_url_t = 'https://f.monetate.net/trk/4/s/a-7736c7c2/p/allbrands.fullbeauty.com/887980575-0?' \
                          'mi=%272.1939917642.1534417043698%27&cs=!t&e=!(viewPage,gt,viewProduct)&pt=product&' \
                          'u=%27{}%27&eoq=!t'
    family_url_t = 'https://www.roamans.com/on/demandware.store/Sites-fbbrands-Site/default/Product-Variation?' \
                   'pid={}'
    sku_url_t = 'https://www.roamans.com/on/demandware.store/Sites-fbbrands-Site/default/Product-Variation?' \
                'pid={pid}&dwvar_{pid}_size={size_code}&dwvar_{pid}_braCupSize={size_code}&' \
                'dwvar_{pid}_shoeSize={size_code}&dwvar_{pid}_sizeFamily={variant_code}&' \
                'dwvar_{pid}_braBandSize={variant_code}&dwvar_{pid}_shoeWidth={variant_code}&' \
                'dwvar_{pid}_color={color_code}'

    care_terms = [
        'wash',
        'bleach',
        'temperature'
    ]
    currencies_map = (
        ('$', 'USD'),
    )

    def parse(self, response):
        item = Item()
        item['name'] = self.detect_item_name(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['url'] = response.url
        item['categories'] = self.extract_categories(response)
        item['description'] = self.detect_description(response)
        item['care'] = self.detect_care(response)
        item['brand'] = self.detect_brand(response)
        item['gender'] = 'women'
        item['skus'] = {}
        item['meta'] = {'requests': []}

        if self.has_size_family(response):
            item['meta']['requests'] = self.make_size_family_request(response)
        else:
            item['meta']['requests'] = self.make_sku_requests(response)

        return self.next_request_or_item(item)

    def parse_size_family(self, response):
        item = response.meta['item']
        item['meta']['requests'] += self.make_variant_requests(response)
        return self.next_request_or_item(item)

    def parse_variants(self, response):
        item = response.meta['item']
        item['meta']['requests'] += self.make_sku_requests(response)
        return self.next_request_or_item(item)

    def parse_sku(self, response):
        item = response.meta['item']
        item['skus'].update(self.extract_sku(response))
        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        if not item['meta']['requests']:
            del item['meta']
            return item

        request = item['meta']['requests'].pop()
        request.meta['item'] = item
        return request

    def make_size_family_request(self, response):
        return [Request(url=self.size_families_url_t.format(response.url), callback=self.parse_size_family)]

    def make_variant_requests(self, response):
        item = response.meta.get('item')

        size_families = re.findall(r"data-swatchvalue=\\\"(.+?)\\\"", response.text)

        urls = [self.family_url_t.format(f'{item["retailer_sku"]}-{s}') if s != 'R'
                else self.family_url_t.format(f'{item["retailer_sku"]}')
                for s in size_families]
        return [Request(url=url, callback=self.parse_variants) for url in urls]

    def make_sku_requests(self, response):
        variant_css = '.attribute.sizeFamily li::attr(data-swatchvalue), ' \
                      '.attribute.braBandSize li::attr(data-swatchvalue), ' \
                      '.attribute.shoeWidth li::attr(data-swatchvalue)'
        variant_codes = response.css(variant_css).extract() or ['']

        size_css = '.attribute.size li::attr(data-swatchvalue), ' \
                   '.attribute.braCupSize li::attr(data-swatchvalue), ' \
                   '.attribute.shoeSize li::attr(data-swatchvalue)'
        size_codes = response.css(size_css).extract()

        color_css = '.attribute.color li::attr(data-swatchvalue)'
        color_codes = response.css(color_css).extract()

        product_id = self.extract_product_id(response.url)

        skus_requests = []
        for variant_code, size_code, color_code in itertools.product(variant_codes, size_codes, color_codes):
            url = self.sku_url_t.format(pid=product_id, size_code=size_code, variant_code=variant_code,
                                        color_code=color_code)
            skus_requests.append(Request(url=url, callback=self.parse_sku))
        return skus_requests

    def extract_raw_name(self, response):
        name_css = '.top-wrap .product-name::text'
        return response.css(name_css).extract_first()

    def detect_item_name(self, response):
        raw_name = self.extract_raw_name(response)
        return self.brand_regex.sub('', raw_name).strip()

    def detect_brand(self, response):
        name = self.extract_raw_name(response)

        brand = self.brand_regex.findall(name, re.IGNORECASE)
        brand = brand[-1] if brand else ['Roamans']
        return [b for b in brand if b][0]

    def extract_retailer_sku(self, response):
        return re.findall('/(\d+)', response.url)[0]

    def extract_product_id(self, url):
        return re.findall('(\d+(-[PTR])?)', url)[0][0]

    def extract_image_urls(self, response):
        css = '[name="product_detail_image"] img::attr(data-lgimg)'
        return [url_query_cleaner(json.loads(img)['url']) for img in response.css(css).extract()]

    def extract_categories(self, response):
        css = '.breadcrumb-element::text'
        return response.css(css).extract()[1:-2]

    def extract_raw_description(self, response):
        description_xpath = '//div[@class="product-details-description"]/descendant::text()' \
                            '[not(ancestor::div/@class="details-mainframeid")]'
        raw_description = sum([rd.split('.') for rd in response.xpath(description_xpath).extract()], [])
        return [rd.strip() for rd in raw_description if rd.strip()]

    def detect_description(self, response):
        return [rd for rd in self.extract_raw_description(response) if not any(c in rd for c in self.care_terms)]

    def detect_care(self, response):
        return [rd for rd in self.extract_raw_description(response) if any(c in rd for c in self.care_terms)]

    def has_size_family(self, response):
        return response.css('.attribute.sizeFamily').extract()

    def extract_color(self, response):
        css = '.attribute.color .selected-value::text'
        return response.css(css).extract_first().strip()

    def extract_size(self, response):
        sizes_css = '.attribute:not(.color) .selected-value::text'
        return '/'.join([s.strip() for s in response.css(sizes_css).extract()])

    def is_out_of_stock(self, response):
        return response.css('.color .unselectable.selected').extract()

    def convert_price(self, price):
        price = price.replace(',', '.')
        return int(float(price) * 100)

    def detect_currency(self, response):
        price_str = ' '.join(response.css(self.prices_css).extract())
        for currency_str, currency in self.currencies_map:
            if currency_str in price_str:
                return currency

    def extract_pricing(self, response):
        prices_regex = '[\d,.]+'
        prices = sorted([self.convert_price(p) for p in response.css(self.prices_css).re(prices_regex)])

        pricing = {
            'currency': self.detect_currency(response),
            'price': prices[0],
            'previous_prices': prices[1:]
        }

        return pricing

    def extract_sku(self, response):
        sku = self.extract_pricing(response)
        sku['color'] = self.extract_color(response)
        sku['size'] = self.extract_size(response)

        if self.is_out_of_stock(response):
            sku['is_out_of_stock'] = True

        return {f'{sku["color"]}_{sku["size"]}': sku}


class RoamansCrawler(CrawlSpider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }
    name = 'roamans'

    start_urls = ['https://www.roamans.com/']
    allowed_domains = [
        'roamans.com',
        'monetate.net'
    ]

    navigation_pagination_css = '.menu-category > li, .page-next'
    product_css = '.name-link'
    rules = (
        Rule(LinkExtractor(restrict_css=navigation_pagination_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    item_parser = RoamansParser()

    def parse_item(self, response):
        return self.item_parser.parse(response)

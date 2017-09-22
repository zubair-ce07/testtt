import json

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, remove_jsession


class Mixin:
    retailer = 'sportinglife-ca'
    lang = 'ca'
    market = 'CA'
    allowed_domains = [
        'sportinglife.ca'
    ]

    start_urls_with_meta = [
        ('https://www.sportinglife.ca/c/home', {'gender': None, 'industry': 'homeware'}),
        ('https://www.sportinglife.ca/c/junior-girls-atheltic', {'gender': 'girls'}),
        ('https://www.sportinglife.ca/c/boys', {'gender': 'boys'}),
        ('https://www.sportinglife.ca/c/ladies', {'gender': 'women'}),
        ('https://www.sportinglife.ca/c/mens', {'gender': 'men'}),
        ('https://www.sportinglife.ca/c/footwear', {})
    ]


class SportingLifeParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '#priceDisplay span::text'

    sku_url_t = 'https://www.sportinglife.ca/json/sizePickerReloadResponse.jsp' \
                '?productId={product_id}&colour={color}'
    image_url_t = 'https://www.sportinglife.ca/include/productDetailImage.jsp' \
                  '?prdId={product_id}&colour={color}'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(garment, response)
        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {
            'requests_queue': self.sku_color_size_requests(response) + self.image_urls_requests(response),
        }

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return response.url.split('/')[-2]

    def product_name(self, response):
        return clean(response.css('.product-detail-container h2::text'))[0]

    def product_brand(self, response):
        return clean(response.css('.product-detail-container strong::text'))[0] or 'SportingLife'

    def product_category(self, response):
        raw_category = clean(response.css('.breadcrumb li ::text')) or []
        return clean(raw_category[1:-1])

    def product_color(self, response):
        return clean(response.css('.swatches img::attr(title)')) or ['']

    def image_urls_requests(self, response):
        product_id = self.product_id(response)
        colors = self.product_color(response)
        return [Request(url=self.image_url_t.format(product_id=product_id, color=color), callback=self.parse_image_url)
                for color in colors]

    def parse_image_url(self, response):
        css = 'svg::attr(href)'
        garment = response.meta['garment']
        garment['image_urls'] += [response.urljoin(url) for url in clean(response.css(css))]

        return self.next_request_or_garment(garment)

    def sku_color_size_requests(self, response):
        product_id = self.product_id(response)
        sku_urls = []
        for color in self.product_color(response):
            sku_urls.append(Request(url=self.sku_url_t.format(product_id=product_id, color=color),
                                    callback=self.parse_skus,
                                    meta={'pricing': self.product_pricing_common_new(response),
                                          'color': color
                                          }))
        return sku_urls

    def parse_skus(self, response):
        _skus = {}
        raw_sku = json.loads(response.text)
        for size in raw_sku.get('sizes', [{'size': self.one_size}]):
            sku_id = '{color}_{size}'.format(color=response.meta['color'], size=size['size']).lower()
            sku = {
                'sku_id': sku_id,
                'size': size['size'],
            }
            if response.meta['color']:
                sku['color'] = response.meta['color']
            if not (size.get('enabled') or raw_sku.get('singleSku', {'enabled': False})['enabled']):
                sku['out_of_stock'] = True
            sku.update(response.meta['pricing'])
            _skus[sku_id] = sku
        garment = response.meta['garment']
        garment['skus'].update(_skus)

        return self.next_request_or_garment(garment)

    def raw_description(self, response):
        css = '#tabs-details ::text'
        return clean(response.css(css))

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def product_gender(self, garment, response):
        if response.meta.get('industry') == 'homeware':
            return

        if response.meta.get('gender'):
            return response.meta['gender']

        soup = [garment['name']] + garment['category'] + [garment['url']]
        soup = ' '.join(soup).lower()

        for gender_str, gender in self.GENDER_MAP:
            if gender_str in soup:
                return gender

        return 'unisex-adults'


class SportingLifeCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SportingLifeParseSpider()

    listing_xpath = '//*[@class="menu-dropdown list-inline"]' \
                    '//*[contains(text(), "Women") or ' \
                    'contains(text(), "Men") or ' \
                    'contains(text(), "Girls") or ' \
                    'contains(text(), "Boys")]/parent::*'

    listing_css = [
        '.row .parent .small-padding',
        '.pagination',
    ]
    products_css = '.product-card .image-container'

    deny_regex = ['/equipment/?',
                  '/equipment-cylce/?',
                  '/home-accesories-toys/?',
                  ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css,
                           restrict_xpaths=listing_xpath,
                           deny=deny_regex,
                           process_value=remove_jsession),
             callback='parse', ),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item', )
    )

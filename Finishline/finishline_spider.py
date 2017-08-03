import re
from w3lib.url import add_or_replace_parameter as add_parameter

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'finishline-us'
    allowed_domains = ['finishline.com']
    market = 'US'
    start_urls = [
        'http://www.finishline.com',
    ]


class FinishLineParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    image_api_url = 'http://www.finishline.com/store/browse/gadgets/alternateimage.jsp'
    price_css = 'span::text'

    brand_re = re.compile(r'FL.setup.brand = "(.*?)";')

    gender_map = [
        ('women', 'women'),
        ('men', 'men'),
        ('girl', 'girls'),
        ('boy', 'boys'),
        ('kid', 'unisex-kids'),
    ]
    request_headers = {
        'X-Requested-With': 'XMLHttpRequest'
    }

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['skus'] = self.skus(response)

        garment['image_urls'] = self.image_urls(response)
        garment['merch_info'] = self.merch_info(response)
        garment['gender'] = self.product_gender(garment)
        garment['meta'] = {'requests_queue': self.image_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = 'a[data-productid]::attr(data-productid)'
        return clean(response.css(css))[0].split('-')[0]

    def product_name(self, response):
        return clean(response.css('#title::text'))[0]

    def product_brand(self, response):
        brand_xpath = '//script[contains(text(), "FL.setup.brand")]'
        return clean(response.xpath(brand_xpath).re_first(self.brand_re))

    def merch_info(self, response):
        css = '.specialMessaging::text'
        raw_merch_info = sum((mi.split(',') for mi in clean(response.css(css))), [])
        return list(set([mi for mi in raw_merch_info if 'shipping' not in mi.lower()]))

    def raw_description(self, response):
        css = '#productDescription ::text'
        return sum((clean(x.split('.')) for x in clean(response.css(css))[1:]), [])

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def product_category(self, response):
        return clean(response.css('.breadcrumbs [itemprop="name"]::text'))[1:]

    def product_gender(self, garment):
        soup = ' '.join(garment['category']).lower()

        for gender_str, gender in self.gender_map:
            if gender_str in soup:
                return gender

        return 'unisex-adults'

    def product_colors(self, response):
        result = []

        for item in response.css('#productStyleColor div.stylecolor'):
            result.append({
                'id': clean(item.css('.styleColorIds::text')[0]),
                'color': clean(item.css('.description::text')[0])
            })

        return result

    def colour_pricing(self, response, colour_id):
        css = '#prices_{}'.format(colour_id.replace(' ', '-'))
        pricing_sel = response.css(css)

        return self.product_pricing_common_new(pricing_sel)

    def skus(self, response):
        colors = self.product_colors(response)
        skus = {}

        for color in colors:
            common = self.colour_pricing(response, color['id'])
            css = '#sizes_{} .size'.format(color['id'].replace(' ', '-'))

            for raw_size in response.css(css):
                sku = common.copy()

                sku['size'] = self.one_size if raw_size.css('.NONE') else clean(raw_size.css('::text'))[0]
                sku_id = self.sku_id(color['id'], sku['size'])

                if raw_size.css('.unavailable'):
                    sku['out_of_stock'] = True

                sku['color'] = color['color']
                skus[sku_id] = sku

        return skus

    def sku_id(self, color_id, size):
        return '{0}_{1}'.format(color_id.split()[-1], size)

    def image_urls(self, response):
        image_urls = []
        css = '#alt::attr(data-large)'

        for image_url in clean(response.css(css)):
            image_urls.append(image_url.replace(' ', ''))

        return image_urls

    def colorids_and_styleids(self, response):
        results = []

        for color in response.css('a[data-productid]')[1:]:
            results.append((
                clean(color.css('::attr(data-productid)'))[0],
                clean(color.css('::attr(data-styleid)'))[0]
            ))

        return results

    def product_url_name(self, response):
        css = '.bVProductName::attr(value)'
        return clean(response.css(css))[0]

    def product_item_id(self, response):
        css = '[data-productitemId]::attr(data-productitemid)'
        return clean(response.css(css))[0]

    def product_is_shoe(self, response):
        css = '[data-productisshoe]::attr(data-productisshoe)'
        return clean(response.css(css))[0]

    def product_is_accessory(self, response):
        css = '[data-productisaccessory]::attr(data-productisaccessory)'
        return clean(response.css(css))[0]

    def image_requests(self, response):
        requests = []

        raw_url = add_parameter(self.image_api_url, 'productName', self.product_url_name(response))
        raw_url = add_parameter(raw_url, 'productIsAccessory', self.product_is_accessory(response))
        raw_url = add_parameter(raw_url, 'productIsShoe', self.product_is_shoe(response))
        raw_url = add_parameter(raw_url, 'productItemId', self.product_item_id(response))

        for color_id, style_id in self.colorids_and_styleids(response):
            url = add_parameter(raw_url, 'colorID', color_id)
            url = add_parameter(url, 'styleID', style_id)

            requests += [Request(url, callback=self.parse_images, headers=self.request_headers)]

        return requests


class FinishLineCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = FinishLineParseSpider()
    custom_settings = {
        'DOWNLOAD_DELAY': 1.25
    }

    products_css = '.product-container'
    listing_css = [
        '.Men-menu-dropdown',
        '.Women-menu-dropdown',
        '.Kids-menu-dropdown',
        '.paginationDiv'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

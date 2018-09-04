import json
import re

from scrapy.http import Request
from scrapy.spiders import Rule

from .base import (BaseCrawlSpider, BaseParseSpider, Gender, LinkExtractor,
                   clean)


class Mixin:
    retailer = 'cubus'
    allowed_domains = ['cubus.com']
    start_urls = ['https://cubus.com/']


class MixinSE(Mixin):
    retailer = Mixin.retailer + '-se'
    market = 'SE'
    start_urls = ['https://cubus.com/sv/']


class CubusParseSpider(BaseParseSpider, Mixin):

    def parse(self, response):
        raw_product = self.raw_product(response)

        product_id = raw_product['Code']
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = raw_product['Name']
        garment['category'] = raw_product['CategoryStructure']
        garment['brand'] = raw_product['ProductBrand']
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)

        garment['gender'] = self.product_gender(raw_product)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['merch_info'] = self.merch_info(raw_product)
        garment['skus'] = self.skus(raw_product)

        return garment

    def product_description(self, raw_product):
        raw_description = raw_product.get('CustomSiteSpecificFields', []) or []
        raw_description += [raw_product.get('ShortDescription', '') or '']

        raw_description = sum([rd.split('. ') for rd in raw_description], [])

        return [rd for rd in clean(raw_description) if not self.care_criteria(rd)]

    def product_care(self, raw_product):
        care = [c['Name'] for c in raw_product.get('ProductCare', [])]
        return care + clean((raw_product.get('Composition', '') or '').split(','))

    def product_gender(self, raw_product):
        soup = raw_product['CategoryStructure'] + [raw_product['ProductDepartment']]
        return self.gender_lookup(' '.join(soup)) or Gender.ADULTS.value

    def image_urls(self, raw_product):
        return [i['Url'] for i in raw_product['ProductImages']]

    def merch_info(self, raw_product):
        return raw_product['DiscountMessages'] + raw_product['PartOfCampaigns']

    def product_pricing_common(self, raw_product):
        money_strs = [
            raw_product['OfferedPrice']['Price'],
            raw_product['ListPrice']['Price'],
            raw_product['OfferedPrice']['Currency'],
        ]
        return super().product_pricing_common(None, money_strs=money_strs)

    def skus(self, raw_product):
        common = self.product_pricing_common(raw_product)
        common['colour'] = raw_product['VariantColor']['Label']

        skus = {}
        for raw_sku in raw_product['Skus']:
            sku = common.copy()
            sku['size'] = raw_sku['Size']

            if raw_sku['Quantity'] == 0:
                sku['out_of_stock'] = True

            skus[raw_sku['Id']] = sku

        return skus

    def raw_product(self, response):
        raw_product_re = 'Components.VariantPage,\s*({.+})\),'
        xpath = '//script[contains(., "Components.VariantPage")]'
        raw_product = response.xpath(xpath).re_first(raw_product_re)

        return json.loads(raw_product)['product']


class CubusCrawlSpider(BaseCrawlSpider, Mixin):
    custom_settings = {'DOWNLOAD_DELAY': 0.5}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    raw_paging_re = re.compile('Components.ProductListPage,\s*({.+})\),')
    pagination_url = 'https://cubus.com/sv/api/product/Post'
    listing_css = ['.site-nav__dropdown-wr']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css),
             callback='parse_pagination'),
    )

    def parse_pagination(self, response):
        xpath = '//script[contains(., "Components.ProductListPage")]'
        raw_paging = response.xpath(xpath).re_first(self.raw_paging_re)

        if not raw_paging:
            return

        raw_paging = json.loads(raw_paging)
        meta = {'trail': self.add_trail(response)}

        total_items = raw_paging['totalCount']
        pages = int(total_items/raw_paging['initData']['ItemsPerPage']) + 1

        for page in range(0, pages):
            formdata = raw_paging['initData']
            formdata['Page'] = page

            yield Request(self.pagination_url, body=json.dumps(formdata), method='POST',
                          headers=self.headers, meta=meta.copy(), callback=self.parse_listing)

    def parse_listing(self, response):
        raw_listing = json.loads(response.text)
        meta = {'trail': self.add_trail(response)}

        for product in raw_listing['Products']:
            for color in product['Siblings']:
                url = response.urljoin(color['Url'])

                yield Request(url, self.parse_item, meta=meta.copy())


class CubusSEParseSpider(CubusParseSpider, MixinSE):
    name = MixinSE.retailer + '-parse'


class CubusSECrawlSpider(CubusCrawlSpider, MixinSE):
    name = MixinSE.retailer + '-crawl'
    parse_spider = CubusSEParseSpider()

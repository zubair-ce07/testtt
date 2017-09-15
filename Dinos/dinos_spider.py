import re
from itertools import product
from copy import deepcopy

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'dinos-jp'
    lang = 'ja'
    market = 'JP'
    allowed_domains = ['dinos.co.jp']
    start_urls = [
        'https://www.dinos.co.jp/c2/002003/',
        'https://www.dinos.co.jp/c2/002009/',
        'https://www.dinos.co.jp/c4/002010025005/1a2/',
        'https://www.dinos.co.jp/c4/002010025009/1a2/',
        'https://www.dinos.co.jp/c4/002010025010/1a2/',
        'https://www.dinos.co.jp/c4/002010025011/1a2/',
        'https://www.dinos.co.jp/c4/002010025018/1a2/',
        'https://www.dinos.co.jp/c3/002003005/1a1/',
        'https://www.dinos.co.jp/c3/002009016/1a1/',
        'https://www.dinos.co.jp/c4/002010025005/1a2/',
        'https://www.dinos.co.jp/c4/002010025009/1a2/',
        'https://www.dinos.co.jp/c4/002010025010/1a2/',
        'https://www.dinos.co.jp/c4/002010025011/1a2/',
        'https://www.dinos.co.jp/c4/002010025018/1a2/',
        'https://www.dinos.co.jp/p/1367100493/?id=002010025009___1513545',
        'https://www.dinos.co.jp/p/1367100492/?id=002010025009___1513544'
    ]


class DinosParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    gender_map = [
        ('ガールズ', 'girls'),
        ('ボーイズ', 'boys'),
        ('メンズ', 'men'),
    ]

    brand_re = re.compile('(.*)/')
    image_re = re.compile('(.*)www')

    price_css = '.pMedium::text'
    previous_price_re = re.compile('(¥.*)')

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['gender'] = self.product_gender(response)

        return garment

    def product_gender(self, response):
        gender = self.gender_from_name_and_category(response) or self.gender_from_trail(response)

        return gender or 'unisex-adults'

    def gender_from_name_and_category(self, response):
        raw_name = self.raw_name(response) + ' '.join(self.product_category(response))
        for gender_key, gender in self.gender_map:
            if gender_key in raw_name:
                return gender
        return None

    def gender_from_trail(self, response):
        for t, url in response.meta.get('trail', [('', response.url)]):
            gender = self.gender_from_url(url)
            if gender:
                return gender
        return None

    def gender_from_url(self, url):
        genders = {
            'men': ['002003005', '002009016'],
            'unisex-kids': ['002010025005',
                            '002010025009',
                            '002010025010',
                            '002010025011',
                            '002010025018']
        }
        for gender, ids in genders.items():
            for gender_id in ids:
                if gender_id in url:
                    return gender
        return None

    def image_urls(self, response):
        return [x.replace(self.image_re.search(x).group(1) if self.image_re.search(x) else '', '')
                for x in clean(response.css('#dpvThumb li::attr(data-dpv-main-url)'))]

    def previous_price(self, response):
        css = '.priceB::text'
        selector = response.css(css)

        return [self.previous_price_re.search(clean(selector)[0]).group(1)] if selector else None

    def raw_skus(self, response):
        colours_in_stock = self.colours_in_stock(response)
        sizes_in_stock = self.sizes_in_stock(response)
        raw_skus = self.raw_skus_from_attributes(colours_in_stock, sizes_in_stock)

        colours_out_of_stock = self.colours_out_of_stock(response)
        sizes_out_of_stock = self.sizes_out_of_stock(response)
        raw_skus.update(self.raw_skus_out_of_stock(colours_out_of_stock or colours_in_stock, sizes_out_of_stock))

        return raw_skus

    def skus(self, response):
        raw_skus = self.raw_skus(response)
        skus = {}
        previous_price = self.previous_price(response)
        pricing = self.product_pricing_common_new(response, money_strs=previous_price)

        for key, raw_sku in raw_skus.items():
            sku = deepcopy(pricing)
            sku.update(raw_sku)
            skus[key] = sku

        return skus

    def raw_skus_from_attributes(self, colour, sizes):
        raw_skus = {}
        if not colour or not sizes:
            key = 'colour' if colour else 'size'
            for element in colour or sizes:
                raw_skus[element] = {key: element}
                raw_skus[element]['size'] = element if sizes else self.one_size

            return raw_skus

        for colour, size in list(product(colour, sizes)):
            raw_skus[colour+'__'+size] = {'colour': colour, 'size': size}

        return raw_skus

    def raw_skus_out_of_stock(self, colour, sizes):
        if not sizes:
            return {}
        raw_skus = self.raw_skus_from_attributes(colour, sizes)
        for key, raw_sku in raw_skus.items():
            raw_sku.update({'out_of_stock': True})
        return raw_skus

    def colours_in_stock(self, response):
        return clean(response.css('.dctSelectBox.color li:not(.soldOut)::attr(title)'))

    def sizes_in_stock(self, response):
        return clean(response.css('.dctSelectBox.size li:not(.soldOut) .wrap ::text'))

    def colours_out_of_stock(self, response):
        return clean(response.css('.dctSelectBox.color li.soldOut::attr(title)'))

    def sizes_out_of_stock(self, response):
        return clean(response.css('.dctSelectBox.size li.soldOut .wrap ::text'))

    def product_id(self, response):
        return clean(response.css('#vs-product-id::attr(value)'))[0]

    def raw_name(self, response):
        return clean(response.css('[itemprop="name"] ::text'))[0]

    def product_category(self, response):
        return clean(response.css('[itemprop="category"] [itemprop="title"]::text'))[1:]

    def product_brand(self, response):
        brand = self.brand_re.search(self.raw_name(response))

        return brand.group(1) if brand else ''

    def product_name(self, response):
        return self.raw_name(response).replace(self.product_brand(response)+'/', '')

    def raw_description(self, response):
        return clean(response.xpath('//*[contains(@id, "itemtable")]/tbody/tr[1]/td/text()'))

    def product_description(self, response):
        css = '.itemD_itemGuide ::text, [itemprop="description"] ::text'
        description = clean(response.css(css))

        return description + [x for x in self.raw_description(response) if not self.care_criteria_simplified(x)]

    def product_care(self, response):
        care = clean(response.css('.itemD_featureBox ::text'))

        return care + [x for x in self.raw_description(response) if self.care_criteria_simplified(x)]


class DinosCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = DinosParseSpider()

    pagination_xpath = '(//*[@class="btn next"])[1]'

    product_css = '.picPreview a'

    rules = (
        Rule(LinkExtractor(restrict_xpaths=pagination_xpath), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css),
             callback='parse_item'),
    )

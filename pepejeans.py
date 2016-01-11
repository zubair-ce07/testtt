# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider, clean, tokenize
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
import re
import json


class Mixin(object):
    retailer = 'pepejeans'
    allowed_domains = ['www.pepejeans.com', 'intl.pepejeans.com']
    pfx = 'http://www.pepejeans.com/'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    lang = 'en'
    start_urls = [Mixin.pfx + 'en_gb/']
    gender_map = (
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('women', 'women'),
        ('men', 'men'),
        ('kid', 'unisex-kids'),
    )


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    lang = 'de'
    start_urls = [Mixin.pfx + 'de_de/']
    gender_map = (
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('madchen', 'girls'),
        ('junge', 'boys'),
        ('frau', 'women'),
        ('damen', 'women'),
        ('mann', 'men'),
        ('herren', 'men'),
        ('kid', 'unisex-kids'),
    )


class PepeJeansParseSpider(Mixin, BaseParseSpider):
    take_first = TakeFirst()
    price_x = "//div[@class='price-info']//span[@class='price']//text()"

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        pid = self.product_id(hxs)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, hxs, response)

        garment['category'] = self.product_category(response.url)
        garment['gender'] = self.product_gender(garment['category'])
        garment['brand'] = self.product_brand(garment['category'])
        garment['skus'], media_urls = self.skus(hxs)
        garment['image_urls'], requests = self.image_urls(hxs, media_urls)
        garment['meta'] = {'requests_queue': requests}

        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        hxs = HtmlXPathSelector(response)

        garment = response.meta['garment']
        garment['image_urls'] += [self.take_first(clean(hxs.select('//img/@data-zoom-image')))]

        return self.next_request_or_garment(garment)

    def skus(self, hxs):
        seen_colors, media_urls, denim_length, skus = [], [], [], {}

        mapping_info = self.take_first(clean(hxs.select("//script[contains(text(), 'new Product.Config(')]//text()")))
        mapping_info = json.loads(re.findall('Product.Config\(({.*})', mapping_info)[0])
        skus_info = self.skus_data(hxs)

        colors = mapping_info['attributes']['92']['options']
        sizes = mapping_info['attributes']['173']['options']
        denim_lengths = mapping_info.get('attributes').get('212', {}).get('options', [])

        previous_price, price, currency = self.product_pricing(hxs)

        for key, sku_item in skus_info.iteritems():
            ids = key.split(',')

            if len(ids) == 3:
                color_id, size_id, denim_id = key.split(',')
            elif len(ids) == 2:
                color_id, size_id = key.split(',')
                denim_id = None
            else:
                continue

            try:
                color = [x['label'] for x in colors if x['id'] == color_id][0]
                size = [x['label'] for x in sizes if x['id'] == size_id][0]
                if denim_id:
                    denim_length = [x['label'] for x in denim_lengths if x['id'] == denim_id][0]
            except IndexError:
                continue

            size = self.one_size if size in ['One size fits all', '0'] else size
            sku = {
                'price': price,
                'currency': currency,
                'size': size,
                'colour': color,
                'out_of_stock': sku_item['not_is_in_stock'],
            }

            if previous_price:
                sku['previous_prices'] = [previous_price]

            sku_key = color + '_' + size + '_' + denim_length if denim_length else color + '_' + size
            skus[sku_key] = sku
            if color not in seen_colors:
                seen_colors += [color]
                media_urls += [sku_item.get('media_url', '')]

        return skus, clean(media_urls)

    def skus_data(self, hxs):
        stock_info = self.take_first(clean(hxs.select("//script[contains(text(), 'AmConfigurableData(')]//text()")))
        return json.loads(re.findall('AmConfigurableData\(({.*})', stock_info)[0])

    def image_urls(self, hxs, media_urls):
        images_data = clean(hxs.select("//script[contains(text(),'imageZoom')]"))[1:]
        images_url = clean([re.findall("imageZoom = '(.*?)';", x)[0] for x in images_data])
        return list(reversed(images_url)), [Request(url=x, callback=self.parse_images) for x in media_urls]

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("//p[@class='ref']//text()").re('SKU: (.*)')))

    def product_category(self, url):
        return urlparse(url).path.split('/')[2:-1] if isinstance(url, str) else None

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//div[@class='product-name']//text()")))

    def product_brand(self, category):
        return 'IRBR' if isinstance(category, list) and 'red-bull-racing-collection' in category else 'PepeJeans'

    def product_care(self, hxs):
        return clean(hxs.select("//div[@id='care-layer-materials']//text() | //div[@id='care-layer-care']//text()"))

    def product_description(self, hxs):
        return clean(hxs.select("//div[@class='description']//text()"))

    def product_gender(self, category):
        for x, y in self.gender_map:
            if x in tokenize(category):
                return y
        return 'unisex-kids'


class PepeJeansCrawlSpider(Mixin, BaseCrawlSpider):
    deny_r = ['campaigns']
    pagination_x = "//div[contains(@id,'am-pager-count')]//text()"
    listings_x = [
        "//li[contains(@class,'level0')]",
    ]
    products_x = [
        "//li[@class='item last']",
    ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x, deny=deny_r),
             callback='parse_pages'),

        Rule(SgmlLinkExtractor(restrict_xpaths=products_x), callback='parse_item')
    )

    def parse_pages(self, response):
        hxs = HtmlXPathSelector(response)
        total_pages = clean(hxs.select(self.pagination_x))
        url_t = response.url + '?is_ajax=1&p=%s&is_scroll=1'
        if total_pages:
            for page_no in range(int(total_pages[0]) + 1):
                url = url_t % str(page_no)
                yield Request(url, callback=self.parse, meta={'trail': self.add_trail(response)})

    def add_trail(self, response):
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        return response.meta.get('trail', []) + trail_part


class PepeJeansUKParseSpider(PepeJeansParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class PepeJeansUKCrawlSpider(PepeJeansCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = PepeJeansUKParseSpider()


class PepeJeansDEParseSpider(PepeJeansParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class PepeJeansDECrawlSpider(PepeJeansCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = PepeJeansDEParseSpider()
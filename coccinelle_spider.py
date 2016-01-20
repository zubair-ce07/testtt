# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider, clean
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
import re
import json


class Mixin(object):
    retailer = 'coccinelle'
    allowed_domains = ['www.coccinelle.com']
    pfx = 'http://www.coccinelle.com/'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = [Mixin.pfx + 'gb_en/']


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    lang = 'de'
    start_urls = [Mixin.pfx + 'de_de/']


class CoccinelleParseSpider(Mixin, BaseParseSpider):
    take_first = TakeFirst()
    price_x = "//span[@class='price']//text()"

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        pid = self.product_id(hxs)
        if hxs.select("//div[@class='product_not_saleble_view']"):
            return self.out_of_stock_garment(response, pid)

        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, hxs, response)

        garment['image_urls'] = self.image_urls(hxs)
        garment['skus'] = self.skus(hxs)
        return garment

    def skus(self, hxs):
        skus = {}
        #: Get colors from images_url in rare case when color label is  missing
        colors = clean(hxs.select("(//div[@id='swatch_holder_272'])[1]//img/@alt")) or self.get_colors(hxs)
        color_ids = clean(hxs.select("(//div[@id='swatch_holder_272'])[1]//img/@rel"))

        color_prices = self.get_prices(hxs)

        for color, color_id in zip(colors, color_ids):
            hxs = HtmlXPathSelector(text=color_prices[color_id])
            previous_price, price, currency = self.product_pricing(hxs)
            size = self.one_size

            sku = {
                'price': price,
                'currency': currency,
                'size': size,
                'colour': color,
            }

            if previous_price:
                sku['previous_prices'] = [previous_price]

            skus[color + '_' + size] = sku

        return skus

    def get_prices(self, hxs):
        prices_dict = {}
        color_prices = self.take_first(clean(hxs.select('//script[contains(text(), "prices_mappings")]//text()')))
        color_prices = json.loads(re.findall("prices_mappings\['.*?'\] = ({.*}); images", color_prices)[0])

        for color_price in color_prices.values():
            prices_dict.update({color_price['272']: color_price['price']})
        return prices_dict

    def get_colors(self, hxs):
        images = self.image_urls(hxs)
        pattern = "_(\w+?)\d+?_"
        return list(set([re.findall(pattern, image)[0].lower() for image in images]))

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("//input[@name='product']/@value")))

    def product_brand(self, hxs):
        return 'Coccinelle'

    def image_urls(self, hxs):
        color_ids = clean(hxs.select("(//div[@id='swatch_holder_272'])[1]//img/@rel"))
        xpath_t = "//div[@class='more-views']//li[contains(@id,'%s')]//img/@big"

        return [image for color_id in color_ids for image in clean(hxs.select(xpath_t % color_id))]

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//div[@class='product-name']//text()")))

    def product_category(self, hxs):
        categories = clean(hxs.select("//ul[@class='breadcrumbs']//text()"))
        return clean([category.strip('-') for category in categories])[1:-1]

    def raw_description(self, hxs):
        return clean(hxs.select("//div[@class='panel']//text()[not(parent::h2)]"))

    def product_description(self, hxs):
        return [rd for rd in self.raw_description(hxs) if not self.care_criteria(rd)]

    def product_care(self, hxs):
        return [rd for rd in self.raw_description(hxs) if self.care_criteria(rd)]


class CoccinelleCrawlSpider(Mixin, BaseCrawlSpider):
    deny_r = ['giftcard', 'feel-good', 'social', 'catalogue', 'campaign', 'season-trends', '/_/']

    listings_x = [
        "//div[@class='nav-container']",
        "//li[@class='next']",
    ]
    products_x = [
        "//ul[contains(@class,'products-grid')]//*[@class='product-name']",
    ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x, deny=deny_r),
             callback='parse_and_add_women'),

        Rule(SgmlLinkExtractor(restrict_xpaths=products_x, deny=['giftcard'])
             , callback='parse_item')
    )


class CoccinelleUKParseSpider(CoccinelleParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class CoccinelleUKCrawlSpider(CoccinelleCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = CoccinelleUKParseSpider()


class CoccinelleDEParseSpider(CoccinelleParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class CoccinelleDECrawlSpider(CoccinelleCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = CoccinelleDEParseSpider()

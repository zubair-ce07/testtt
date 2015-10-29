# -*- coding: utf-8 -*-
import re
from base import BaseParseSpider, BaseCrawlSpider, CurrencyParser
from base import clean
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='(%(processName)-10s) %(message)s',  #: Output the Process Name just for checking purposes
                    )


class Mixin(object):
    retailer = 'mango'
    allowed_domains = ['shop.mango.com']
    pfx = 'http://shop.mango.com/'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = [Mixin.pfx + 'GB']


class MangoParseSpider(BaseParseSpider):

    #: Path of money string
    price_x = '//span[@itemprop="price"]/span/text()'

    #: Callback function
    def parse(self, response):

        hxs = HtmlXPathSelector(response)

        #: Initialize the garment object by giving it a unique id
        xpath_id = '//div[@class="referenciaProducto row-fluid"]/text()'
        unique_id = clean(hxs.select(xpath_id))
        unique_id = re.search(u'REF. \d*', unique_id[0], flags=re.UNICODE).group()
        unique_id = unique_id.split('. ')[1]
        garment = self.new_unique_garment(unique_id)
        if garment is None:
            return

        self.boilerplate_normal(garment, hxs, response)
        previous_price, price, currency = self.product_pricing(hxs)

        #: Setting parameters for a garment
        garment['price'] = price
        garment['currency'] = currency
        garment['spider_name'] = self.name
        garment['gender'] = self.product_gender(hxs)
        garment['brand'] = self.product_brand(hxs)
        garment['image_urls'] = self.image_urls(hxs)
        garment['skus'] = self.skus(hxs)

        return garment

    def image_urls(self, hxs):
        small_images = clean(hxs.select('//div[@class="scroll_tray"]//img/@data-src'))
        #: Generate same images for large format
        large_images = map(lambda x: x.split('S1'), small_images)
        large_images = map(lambda x: x[0] + "S6" + x[1], large_images)
        return small_images + large_images

    def skus(self, hxs):
        xpath_skus = '//input[@class="inputOcultoColor"]/@value'
        sku_info_strings = clean(hxs.select(xpath_skus))
        color_list = clean(hxs.select('//div[@class="_color_div_on"]//img/@title'))
        #: Remove spaces from color list
        color_list = map(lambda x: x.strip(), color_list)

        skus = {}
        for color, sku_info_string in zip(color_list, sku_info_strings):

            previous_price, price, currency = self.product_pricing(hxs)
            #: Get sizes
            sizes = sku_info_string.split('#')
            sizes = map(lambda x: x.split('|'), sizes)

            for size in sizes:
                actual_size = size[2].split(' -')[0]
                out_of_stock = size[1]
                if out_of_stock == 'false':
                    out_of_stock = True
                else:
                    out_of_stock = False

                key = color + "_" + actual_size
                sku = {
                    'price': price,
                    'currency': currency,
                    'size': actual_size,
                    'colour': color,
                    'out_of_stock': out_of_stock,
                }
                if previous_price:
                    sku['previous_price'] = previous_price

                skus[key] = sku

        return skus

    def product_pricing(self, hxs):
        previous_price = ''
        money_string = clean(hxs.select(self.price_x))
        #: Join all elements of a list=money_string
        money_string = ''.join(map(unicode, money_string))
        currency, price = CurrencyParser.currency_and_price(money_string)

        #: Split the string
        money_string = money_string.split(u'£')
        if len(money_string) > 2:         #: It means product has previous price also
            previous_price = CurrencyParser.lowest_price(money_string[1])

        return previous_price, price, currency

    def product_gender(self, hxs):
        xpath_gen = '//li[contains(@class,"currentBrandMenu")]/a/text()'
        gender = clean(hxs.select(xpath_gen))[0]
        if gender == 'Plus Size':
            gender = 'Women'
        return gender

    def product_brand(self, hxs):
        return clean(hxs.select('//input[@id="id_brandItem_hidden"]/@value'))[0]

    def product_name(self, hxs):
        return clean(hxs.select('//div[@itemprop="name"]/h1/text()'))[0]

    def product_description(self, hxs):
        return clean(hxs.select('//div[@class="panel_descripcion"]//text() |'
                                ' //div[@class="tallas_descripcion"]/span/text()'))

    def product_care(self, hxs):
        care = clean(hxs.select('//div[@class="composicion"]//text()'))
        care = map(lambda x: x.strip('-'), care)
        #: Remove all the elements which are empty from the care list
        return [x for x in care if x]

    def product_category(self, hxs):
        return clean(hxs.select('//div[@class="pull-left breadcrumb_container"]/a//text()'))


class MangoCrawlSpider(BaseCrawlSpider, Mixin):

    #: Set the rules for scraping all the available products of a website
    rules = (

        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                '//div[contains(@class,"contentMenu__menu")]/div[1]/div//a')),
            callback='parse', follow=True
        ),
        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                '//div[@class="span12 product__page"]/div/div[1]//a')),
            callback='parse_item'
        ),
    )


class MangoUKParseSpider(MangoParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class MangoUKCrawlSpider(MangoCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = MangoUKParseSpider()



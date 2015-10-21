# -*- coding: utf-8 -*-
import re
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
import json
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
import logging
from scrapy.http import Request
import article
import xml.etree.ElementTree as ET


logging.basicConfig(level=logging.DEBUG,
                    format='(%(processName)-10s) %(message)s',  #: Output the Process Name just for checking purposes
                    )


class Mixin(object):
    retailer = 'sheego'
    allowed_domains = ['sheego.de']
    pfx = 'http://www.sheego.de/'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    start_urls = [Mixin.pfx]


class SheegoParseSpider(BaseParseSpider):

    price_x = '//div[@class="price holder"]/span/text()[1]'

    #: Callback function
    def parse(self, response):

        hxs = HtmlXPathSelector(response)

        #: Initialize the garment object by giving it a unique id
        garment = self.new_unique_garment(response.url.split('_')[1].split('-')[0])
        if garment is None:
            return

        self.boilerplate_normal(garment, hxs, response)
        previous_price, price, currency = self.product_pricing(HtmlXPathSelector(response))

        #: Setting parameters for a garment
        garment['price'] = price
        garment['currency'] = currency
        garment['spider_name'] = self.name
        garment['gender'] = 'women'
        garment['brand'] = self.product_brand(hxs)

        #: Initializing Image_urls list and skus Dictionary to avoid errors in further processing
        garment['image_urls'] = []
        garment['skus'] = {}

        #: Function to generate the requests for every sku
        queue = self.skus(response)
        #: Passing garment as meta data for each request
        queue = map(lambda x: x.replace(meta={'item': garment, 'dont_redirect': True, "handle_httpstatus_list": [301]}), queue)

        #: Initialize several data that you need while processing skus
        garment['meta'] = {}
        garment['meta']['requests_queue'] = queue
        garment['meta']['seen_colors'] = []
        g = GenerateXML()
        garment['meta']['body'] = g
        garment['meta']['key_list'] = []

        return self.next_request_or_garment(garment)

    #: Callback function that update availability status for each sku
    def set_skus_availability(self, response):

        garment = response.meta['item']
        key_list = garment['meta']['key_list']

        index = 1
        for key in key_list:
            sel = clean(XmlXPathSelector(response).select('(//DeliveryStatement/text())[' + str(index) + ']'))[0]
            #: Updating sku
            garment['skus'][key]['out_of_stock'] = not int(sel)
            index += 1

        return self.next_request_or_garment(garment)

    #: Callback function
    def skus(self, response):

        hxs = HtmlXPathSelector(response)
        #: Get art no from javascript of all sku Item which will be needed for all sku info
        script = clean(hxs.select('//div[@id="detailsuggestion"]/following::script[1]/text()'))[0]
        script = re.search('articlesString\(.*?\)', script).group()
        script = re.search("\'.*\'", script).group()
        script = script.split(';')

        #: Remove quotation marks from start and end
        script[0] = script[0].strip("'")
        script[-1] = script[-1].strip("'")


        queue = []

        it = iter(script)
        for script in it:
            url1 = response.url.split('_')
            url = url1[0] + '_' + url1[1].split('-')[0] + '-' + script[0:6] + '-' + next(it) + '-' + script[6:] + '.html'
            req = [Request(url, callback=self.parse_skus, dont_filter="True")]
            queue = queue + req

        return queue

    #: Call back function for extracting data for each sku
    def parse_skus(self, response):

        garment = response.meta['item']
        hxs = HtmlXPathSelector(response)

        color = clean(hxs.select('//div[contains(text(),"Farbe ")]/span/text()'))[0]
        color = re.sub(u'\W', u'', color,  flags=re.UNICODE)

        #: Getting images for every color if its not been seen before
        if color not in garment['meta']['seen_colors']:

            # Add color in seen colors
            garment['meta']['seen_colors'] = garment['meta']['seen_colors'] + [color]

            format_1s = clean(hxs.select('//div[@id="thumbslider"]//a//img/@data-src'))

            # Generate the urls for Zoom _ format images manually
            format_zoom = map(lambda x: x.split('format_1s'), format_1s)
            #: Filter out the elements of format_zoom on the bases of length
            format_zoom = filter(lambda x: len(x) == 2, format_zoom)
            #: Make a new image url
            format_zoom = map(lambda x: x[0] + "format_zoom" + x[1], format_zoom)

            #: Include all the parsed image urls in the garment
            garment['image_urls'] = garment['image_urls'] + format_1s + format_zoom

        skus = {}
        previous_price, price, currency = self.product_pricing(hxs)

        size = clean(hxs.select('//button[contains(@class,"btn active")]/text()'))[0]

        key = color + "_" + size
        sku = {
            'price': price,
            'currency': currency,
            'size': size,
            'colour': color,
        }
        if previous_price:
            sku['previous_price'] = previous_price
        else:
            #: Set previous price if base.py can not detect it
            previous_price = clean(HtmlXPathSelector(response).select('//sub[@class="wrongprice"]/text()'))
            if previous_price:
                sku['previous_price'] = re.sub(u'\D', u'', previous_price[0],  flags=re.UNICODE)

        skus[key] = sku

        #: Update the sku element of garment
        garment['skus'].update(skus)

        #: This list is needed in checking out_of_stock
        garment['meta']['key_list'] += [key]

        #: Now create the body for each sku so we can check availability later
        artNr = clean(hxs.select('//input[@name="artNr"]/@value'))[0]
        promotion_std = clean(hxs.select('//input[@name="aid"]/@value'))[0].split('-')[-1]

        size = clean(response.url.split('-')[-2])
        #: Generate a body here for each sku
        a = article.Article(artNr, size, promotion_std)
        g = garment['meta']['body']
        g.generate_one_element(a)

        #: If all the skus have been processed then generate POST request for checking the availability
        if not garment['meta']['requests_queue']:
            body = garment['meta']['body']
            body = body.print_xml()
            garment['meta']['requests_queue'] = garment['meta']['requests_queue'] + [Request('http://www.sheego.de/request/kal.php', method='POST', body=body, meta={'item': garment}, callback=self.set_skus_availability, dont_filter=True)]

        return self.next_request_or_garment(garment)

    def product_brand(self, hxs):
        return clean(hxs.select('(//div[@class="brand"]//text())[2]'))

    def product_name(self, hxs):
        return clean(hxs.select('(//span[@itemprop="name"]/text())[1]'))

    def product_description(self, hxs):
        return clean(hxs.select('//div[@id="moreinfo-highlight"]//li/text()')) + clean(hxs.select('(//div[@itemprop="description"])[1]/text()'))

    def product_care(self, hxs):
        return clean(hxs.select('(//td//span[text()="Materialzusammensetzung"]/following::td[1]/text())[1]  | (//dl[@class="dl-horizontal articlequality"])[1]//text()'))

    def product_category(self, hxs):
        return clean(hxs.select('(//ul[@class="breadcrumb"])[1]//a/text()'))


class SheegoCrawlSpider(BaseCrawlSpider, Mixin):

    #: Set the rules for scraping all the available products of a website
    rules = (

        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                '(//ul[@class="mainnav__ul js-mainnav-ul"]/li//a)[position() < 4]')),
            callback='parse', follow=True
        ),
        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                '//a[@class="br js-pl-product"]')),
            callback='parse_item'
        ),
    )


class SheegoUKParseSpider(SheegoParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class SheegoUKCrawlSpider(SheegoCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = SheegoUKParseSpider()


class SheegoUKCrawlSpider(SheegoCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = SheegoUKParseSpider()


class GenerateXML(object):
    def __init__(self):
        self.xml = ''
        self.append_static_elements()

    def generate_one_element(self, article):
        parent = self.xml.find('.//Articles')
        a = ET.SubElement(parent, 'Article')
        b = ET.SubElement(a, 'CompleteCatalogItemNo')
        b.text = str(article.complete_catalog_item_no)
        c = ET.SubElement(a, 'SizeAlphaText')
        c.text = str(article.size_alpha_tex)
        d = ET.SubElement(a, 'Std_Promotion')
        d.text = article.std_promotion
        e = ET.SubElement(a, 'CustomerCompanyID')
        e.text = str(article.customer_company_id)

    def append_static_elements(self):
        a = ET.Element('tns:KALAvailabilityRequest')
        a.set("xmlns:tns", "http://www.schwab.de/KAL")
        a.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        a.set("xsi:schemaLocation", "http://www.schwab.de/KAL http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd")
        ET.SubElement(a, 'Articles')
        self.xml = a

    def print_xml(self):
        return ET.tostring(self.xml)



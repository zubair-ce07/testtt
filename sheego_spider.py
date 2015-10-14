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

        #: Function to generate requests for each color
        queue = self.get_colours(hxs)
        queue = map(lambda x: x.replace(meta={'item': garment}), queue)

        garment['meta'] = {}
        garment['meta']['requests_queue'] = queue

        #: Function to generate the requests for getting information regarding OUT_Of_Stock for each sku
        queue, key_list = self.skus(hxs)
        queue = map(lambda x: x.replace(meta={'item': garment, 'key': key_list}), queue)

        garment['meta']['requests_queue'] = garment['meta']['requests_queue'] + queue

        return self.next_request_or_garment(garment)

    def parse_skus_and_images(self, response):

        #: Get the data that has been set  in the Request.meta
        garment = response.meta['item']

        #: Get all the images for a specific color
        format_1s = clean(HtmlXPathSelector(response).select('//div[@class="js-product-thumbs-slider"]//a/img/@data-src'))

        # Generate the urls for Zoom _ format images manually
        format_zoom = map(lambda x: x.split('format_1s'), format_1s)
        #: Filter out the elements of format_zoom on the bases of length
        format_zoom = filter(lambda x: len(x) == 2, format_zoom)
        #: Make a new image url
        format_zoom = map(lambda x: x[0] + "format_zoom" + x[1], format_zoom)

        #: Include all the parsed url in the garment
        garment['image_urls'] = garment['image_urls'] + format_1s + format_zoom

        #: Get all the sizes of a specific color
        size_list = clean(HtmlXPathSelector(response).select('//div[@class=" js-variantSelector size clearfix"]//button/@data-noa-size'))

        #: Get the current color value
        color = clean(HtmlXPathSelector(response).select('//div[@class="color js-variantSelector"]/div/span/text()'))[0]
        #: "Detect color" of base.py is not working here for all colors that's why I used regular expression
        color = re.sub(u'\W', u'', color,  flags=re.UNICODE)

        #: Remove non-acsii characters else not acceptable as key value
        color = ''.join([i if ord(i) < 128 else ' ' for i in color])

        #: Update skus for each size of current color
        skus = {}
        previous_price, price, currency = self.product_pricing(HtmlXPathSelector(response))

        for size in size_list:

            key = str(color) + "_" + str(size)
            sku = {
                'price': price,
                'currency': currency,
                'size': size,
                'colour': color,
                'out_of_stock': garment['skus'][key]['out_of_stock']
            }
            if previous_price:
                sku['previous_price'] = previous_price
            else:
                #: Set previous price if base.py can not detect it
                previous_price = clean(HtmlXPathSelector(response).select('//div[@class="price holder"]/span/sub[@class="wrongprice"]/text()'))
                if previous_price:
                    sku['previous_price'] = re.sub(u'\D', u'', previous_price[0],  flags=re.UNICODE)

            skus[key] = sku

        #: Update the sku element of the garment
        garment['skus'].update(skus)
        return self.next_request_or_garment(garment)

    def set_skus_availability(self, response):

        skus = {}
        garment = response.meta['item']
        key_list = response.meta['key']

        index = 1
        for key in key_list:
            sel = clean(XmlXPathSelector(response).select('(//Stock/text())[' + str(index) + ']'))[0]
            sku = {
                'out_of_stock': not int(sel)
            }
            skus[key] = sku
            garment['skus'].update(skus)
            index += 1

        return self.next_request_or_garment(garment)

    def skus(self, hxs):

        #: Get the ids from color urls to get the information regarding std_promotion
        ids = clean(hxs.select('//ul[@class="cover list-unstyled list-inline"]//a/@href'))

        colors = clean(hxs.select('//ul[@class="cover list-unstyled list-inline"]//a//img/@title'))
        colors = map(lambda x: re.sub(u'\W', u'', x,  flags=re.UNICODE), colors)

        if len(ids) != len(colors):
            #: Get div information also
            colors1 = clean(hxs.select('//ul[@class="cover list-unstyled list-inline"]//a//div/text()'))
            #: Get only last word from a sentence
            colors1 = map(lambda x: x.rsplit(None, 1)[-1], colors1)
            colors =  colors + colors1

        #: If any of the color has non ascii character the remove it otherwise it will not be acceptable as key
        colors = map(lambda x: ''.join([i if ord(i) < 128 else ' ' for i in x]), colors)

        sizes = clean(hxs.select('//div[@data-toggle="buttons-checkbox"]/button/@data-noa-size'))

        index = 0

        g = GenerateXML()
        key_list = []
        for color in colors:

            id1 = ids[index].split('_')[1].split('p.html')[0].split('-')
            for size in sizes:

                key_list.append(str(color) + "_" + str(size))
                #: Generate a body here for each request
                a = article.Article(id1[1]+id1[2], size, id1[2])
                g.generate_one_element(a)
                #: Make a post request for each sku item to get the information regarding out_of_stock
            index += 1
        body = g.print_xml()
        logging.info(body)
        queue = [Request('http://www.sheego.de/request/kal.php', method='POST', body=body, callback=self.set_skus_availability, dont_filter=True)]

        return queue, key_list

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

    def get_colours(self, hxs):

        queue = []
        colors = clean(hxs.select('//ul[@class="cover list-unstyled list-inline"]//a/@href'))

        for color in colors:
            queue = queue + [Request(color, callback=self.parse_skus_and_images, dont_filter=True)]

        return queue


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




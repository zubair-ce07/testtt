#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from sheego.items import SheegoItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http.request import Request
from scrapy.http import FormRequest
import re


class SheegoSpider(CrawlSpider):
    name = "SheegoSpider"
    allowed_domains = ["sheego.de"]
    start_urls = [
        "http://www.sheego.de/"
    ]
    main_menu_xpath = '//a[contains(@class,"expandable")]/following-sibling::div//div[contains(@class,"subnavigation")]//li/a'
    products_page_xpath = '//div[contains(@class,"product-box")]//*[contains(@class,"item-desc")]/a'
    pagination_xpath = './/a[@class="next js-next btn btn-next"]'
    rules = [

        Rule(LinkExtractor(restrict_xpaths=main_menu_xpath)),
        Rule(LinkExtractor(restrict_xpaths=products_page_xpath, attrs='data-url'), callback='get_product_detail'),
        Rule(LinkExtractor(restrict_xpaths=pagination_xpath))
    ]

    varselid = ''
    last = ''

    def get_product_detail(self, response):
        item = SheegoItem()
        item['retailer'] = 'Sheego'
        item['spider_name'] = self.name
        item['category'] = self.get_category(response)
        item['url'] = response.url
        item['description'] = self.get_description(response)
        item['image_urls'] = []
        colors = response.xpath('.//*[@class="moreinfo-color colors"]/ul/li/a/@href').extract()
        url = response.url
        match = re.search("\_([\w-]+)\.html$", url)
        parentid = match.group(1)
        size_with_price = {}
        return self.request_for_color(colors, item, size_with_price, parentid)

    def request_for_color(self, colors, item, size_with_price, parentid):
        return Request(url=colors.pop(0), callback=self.parse_colors_from_product,
                       meta={'color': colors,
                             'item': item,
                             'size_with_price': size_with_price, 'parentid': parentid})

    def parse_colors_from_product(self, response):
        parentid = response.meta['parentid']
        size_with_price = response.meta['size_with_price']
        colors = response.meta['color']
        item = response.meta['item']
        self.get_images(response, item)
        if response.xpath(
                './/*[@id="variants"]//*[@class="variants js-variantSelector js-moreinfo-variant js-sh-dropdown"]'):
            variant_select = response.xpath(
                './/*[@id="variants"]//*[@class="variants js-variantSelector js-moreinfo-variant js-sh-dropdown"]/option[not(contains(@selected,"selected"))]/@value').extract()
            selected = response.xpath(
                './/*[@id="variants"]//*[@class="variants js-variantSelector js-moreinfo-variant js-sh-dropdown"]/option[contains(@selected,"selected")]/@value').extract()[
                0]
            if (selected == ''):
                self.varselid = variant_select[0]
            else:
                self.varselid = selected
                selected = ''
            sizes = response.xpath('.//*[@id="variants"]//button/@data-selection-id').extract()
            size_title = response.xpath('.//*[@id="variants"]//button/text()').extract()
            match = re.search("(\d+)", size_title[0])
            size_title[0] = match.group(1)
            return self.request_for_size(response, colors, item, size_with_price, variant_select, size_title, sizes,
                                         parentid)
        else:
            size_check = response.xpath(
                './/*[@id="variants"]//div[@class="js-sizeSelector cover js-moreinfo-size"]')
            if not size_check:
                price = self.get_price(response)
                color = self.get_color(response)
                size = 'One-Size'
                size_with_price[size + "_" + color] = {'color': color,
                                                       'size': size,
                                                       'price': price}
                if colors:
                    return self.request_for_color(colors, item, size_with_price, parentid)
                else:
                    item['skus'] = self.get_skus(size_with_price)
                    return item
            else:
                size_title = response.xpath('.//*[@id="variants"]//button/text()').extract()
                match = re.search("(\d+)", size_title[0])
                size_title[0] = match.group(1)
                sizes = response.xpath('.//*[@id="variants"]//button/@data-selection-id').extract()
                return self.request_for_size(response, colors, item, size_with_price, None, size_title, sizes, parentid)

    def request_for_size(self, response, colors, items, size_with_price, variants, size_title, sizes, parentid):
        actCtrl = response.xpath('.//input[@name="actcontrol"]/@value').extract()[0]
        aid = response.xpath('.//input[@name="aid"]/@value').extract()[0]
        artid = response.xpath('.//input[@name="artNr"]/@value').extract()[0]
        path = response.xpath('.//input[@name="econdapath"]/@value').extract()[0]
        aid = re.sub(r'-\w{2}-', '-' + size_title[0] + '-', aid)
        self.last = sizes.pop(0)
        yield FormRequest.from_response(response,
                                        formdata={
                                            'actcontrol': str(actCtrl)
                                            , 'aid': str(aid),
                                            'ajaxdetails': 'ajaxdetailsPage',
                                            'anid': str(parentid),
                                            'artNr': str(artid),
                                            'cl': 'oxwarticledetails',
                                            'econdapath': path,
                                            'parentid': str(parentid),
                                            'selectFirstDeliverableProduct': '1',
                                            'varselid[0]': self.last,
                                            'varselid[1]': self.varselid
                                        }, formxpath=str('.//form[@class="js-oxProductForm niceform"]'),
                                        callback=self.parse_price_from_sizes,
                                        meta={'variant_select': variants, 'sizes': sizes,
                                              'size_with_price': size_with_price, 'item': items, 'color': colors,
                                              'title': size_title, 'parentid': parentid})

    def request_for_variants(self, response, colors, item, size_with_price, variant_select, parentid):
        actCtrl = response.xpath('.//input[@name="actcontrol"]/@value').extract()[0]
        aid = response.xpath('.//input[@name="aid"]/@value').extract()[0]
        artid = response.xpath('.//input[@name="artNr"]/@value').extract()[0]
        path = response.xpath('.//input[@name="econdapath"]/@value').extract()[0]
        self.varselid = variant_select.pop(0)
        yield FormRequest.from_response(response,
                                        formdata={
                                            'actcontrol': str(actCtrl)
                                            , 'aid': str(aid),
                                            'ajaxdetails': 'ajaxdetailsPage',
                                            'anid': str(parentid),
                                            'artNr': str(artid),
                                            'cl': 'oxwarticledetails',
                                            'econdapath': path,
                                            'parentid': str(parentid),
                                            'selectFirstDeliverableProduct': '1',
                                            'varselid[0]': self.last,
                                            'varselid[1]': self.varselid
                                        }, formxpath=str('.//form[@class="js-oxProductForm niceform"]'),
                                        callback=self.parse_size_from_models,
                                        meta={'variant_select': variant_select, 'size_with_price': size_with_price,
                                              'item': item, 'color': colors, 'parentid': parentid})

    def parse_price_from_sizes(self, response):
        parentid = response.meta['parentid']
        colors = response.meta['color']
        sizes = response.meta['sizes']
        size_title = response.meta['title']
        variant_select = response.meta['variant_select']
        size_with_price = response.meta['size_with_price']
        item = response.meta['item']
        size_title.pop(0)
        if size_title:
            match = re.search("(\d+)", size_title[0])
            size_title[0] = match.group(1)
        size_temp = \
            response.xpath(
                u'.//*[@id="variants"]//*[@class="title" and contains(text(),"Grösse")]//span/text()').extract()[0]
        price = self.get_price(response)
        color = self.get_color(response)
        size = size_temp.lstrip(u'– ')
        size_with_price[size + "_" + color] = {'color': color,
                                               'size': size,
                                               'price': price}
        newbody = response.body.replace("<div>",
                                        '<form class="js-oxProductForm niceform" method="post" action="http://www.sheego.de/index.php?">\n <div>',
                                        1)
        response = response.replace(body=newbody)
        if sizes:
            return self.request_for_size(response, colors, item, size_with_price, variant_select, size_title, sizes,
                                         parentid)
        elif variant_select:
            return self.request_for_variants(response, colors, item, size_with_price, variant_select, parentid)
        elif colors:
            return self.request_for_color(colors, item, size_with_price, parentid)
        else:
            item['skus'] = self.get_skus(size_with_price)
            return item

    def parse_size_from_models(self, response):
        size_with_price = response.meta['size_with_price']
        colors = response.meta['color']
        item = response.meta['item']
        parentid = response.meta['parentid']
        variant_select = response.meta['variant_select']
        newbody = response.body.replace("<div>",
                                        '<form class="js-oxProductForm niceform" method="post" action="http://www.sheego.de/index.php?">\n <div>',
                                        1)
        response = response.replace(body=newbody)
        size_check = response.xpath(
            './/*[@id="variants"]//div[@class="js-sizeSelector cover js-moreinfo-size"]')
        if size_check:
            sizes = response.xpath('.//*[@id="variants"]//button/@data-selection-id').extract()
            size_title = response.xpath('.//*[@id="variants"]//button/text()').extract()
            match = re.search("(\d+)", size_title[0])
            size_title[0] = match.group(1)
            return self.request_for_size(response, colors, item, size_with_price, variant_select, size_title, sizes,
                                         parentid)
        else:
            price = self.get_price(response)
            color = self.get_color(response)
            size = 'One-Size'
            size_with_price[size + "_" + color] = {'color': color,
                                                   'size': size,
                                                   'price': price}
            if variant_select:
                return self.request_for_variants(response, colors, item, size_with_price, variant_select, parentid)
            elif colors:
                return self.request_for_color(colors, item, size_with_price, parentid)
            else:
                item['skus'] = self.get_skus(size_with_price)
                return item

    def get_images(self, response, item):
        images = response.xpath('.//*[@id="thumbslider"]//a/img[contains(@data-src,"4s$")]/@data-src').extract()
        for img in images:
            item['image_urls'].append(img)

    def get_title(self, response):
        title = response.xpath('.//span[@itemprop="name"]/text()').extract()[0]
        return title

    def get_category(self, response):
        category = response.xpath('.//*[@id="breadcrumb"]//li[position()>1]/a/text()').extract()
        return category

    def get_color(self, response):
        color = response.xpath('.//*[@class="color js-variantSelector"]/div[@class="title"]/span/text()').extract()[0]
        return color.lstrip(u'— ')

    def get_description(self, response):
        description = response.xpath('.//*[@id="moreinfo-highlight"]//li/text()').extract()
        return description

    def get_price(self, response):
        new_price = response.xpath('.//*[@class="lastprice"]/text()').extract()[0].strip()
        old_price = response.xpath('.//*[@class="price holder"]//sub/text()').extract()
        if len(old_price) == 0:
            return (' ').join(new_price.split())
        else:
            return {'new_price': (' ').join(new_price.split()), 'old_price': (' ').join(old_price[0].split())}

    def get_skus(self, size):
        skus = size
        return skus

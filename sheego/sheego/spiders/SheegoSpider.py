#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from sheego.items import SheegoItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http.request import Request
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import FormRequest
import re


class SheegoSpider(CrawlSpider):
    name = "SheegoSpider"
    allowed_domains = ["sheego.de"]
    start_urls = [
        "http://www.sheego.de/"
    ]
    main_menu_xpath = '(//a[contains(@class,"expandable")]/following-sibling::div//div[contains(@class,"subnavigation")]//li)[11]/a'
						# this for limited menu for all //a[contains(@class,"expandable")]/following-sibling::div//div[contains(@class,"subnavigation")]//li/a
    products_page_xpath = '//div[contains(@class,"product-box")]//div[contains(@class,"color")]//li[1]/a'
    #pagination_xpath = './/a[@class="next js-next btn btn-next"]'
    rules = [

        Rule(LinkExtractor(restrict_xpaths=main_menu_xpath)),
        Rule(LinkExtractor(restrict_xpaths=products_page_xpath),
             process_request='save_links'),
        #Rule(LinkExtractor(restrict_xpaths=pagination_xpath))
    ]

    varselid = ''
    urlTemp = ''
    last = ''
    size_with_price = []
    select = []
    urls = []
    size_action_response = None

    def __init__(self, *args, **kwargs):
        super(SheegoSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_idle)

    def spider_closed(self, spider):
        if self.urls:
            self.crawler.engine.crawl(self.next_url_request(), spider)

    def save_links(self, value):
        if value.url not in self.urls:
            self.urls.append(value.url)
        return None

    def next_url_request(self):
        if self.urls:
            return Request(url=self.urls.pop(),
                           callback=self.get_product_detail,
                           dont_filter=True)

    def get_title(self, response):
        title = response.xpath('.//span[@itemprop="name"]/text()').extract()[0]
        return title

    def get_cat(self, response):
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
        skus = {}
        for result in size:
            arr = {}
            arr['currency'] = 'US'
            arr['colour'] = result[2]
            arr['price'] = result[1]
            arr['size'] = result[0]
            arr['available'] = result[3]
            skus[arr['size'] + '_' + arr['colour']] = arr
        return skus

    def parse_size(self, response):
        actCtrl = response.xpath('.//input[@name="actcontrol"]/@value').extract()[0]
        aid = response.xpath('.//input[@name="aid"]/@value').extract()[0]
        artid = response.xpath('.//input[@name="artNr"]/@value').extract()[0]
        path = response.xpath('.//input[@name="econdapath"]/@value').extract()[0]
        match = re.search("\_([\w-]+)\.html$", self.urlTemp)
        parentid = match.group(1)
        colors = response.meta['color']
        item = response.meta['item']
        variant_select = response.meta['select']
        self.varselid = variant_select[-1]
        if (variant_select > 0):
            variant_select.pop()
            sizes = response.xpath('.//*[@id="variants"]//button/@data-selection-id').extract()
            size_title = response.xpath('.//*[@id="variants"]//button/text()').extract()
            size_title.reverse()
            sizes.reverse()
            aid = re.sub(r'-\w{2}-', '-' + size_title[-1] + '-', aid)
            self.size_action_response = response
            newbody = response.body.replace("<div>",
                                            '<form class="js-oxProductForm niceform" method="post" action="http://www.sheego.de/index.php?">\n <div>',
                                            1)
            response = response.replace(body=newbody)
            self.select = variant_select
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
                                                'varselid[0]': sizes[-1],
                                                'varselid[1]': self.varselid

                                            }, formxpath=str('.//form[@class="js-oxProductForm niceform"]'),
                                            callback=self.parse_price,
                                            meta={'sizes': sizes, 'item': item, 'color': colors, 'title': size_title})
        else:
            yield Request(url=colors[-1], callback=self.parse_color, meta={'color': colors, 'item': item},
                          dont_filter=True)

    def parse_color(self, response):
        self.urlTemp = response.url
        colors = response.meta['color']
        item = response.meta['item']
        images = response.xpath('.//*[@id="thumbslider"]//a/img[contains(@data-src,"4s$")]/@data-src').extract()
        for img in images:
            item['image_urls'].append(img)
        if (len(colors) > 0):
            colors.pop()
            if (len(response.xpath(
                    './/*[@id="variants"]//*[@class="variants js-variantSelector js-moreinfo-variant js-sh-dropdown"]')) != 0):
                variant_select = response.xpath(
                    './/*[@id="variants"]//*[@class="variants js-variantSelector js-moreinfo-variant js-sh-dropdown"]/option[not(contains(@selected,"selected"))]/@value').extract()
                selected = response.xpath(
                    './/*[@id="variants"]//*[@class="variants js-variantSelector js-moreinfo-variant js-sh-dropdown"]/option[contains(@selected,"selected")]/@value').extract()[
                    0]
                variant_select.reverse()
                self.select = variant_select
                if (selected == ''):
                    self.varselid = variant_select[-1]
                else:
                    self.varselid = selected
                    selected = ''
                actCtrl = response.xpath('.//input[@name="actcontrol"]/@value').extract()[0]
                aid = response.xpath('.//input[@name="aid"]/@value').extract()[0]
                artid = response.xpath('.//input[@name="artNr"]/@value').extract()[0]
                path = response.xpath('.//input[@name="econdapath"]/@value').extract()[0]
                match = re.search("\_([\w-]+)\.html$", self.urlTemp)
                parentid = match.group(1)
                size_title = response.xpath('.//*[@id="variants"]//button/text()').extract()
                size_title.reverse()
                match = re.search("(\d+)", size_title[-1])
                size_title[-1] = match.group(1)
                sizes = response.xpath('.//*[@id="variants"]//button/@data-selection-id').extract()
                sizes.reverse()
                aid = re.sub(r'-\w{2}-', '-' + size_title[-1] + '-', aid)
                self.size_action_response = response
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
                                                    'varselid[0]': sizes[-1],
                                                    'varselid[1]': self.varselid
                                                }, formxpath=str('.//form[@class="js-oxProductForm niceform"]'),
                                                callback=self.parse_price,
                                                meta={'select': variant_select, 'sizes': sizes, 'item': item,
                                                      'color': colors, 'title': size_title})
            else:
                size_check = response.xpath(
                    './/*[@id="variants"]//div[@class="js-sizeSelector cover js-moreinfo-size"]')
                if (len(size_check) == 0):
                    price = self.get_price(response)
                    color = self.get_color(response)
                    available = True
                    self.size_with_price.append(['One-Size', price, color, available])
                    if (len(colors) > 0):
                        yield Request(url=colors[-1], callback=self.parse_color, meta={'color': colors, 'item': item},
                                      dont_filter=True)
                    else:
                        item['skus'] = self.get_skus(self.size_with_price)
                        yield item
                else:
                    size_title = response.xpath('.//*[@id="variants"]//button/text()').extract()
                    size_title.reverse()
                    match = re.search("(\d+)", size_title[-1])
                    size_title[-1] = match.group(1)
                    sizes = response.xpath('.//*[@id="variants"]//button/@data-selection-id').extract()
                    actCtrl = response.xpath('.//input[@name="actcontrol"]/@value').extract()[0]
                    aid = response.xpath('.//input[@name="aid"]/@value').extract()[0]
                    artid = response.xpath('.//input[@name="artNr"]/@value').extract()[0]
                    path = response.xpath('.//input[@name="econdapath"]/@value').extract()[0]
                    match = re.search("\_([\w-]+)\.html$", self.urlTemp)
                    parentid = match.group(1)
                    aid = re.sub(r'-\w{2}-', '-' + size_title[-1] + '-', aid)
                    self.size_action_response = response
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
                                                        'varselid[0]': sizes[-1]
                                                    }, formxpath=str('.//form[@class="js-oxProductForm niceform"]'),
                                                    callback=self.parse_price,
                                                    meta={'sizes': sizes, 'item': item, 'color': colors,
                                                          'title': size_title})
        else:
            item['skus'] = self.get_skus(self.size_with_price)
            yield item

    def parse_price(self, response):
        colors = response.meta['color']
        sizes = response.meta['sizes']
        size_title = response.meta['title']
        variant_select = self.select
        sizes.pop()
        size_title.pop()
        if (len(size_title) > 0):
            match = re.search("(\d+)", size_title[-1])
            size_title[-1] = match.group(1)
        item = response.meta['item']
        size_temp = \
            response.xpath(
                u'.//*[@id="variants"]//*[@class="title" and contains(text(),"Grösse")]//span/text()').extract()[0]
        price = self.get_price(response)
        color = self.get_color(response)
        stock = self.size_action_response.xpath(
            './/*[@id="variants"]//button[contains(text(),"' + size_temp.lstrip(u'– ') + '")]/@disabled').extract()
        if (len(stock) == 0):
            available = True
        else:
            available = False
        self.size_with_price.append([size_temp.lstrip(u'– '), price, color, available])
        newbody = response.body.replace("<div>",
                                        '<form class="js-oxProductForm niceform" method="post" action="http://www.sheego.de/index.php?">\n <div>',
                                        1)
        response = response.replace(body=newbody)

        if (len(sizes) > 0):
            actCtrl = response.xpath('.//input[@name="actcontrol"]/@value').extract()[0]
            aid = response.xpath('.//input[@name="aid"]/@value').extract()[0]
            artid = response.xpath('.//input[@name="artNr"]/@value').extract()[0]
            path = response.xpath('.//input[@name="econdapath"]/@value').extract()[0]
            match = re.search("\_([\w-]+)\.html$", self.urlTemp)
            parentid = match.group(1)
            aid = re.sub(r'-\w{2}-', '-' + size_title[-1] + '-', aid)
            self.last = sizes[-1]
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
                                                'varselid[0]': sizes[-1],
                                                'varselid[1]': str(self.varselid)
                                            }, formxpath='.//form[@class="js-oxProductForm niceform"]',
                                            callback=self.parse_price,
                                            meta={'sizes': sizes, 'item': item, 'color': colors, 'title': size_title})
        elif (len(variant_select) > 0):
            actCtrl = response.xpath('.//input[@name="actcontrol"]/@value').extract()[0]
            aid = response.xpath('.//input[@name="aid"]/@value').extract()[0]
            artid = response.xpath('.//input[@name="artNr"]/@value').extract()[0]
            path = response.xpath('.//input[@name="econdapath"]/@value').extract()[0]
            match = re.search("\_([\w-]+)\.html$", self.urlTemp)
            parentid = match.group(1)
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
                                                'varselid[1]': variant_select[-1]
                                            }, formxpath=str('.//form[@class="js-oxProductForm niceform"]'),
                                            callback=self.parse_size,
                                            meta={'select': variant_select, 'item': item, 'color': colors})
        else:
            if (len(colors) > 0):
                yield Request(url=colors[-1], callback=self.parse_color, meta={'color': colors, 'item': item},
                              dont_filter=True)
            else:
                item['skus'] = self.get_skus(self.size_with_price)
                yield item

    def get_product_detail(self, response):
        item = SheegoItem()
        item['retailer'] = 'Sheego'
        item['spider_name'] = self.name
        item['category'] = self.get_cat(response)
        item['url'] = response.url
        item['description'] = self.get_description(response)
        item['image_urls'] = []
        colors = response.xpath('.//*[@class="moreinfo-color colors"]/ul/li/a/@href').extract()
        self.urlTemp = response.url
        colors.reverse()
        self.size_with_price = []
        yield Request(url=colors[-1], callback=self.parse_color, meta={'color': colors, 'item': item}, dont_filter=True)

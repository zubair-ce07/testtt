# -*- coding: utf-8 -*-
__author__ = 'mateenahmeed'
import scrapy
import re
from orsaySpider.items import orsayItem
from orsaySpider.items import skuItem


class sku_rec_Spider(scrapy.Spider):
    name = "sku_rec"
    start_urls = [

        "http://www.orsay.com/de-de/accessoires/tuecher/loop-tuch-mit-leo-print-koral-92900936.html",
        "http://www.orsay.com/de-de/accessoires/tuecher/loop-tuch-mit-leo-print-himbeerrot-92900931.html",
        "http://www.orsay.com/de-de/accessoires/tuecher/tuch-mit-blumen-print-korallrot-92703722.html",
        "http://www.orsay.com/de-de/accessoires/tuecher/loop-tuch-mit-leo-print-weissgrau-92900701.html",
        "http://www.orsay.com/de-de/accessoires/tuecher/tuch-mit-punkten-92703652.html",
        "http://www.orsay.com/de-de/accessoires/tuecher/tuch-mit-punkten-koral-92703636.html",
        "http://www.orsay.com/de-de/accessoires/tuecher/tuch-mit-punkten-weissgrau-92703601.html",
        "http://www.orsay.com/de-de/accessoires/tuecher/tuch-mit-print-92808232.html",

    ]

    def parse(self, response):

        sel = response.xpath("/html")

        # Making an object of our class present in items.py
        item = orsayItem()

        # just to make things little simpler
        # sel1 is used when we are getting more specific information related to product main
        sel1 = response.xpath("//div[@id='product_main']")

        sku = sel1.xpath("//p[@class='sku']/text()").extract()[0].strip()

        item['retailer_sku'] = re.findall('\d+', sku)[0]

        item['description'] = [i.strip() for i in
                               sel.xpath("//div[@class='product-info six columns']"
                                         "/p/text()").extract()]

        item['url_orignal'] = response.url
        url_link = response.url.split("/")
        if (len(url_link) > 5):
            item['category'] = url_link[4:-1]
        else:
            item['category'] = []

        item['image_urls'] = sel.xpath("//div[@id='product_media']/div/img/@src").extract()

        item['care'] = [i.strip() for i in
                        sel.xpath("//p[@class='material']/text() |"
                                  " //ul[@class='caresymbols']/li/img/@src").extract()]

        item['lang'] = sel.xpath("/html/@lang").extract()[0]

        item['name'] = sel1.xpath("//h2[@class='product-name']/text()").extract()[0].strip()

        # price for currency
        price = sel1.xpath("//div[@class='product-main-info']"
                           "/div/span/span[@class='price']/text()").extract()
        if (len(price) == 0):
            price = sel1.xpath("//p[@class='special-price']"
                               "/span[@class='price']/text()").extract()
        item['currency'] = price[0].strip()[-3:]

        item['skus'] = {}

        hre = response.xpath("//ul[@class='product-colors']/li/a/@href").extract()
        length = len(hre)
        #item['colors_available'] = 0

        print("length of urls before 1 : ", length)
        print hre
        if length:
            my_url = hre.pop(0)
            print("url :", my_url)
            print hre
            print("length of urls after 1 : ", len(hre))
            full_url = response.urljoin(my_url)
            req = scrapy.Request(full_url, callback=self.parse_sku, meta={'item': item, 'urls': hre})
            yield req

        if not length:
            yield item

    def parse_sku(self, response):

        item = response.meta["item"]
        urls = response.meta["urls"]
        #counts = item['colors_available']

        sel = response.xpath("/html")
        sel1 = response.xpath("//div[@id='product_main']")

        in_item = skuItem()

        # in_item['currency'] = sel.xpath("//@data-currency").extract()[0]

        # price
        price = sel1.xpath("//div[@class='product-main-info']"
                           "/div/span/span[@class='price']/text()").extract()
        if (len(price) == 0):
            price = sel1.xpath("//p[@class='special-price']"
                               "/span[@class='price']/text()").extract()
        in_item['price'] = re.sub("[^\d\.]", "", price[0].strip())

        in_item['currency'] = price[0].strip()[-3:]

        # previous pricess
        prev = []
        for i in sel1.xpath(
                "//div[@class='product-main-info']/div/p[@class='old-price']"
                "/span[@class='price']/text()").extract():
            prev.append(i.strip())
        in_item['previous_prices'] = []
        for s in prev:
            in_item['previous_prices'].append(re.sub("[^\d\.]", "", s))

        in_item['colour'] = sel1.xpath("//li[@class='active']"
                                       "/a/img[@class='has-tip']/@alt").extract()[0].strip()
        # size
        size_list = [i.strip() for i in sel1.xpath(
            "//ul/li[@class='size-box ship-available']/text()").extract()]

        if (not len(size_list)) or (size_list[0] == "0"):
            size_list = ["oneSize"]
        for sz in size_list:
            in_item_t = skuItem(in_item)
            in_item_t['size'] = sz
            color_size = in_item_t['colour'] + "_" + sz
            item['skus'][color_size] = in_item_t

        for k, v in item['skus'].items():
            # Display key and value.
            print(k, v)

        print("length of urls before : ", len(urls))
        for x in urls:
            print(x)
        if len(urls):

            my_url = urls.pop(0)
            print("length of urls after : ", len(urls))
            for x in urls:
                print(x)
            full_url = response.urljoin(my_url)
            req = scrapy.Request(full_url, callback=self.parse_sku, meta={'item': item, 'urls': urls})
            yield req
        else:
            yield item

# from __future__ import absolute_import
import scrapy
import re
import json
from orsay.items import Product
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


def url(response, product):
    product['url'] = response.url


def brand(response, product):
    product['brand'] = response.xpath(
        "//script[@type='application/ld+json']/text()").re(r'Brand.*name":"(\w*)"},')[0]


def care(response, product):
    product['care'] = response.xpath(
        "//div[@class='product-care six columns']//@src | //p[@class='material']/text()").extract()


def description(response, product):
    product['description'] = str(response.xpath(
        "//p[@class='description']/text()").extract()[0]).strip()


def image_urls(response, product):
    product['image_urls'] = response.xpath(
        "//div[@class='product-image-gallery-thumbs configurable']//@href").extract()


def name(response, product):
    product['name'] = response.css("h1.product-name::text").extract()


def color_urls(response, product):
    product['color_urls'] = [n.strip() for n in response.xpath(
        "//ul[@class='product-colors']//a/@href").extract() if n != '#']


def retailer_sku(response, product):
    product['retailer_sku'] = list(
        filter(None, response.css("p.sku::text").re(r'(\d*)')))[0]


def skus(response, product):
    sizes_list = list(filter(None, [n.strip() for n in response.css(
        "div.sizebox-wrapper li::text").extract()]))
    avail_list = response.xpath(
        "//div[@class='sizebox-wrapper']//li/@data-qty").extract()

    for sizes in range(len(sizes_list)):
        if int(avail_list[sizes]):
            product['skus'].append({str(list(filter(None, response.css(
                "p.sku::text").re(r'(\d*)')))[0] + '_' + sizes_list[sizes]):
                {'color': response.css("img.has-tip[title]::attr(title)").extract()[0],
                 'currency': response.xpath("//script[@type='application/ld+json']/text()").re(r'priceCurrency\":\"(\w*)')[0],
                 'price': ''.join(response.xpath("//script[@type='application/ld+json']/text()").re(r'price":(\d)*(\.\d*)?')),
                 'size': sizes_list[sizes]}})
        else:
            product['skus'].append({str(list(filter(None, response.css(
                "p.sku::text").re(r'(\d*)')))[0] + '_' + sizes_list[sizes]):
                {'color': response.css("img.has-tip[title]::attr(title)").extract()[0],
                 'currency': response.xpath("//script[@type='application/ld+json']/text()").re(r'priceCurrency\":\"(\w*)')[0],
                 'price': ''.join(response.xpath("//script[@type='application/ld+json']/text()").re(r'price":(\d)*(\.\d*)?')),
                 'size': sizes_list[sizes], 'out_of_stock': 'true'}})


class OrsaySpider(CrawlSpider):
    name = 'orsay'
    allowed_domains = ['www.orsay.com']

    start_urls = [
        'http://www.orsay.com/de-de/collection.html',
        'http://www.orsay.com/de-de/accessoires.html']

    '''def parse(self, response):
        for site in response.xpath("//ul[@class='product-colors product-item-color']//a/@href").extract():
            yield scrapy.Request(site, callback=self.parseprod)
        for href in response.xpath("//a[@class='next i-next']/@href"):
            yield response.follow(href, self.parse)'''

    rules = (
        Rule(LinkExtractor(
        restrict_css="a.next.i-next")),
        Rule(LinkExtractor(
        restrict_css="ul.product-colors.product-item-color a"), callback="parseprod"),)
        

    def temp(self, response):
        yield {
            'url': response.url
        }
    def parseprod(self, response):
        product = Product()
        product['skus'] = []
        url(response, product)
        brand(response, product)
        care(response, product)
        description(response, product)
        image_urls(response, product)
        name(response, product)
        color_urls(response, product)
        retailer_sku(response, product)
        skus(response, product)
        yield product

# -*- coding: utf-8 -*-
import json
import re
from html import unescape

from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

from lornajane_crawler.items import LornajaneCrawlerItem


class LornajaneSpider(Spider):
    name = 'lornajane'
    start_urls = ['https://www.lornajane.sg/c-Shop-All?partitial=true&page=0', "https://www.lornajane.sg/c-Sale?partitial=true&page=0"]

    def parse(self, response):
        json_data = json.loads(response.text)
        product_html_data = json_data['products']
        product_html_data = unescape(product_html_data)
        product_html = Selector(text=product_html_data)
        product_detail_urls = product_html.xpath(
            "//div[@class='image-wrapper']/a/@href").extract()
        if product_detail_urls:
            for url in product_detail_urls:
                yield Request("https://www.lornajane.sg"+url, self.parse_item_details)
            page = int(re.findall(r'[\d]+', response.url)[0])
            page = page + 20
            yield Request("https://www.lornajane.sg/c-Shop-All?partitial=true&page=" + str(page))

    def parse_item_details(self, response):
        lornajane_item = LornajaneCrawlerItem()
        lornajane_item = ItemLoader(item=lornajane_item, response=response)
        lornajane_item.add_xpath(
            "name", "//div[contains(@class, 'pro-heading-sec')]/h1/text()")
        lornajane_item.add_value("brand", "Lorna Jane")
        lornajane_item.add_xpath(
            "product_id", "//div[contains(@class, 'pdt-content')]//p/text()", re=r'[\d]+')
        lornajane_item.add_value("url", response.url)
        description = response.xpath("//div[@class='product-desc'][1]//text()").extract()
        description = [desc.strip() for desc in description if desc.strip()!=""]
        lornajane_item.add_value(
            "description", description)
        lornajane_item.add_xpath(
            "image_urls", "//div[contains(@class, 'ScrollImages')]//img/@src")
        skus = dict()
        color_urls = [response.urljoin(color_url) for color_url in response.xpath(
            "//div[contains(@class, 'color-swatch')]/ul//a/@data-url").extract()]
        meta_dict = {
            "product": lornajane_item,
            "skus": skus,
            "color_urls": color_urls,
        }
        if color_urls:
            yield Request(color_urls[0], self.get_item_colors, meta=meta_dict, dont_filter=True)

    def get_item_colors(self, response):
        lornajane_item = response.meta['product']
        color_urls = response.meta['color_urls']
        skus = response.meta["skus"]
        colour = response.xpath(
            "//div[contains(@class, 'color-swatch')]/ul//a[contains(@class,'selected')]/@title").extract_first()
        available_sizes = response.xpath(
            "//div[@id='sizeWrap']//a[@class=' product-detail-swatch-btn']/text()").extract()
        price = response.xpath(
            "//div[@class='price']/text()").extract()[1]
        currency_code = response.xpath(
            "//span[@class='currency']/text()").extract_first()
        prev_price = response.xpath("//div[@class='price']/span[@style]/text()").extract_first()
        skus[colour] = {
            'colour': colour,
            'price': price,
            'currency_code': currency_code
        }
        if prev_price:
            skus[colour]["prev_price"] = prev_price
        if available_sizes:
            skus[colour]["available_sizes"] = available_sizes
        color_urls = color_urls[1:]
        if color_urls:
            meta_dict = {
                "product": lornajane_item,
                "skus": skus,
                "color_urls": color_urls,
            }
            yield Request(color_urls[0], self.get_item_colors, meta=meta_dict, dont_filter=True)
        else:
            lornajane_item.add_value("skus", skus)
            yield lornajane_item.load_item()

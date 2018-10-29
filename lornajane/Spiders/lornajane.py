# -*- coding: utf-8 -*-
from parsel import Selector
import json
import re
import scrapy
from scrapy.loader import ItemLoader
from lornajane_crawler.items import LornajaneCrawlerItem


class LornajaneSpider(scrapy.Spider):
    name = 'lornajane'
    allowed_domains = ['lornajane.sg']
    start_urls = ['https://www.lornajane.sg/c-Shop-All?partitial=true&page=0']

    def parse(self, response):
        json_data = json.loads(response.text)
        product_html_data = json_data['products']
        product_html_data = product_html_data.replace("&#034;", '"')
        product_html_data = product_html_data.replace("&lt;", '<')
        product_html_data = product_html_data.replace("&gt;", '>')
        product_html = Selector(product_html_data)
        product_detail_urls = product_html.xpath("//div[@class='image-wrapper']/a/@href").extract()
        if product_detail_urls:
            for url in product_detail_urls:
                yield scrapy.Request("https://www.lornajane.sg"+url, self.parse_item_details)
            page = int(re.findall(r'[\d]+', response.url)[0])
            page = page + 20
            yield scrapy.Request("https://www.lornajane.sg/c-Shop-All?partitial=true&page=" + str(page))

    def parse_item_details(self, response):
        lornajane_item = LornajaneCrawlerItem()
        lornajane_item = ItemLoader(item=lornajane_item, response=response)
        lornajane_item.add_xpath("name", "//div[contains(@class, 'pro-heading-sec')]/h1/text()")
        lornajane_item.add_value("brand", "Lorna Jane")
        lornajane_item.add_xpath("product_id", "//div[contains(@class, 'pdt-content')]//p/text()", re=r'[\d]+')
        lornajane_item.add_value("url", response.url)
        lornajane_item.add_xpath("description", "//div[contains(@class, 'pdt-content')]//p[3]/text()")
        lornajane_item.add_xpath("description", "//div[contains(@class, 'pdt-content')]//ul[1]//li/text()")
        lornajane_item.add_xpath("description", "//div[contains(@class, 'pdt-content')]//ul[2]//li/text()")
        lornajane_item.add_xpath("image_urls", "//div[contains(@class, 'ScrollImages')]//img/@src")
        color_scheme = dict()
        color_urls = [response.urljoin(color_url) for color_url in response.xpath("//div[contains(@class, 'color-swatch')]/ul//a/@data-url").extract()]
        meta_dict = {
            "product": lornajane_item,
            "color_scheme": color_scheme,
            "color_urls": color_urls,
        }
        yield scrapy.Request(color_urls[0], self.get_item_colors, meta=meta_dict, dont_filter=True)

    def get_item_colors(self, response):
        lornajane_item = response.meta['product']
        color_urls = response.meta['color_urls']
        color_scheme = response.meta["color_scheme"]
        color_name = response.xpath("//div[contains(@class, 'color-swatch')]/ul//a[contains(@class,'selected')]/@title").extract_first()
        available_sizes = response.xpath("//div[@id='sizeWrap']//a[@class=' product-detail-swatch-btn']/text()").extract()
        price = response.xpath("//div[contains(@class, 'pro-heading-sec')]/div/text()").extract()[1]
        currency_code = response.xpath("//span[@class='currency']/text()").extract_first()
        color_scheme[color_name] = {
            'color_name': color_name,
            'available_sizes': available_sizes,
            'price': price,
            'currency_code': currency_code
        }
        color_urls = color_urls[1:]
        if color_urls:
            meta_dict = {
                "product": lornajane_item,
                "color_scheme": color_scheme,
                "color_urls": color_urls,
            }
            yield scrapy.Request(color_urls[0], self.get_item_colors, meta=meta_dict, dont_filter=True)
        else:
            lornajane_item.add_value("colors", color_scheme)
            yield lornajane_item.load_item()

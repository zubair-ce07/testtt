# -*- coding: utf-8 -*-
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.request import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from carters.items import CartersProduct


class CartersSpider(CrawlSpider):
    name = "carters_spider"
    start_urls = (
        'http://www.carters.com/',
    )
    added_product_ids = set()
    rules = (
        Rule(SgmlLinkExtractor(deny=('outfits', 'oshkosh'),
                               restrict_xpaths=(".//*[@id='navigation']//li[contains(@class,'carters')]",
                                                "(.//a[contains(@class,'page-next')])[1]"))),
        Rule(SgmlLinkExtractor(deny=('outfits', 'oshkosh'),
                               restrict_xpaths=".//li[@class='grid-tile']//div[@class='product-image']"),
             callback="parse_product", process_links='filter_products_links')
    )

    def filter_products_links(self, links):
        filtered_links = []
        for link in links:
            if self.is_valid_link(link.url):
                filtered_links.append(link)
        return filtered_links

    def is_valid_link(self, link):
        product_id = link.split('.html', 1)[0].rsplit('/', 1)[1]
        if product_id in self.added_product_ids:
            return False
        self.added_product_ids.add(product_id)
        return True

    def parse_product(self, response):
        if not response.xpath(".//div[contains(@class,'product-detail-cols')]"):
            return None
        product = CartersProduct()
        product['category'] = self.product_category(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['price'] = self.get_price_digits(self.product_price(response))
        product['name'] = self.product_name(response)
        product['brand'] = self.product_brand(response)
        product['url_original'] = response.url
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['gender'] = self.detect_gender(response.url)
        product['skus'] = {}
        product['image_urls'] = set()
        product['image_urls'].add(self.product_image_url(response))
        product_variations_links = self.get_variations_links(response)
        if response.xpath(".//ul[contains(@class,'size')]/li[@class='selected']"):
            product['skus'].update(self.product_size_details(response))
        return self.get_next_variation(product, product_variations_links)

    def get_variations_links(self, response):
        product_variations_links = set(response.xpath(".//li[@class='emptyswatch']/a/@href").extract())
        current_color = self.get_line_from_node(response.xpath(
                                                ".//ul[contains(@class,'color')]/li[@class='selectedColor']"))
        colors = self.normaliz_string_list(response.xpath(".//ul[contains(@class,'color')]/li/*/text()").extract())
        for url in response.xpath(".//ul[contains(@class,'size')]/li[@class='emptyswatch']//a/@href").extract():
            for color in colors:
                product_variations_links.add(url.replace(current_color, color))
        return product_variations_links

    def get_next_variation(self, product, product_variations_links):
        if product_variations_links:
            return Request(product_variations_links.pop(), callback=self.parse_product_variation,
                           meta={"product": product, "product_variations_links": product_variations_links},
                           dont_filter=True)
        product['image_urls'] = list(product['image_urls'])
        return product

    def parse_product_variation(self, response):
        product = response.meta['product']
        product_variations_links = response.meta['product_variations_links']
        product['image_urls'].add(self.product_image_url(response))
        product['skus'].update(self.product_size_details(response))
        return self.get_next_variation(product, product_variations_links)

    def product_size_details(self, response):
        size_details = {}
        size_details['colour'] = self.product_color(response)
        size_details['size'] = self.product_size(response)
        price = self.product_price(response)
        size_details['price'] = self.get_price_digits(price)
        size_details['currency'] = self.get_currency_symbol(price)
        size_details['previous_prices'] = self.product_previous_prices(response)
        key = '{0}_{1}'.format(size_details['colour'], size_details['size'])
        return {key: size_details}

    def detect_gender(self, url):
        if 'boy' in url:
            return 'boys'
        if 'girl' in url:
            return 'girls'
        if 'neutral' in url:
            return 'unisex-kids'

    def product_previous_prices(self, node):
        price = self.get_line_from_node(node.xpath(".//span[@class='price-standard']"), deep=False)
        return [self.get_price_digits(price)] if price else []

    def product_price(self, node):
        return self.get_line_from_node(node.xpath(".//span[@itemprop='price']"))

    def product_size(self, node):
        return self.get_line_from_node(node.xpath(".//ul[@class='swatches size']//li[@class='selected']"))

    def product_color(self, node):
        return self.get_line_from_node(node.xpath(".//li[@class='selectedColor']"))

    def product_name(self, node):
        return self.get_line_from_node(node.xpath(".//h1[@itemprop='name']"))

    def product_category(self, node):
        return self.normaliz_string_list(
            node.xpath(".//ul[@class='clearfix']/li[not(@class) or @class ='last']//text()").extract())

    def product_retailer_sku(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//input[@data-product-id]/@data-product-id"))

    def product_brand(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//div[@class='primary-logo']/a/@title"))

    def product_image_url(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//a[contains(@class,'product-image')]/@href"))

    def get_care_index(self, node):
        return "-1" if node.xpath(".//ul[@class='customSpecs']/li[position() = last()]//*") else ""

    def product_description(self, node):
        care_index = self.get_care_index(node)
        return self.normaliz_string_list(node.xpath(
            ".//ul[@class='benefits']//text() | .//ul[@class='customSpecs']//li[position() != last(){0} ]//text()"
            .format(care_index)).extract())

    def product_care(self, node):
        care_index = self.get_care_index(node)
        return [self.get_line_from_node(
            node.xpath(".//ul[@class='customSpecs']//li[position() = last(){0}]".format(care_index)))]

    def get_price_digits(self, price):
        return int(re.sub('\D', '', price))

    def get_currency_symbol(self, price):
        return re.sub(r'[\d,.\s]', '', price)

    def normaliz_string_list(self, s_list):
        return [s.strip() for s in s_list if s.strip()]

    def get_text_from_node(self, node, deep=True):
        if not node:
            return []
        _text = './/text()'
        if not deep:
            _text = './text()'
        str_list = [x.strip() for x in node.xpath(_text).extract() if len(x.strip()) > 0]
        return str_list

    def get_line_from_node(self, node, deep=True, sep=' '):
        lines = self.get_text_from_node(node, deep)
        if not lines:
            return ''
        return sep.join(lines).strip()

    def get_attribute_value_from_node(self, node):
        value = node.extract()
        return value[0].strip() if value else ''

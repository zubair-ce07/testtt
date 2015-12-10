# -*- coding: utf-8 -*-
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.request import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from carters.items import CartersProduct


class CarterSpiderSpider(CrawlSpider):
    name = "carter_spider"
    start_urls = (
        'http://www.carters.com/',
    )
    categories_link = set()
    products_link = set()
    added_product_ids = set()

    rules = (
        Rule(SgmlLinkExtractor(
            allow='.com/carters-[a-z-0-9]+\?navID=header',
            deny='outfits',
            restrict_xpaths=".//*[@id='navigation']/nav/ul/li//div[@class='subnav-categories']"),
            callback="parse_products_links", process_links="process_category_links"))

    def get_next_product(self):
        if self.products_link:
            return Request(self.products_link.pop(), callback=self.parse_product)

    def process_category_links(self, links):
        processed_links = set()
        for link in links:
            link.url = "{0}?cgid={1}&startRow=0&sz=all".format(link.url.rsplit('?', 1)[0],
                                                               link.url.rsplit('/', 1)[1].rsplit('?', 1)[0])
            processed_links.add(link)
        return processed_links

    def parse_products_links(self, response):
        for link in response.xpath(".//li[@class='grid-tile']//div[@class='product-image']/a/@href").extract():
            if 'http' not in link:
                link = 'http://www.carters.com{0}'.format(link)
            if self.is_valid_link(link):
                self.products_link.add(link)
        return self.get_next_product()

    def parse_product(self, response):
        product = CartersProduct()
        product['category'] = self.product_category(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['price'] = self.get_price_digits(self.product_price(response))
        product['name'] = self.product_name(response)
        product['brand'] = self.product_brand(response)
        product['url_original'] = response.url
        product['image_urls'] = self.product_image_urls(response)
        product['description'], product['care'] = self.product_description_and_care(response)
        product['gender'] = self.detect_gender(response.url)
        product['skus'] = {}
        product_variations_link = set(response.xpath(".//li[@class='emptyswatch']/a/@href").extract())
        return self.get_next_size(product, product_variations_link)

    def get_next_size(self, product, product_variations_link):
        if product_variations_link:
            yield Request(product_variations_link.pop(), callback=self.parse_product_variation,
                          meta={"product": product, "product_variations_link": product_variations_link},
                          dont_filter=True)
            return
        yield product
        yield self.get_next_product()

    def parse_product_variation(self, response):
        product = response.meta['product']
        product_variations_link = response.meta['product_variations_link']
        size_details = {}
        size_details['colour'] = self.product_color(response)
        size_details['size'] = self.product_size(response)
        price = self.product_price(response)
        size_details['price'] = self.get_price_digits(price)
        size_details['currency'] = self.get_currency_symbol(price)
        size_details['previous_prices'] = self.product_previous_prices(response)
        product['skus']['{0}_{1}'.format(size_details['colour'], size_details['size'])] = size_details
        return self.get_next_size(product, product_variations_link)

    def is_valid_link(self, link):
        if 'outfits' not in link:
            product_id = link.split('.html', 1)[0].rsplit('/', 1)[1]
            if product_id not in self.added_product_ids:
                self.added_product_ids.add(product_id)
                return True
        return False

    def detect_gender(self, url):
        if 'boy' in url:
            return 'boys'
        if 'girl' in url:
            return 'girls'
        if 'neutral' in url:
            return 'unisex-kids'
        return 'unknown gender'

    def product_previous_prices(self, node):
        return [
            self.get_price_digits(self.get_line_from_node(node.xpath(".//span[@class='price-standard']"), deep=False))]

    def product_price(self, node):
        return self.get_line_from_node(node.xpath(".//span[@itemprop='price']"))

    def product_size(self, node):
        return self.get_line_from_node(node.xpath(".//ul[@class='swatches size']//li[@class='selected']"))

    def product_color(self, node):
        return self.get_line_from_node(node.xpath(".//li[@class='selectedColor']"))

    def product_name(self, node):
        return self.get_line_from_node(node.xpath(".//h1[@itemprop='name']"))

    def product_category(self, node):
        return self.normaliz_string_list(node.xpath(".//ul[@class='clearfix']/li[position()>2]//text()").extract())

    def product_retailer_sku(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//input[@data-product-id]/@data-product-id"))

    def product_brand(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//div[@class='primary-logo']/a/@title"))

    def product_image_urls(self, node):
        return node.xpath(".//div[contains(@class,'product-image-container')]//img/@src").extract()

    def product_description_and_care(self, node):
        if node.xpath(".//ul[@class='customSpecs']//*[position() = last() and  @class]"):
            care_index = "-1"
        else:
            care_index = ""
        return self.normaliz_string_list(node.xpath(
            ".//ul[@class='benefits']//text() | .//ul[@class='customSpecs']//*[position() != last(){0} ]//text()"
            .format(care_index)).extract()), \
               [self.get_line_from_node(
                   node.xpath(".//ul[@class='customSpecs']//*[position() = last(){0}]".format(care_index)))]

    def get_price_digits(self, price):
        return re.sub('\D', '', price)

    def get_currency_symbol(self, price):
        return re.sub(r'[\d,.\s]', '', price)

    def normaliz_string_list(self, s_list):
        return [s for s in s_list if s.strip()]

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


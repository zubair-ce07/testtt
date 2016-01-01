import re
import yaml
import urlparse

from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import FormRequest

from topshop.items import TopshopItem


class ChichiSpider(CrawlSpider):
    name = 'topshop_crawl'
    allowed_domains = ['topshop.com']
    start_urls = ('http://www.topshop.com/',)
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=(".//*[@id='nav_catalog_menu']/li[position() < 8]/a",)),
             callback='request_next_page'),
        Rule(SgmlLinkExtractor(restrict_xpaths=".//*[@class='product']/li[@class='product_image']"),
             callback='parse_product')
    )

    def request_next_page(self, response):
        for request in self.parse(response):
            yield request

        url = self.get_attribute_value_from_node(response.xpath("(.//li[@class='show_next']//a)[1]/@href"))
        if url:
            params = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            url = url.split('?', 1)[0]
            required_keys = ['dimSelected', 'catalogId', 'storeId', 'langId']
            required_params = {key: params[key] for key in required_keys }
            yield FormRequest(url, formdata=required_params, dont_filter=True,
                              callback=self.request_next_page, method='POST')

    def parse_product(self, response):
        product_data = self.product_data(response)
        if not product_data:
            return
        product = TopshopItem()
        product['url_original'] = response.url
        product['gender'] = 'women'
        product['retailer'] = 'topshop'
        product['spider_name'] = self.name
        product['retailer_sku'] = product_data['code']
        product['name'] = product_data['name']
        product['brand'] = self.product_brand(product['name'])
        product['price'] = self.get_price_digits(product_data['prices']['now'])
        product['image_urls'] = self.product_images_urls(product_data['thumbnails'], product_data['code'])
        product['category'] = self.product_categories(response)
        product['description'] = self.product_description(response)
        product['market'] = self.product_market(response)
        product['currency'] = self.product_currency(response)
        product['skus'] = self.product_variations(product_data, product['price'], product['currency'])
        return product

    def product_variations(self, product_data, price, currency):
        variations = {}
        variation_template = {"colour": product_data["colour"], "price": price, "currency": currency}

        if product_data['prices'].get('was'):
            variation_template['previous_price'] = self.get_price_digits(product_data['prices']['was'])

        for item in product_data['items']:
            variation = {}
            variation.update(variation_template)
            variation['size'] = item['size']
            variations[item['sku']] = variation

        return variations

    def product_data(self, node):
        product_data = self.get_line_from_node(node.xpath(".//*[@id='product_column_3_espot_2']/following-sibling::*"))
        return yaml.load(re.sub(':', ': ', ' '.join(product_data.split('=', 1)[-1].split())))

    def product_retailer_sku(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//input[@name='productId']/@value"))

    def product_description(self, node):
        return self.get_text_from_node(node.xpath(".//div[@class='product_description']"), deep=False)

    def product_name(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//*[@property='og:description']/@content"))

    def product_categories(self, node):
        return self.get_text_from_node(node.xpath(".//*[@id='nav_breadcrumb']//div/*[@itemprop='url']"))

    def product_color(self, node):
        return self.get_line_from_node(node.xpath(".//*[@class='product_colour']/span"))

    def product_price(self, node):
        return self.get_line_from_node(node.xpath(
            ".//*[@class='product_price']/span | .//*[contains(@class,'now_price')]/span"))

    def product_images_urls(self, thumbnail_suffixes, product_code):
        image_urls = ["http://media.topshop.com/wcsstore/TopShop/images/catalog/{0}_large.jpg".format(product_code)]

        for suffix in thumbnail_suffixes[1:]:
            image_urls.append(
                "http://media.topshop.com/wcsstore/TopShop/images/catalog/{0}{1}_large.jpg".format(
                    product_code, suffix))

        return image_urls

    def product_brand(self, name):
        brand = name.lower().split(' by ')
        return brand[1] if len(brand) > 1 else ''

    def product_market(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//*[@id='region_select']/div/@class")).split(' ', 1)[1]

    def product_currency(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//*[@property='og:price:currency']/@content"))

    def get_price_digits(self, price):
        return int(re.sub('\\D', '', price))

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
        if value:
            return value[0].strip()
        return ''
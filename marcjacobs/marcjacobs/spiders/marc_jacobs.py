# -*- coding: utf-8 -*-
import re
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request

from marcjacobs.items import MarcjacobsItem


class MarcJacobsSpider(CrawlSpider):
    name = "marc_jacobs"
    genders = ['boys', 'girls', 'mens', 'men', 'womens', 'women']
    possible_one_sizes = ['OS', '1SZ', 'O/S']
    nav_bar_path = ".//*[@id='navigation']//div[@class='level-2']"
    pagination_path = ".//div[@data-grid-url]"
    products_path = ".//div[contains(@class,'product-tile')]"

    start_urls = (
        'http://www.marcjacobs.com/',
    )

    rules = (

        Rule(SgmlLinkExtractor(restrict_xpaths=nav_bar_path),),
        Rule(SgmlLinkExtractor(restrict_xpaths= pagination_path, tags=('div',), attrs=('data-grid-url',)),
             process_links="process_next_page_url"),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_path),
             callback='parse_product')
    )

    def process_next_page_url(self, links):
        links[0].url = re.sub('(&)?format=page-element(&)?', '', links[0].url)
        return links

    def parse_product(self, response):
        product = MarcjacobsItem()
        product['url_original'] = response.url
        product['retailer'] = 'MarcJacob'
        product['spider_name'] = self.name
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['name'] = self.product_name(response)
        product['brand'] = self.product_brand(response)
        product['price'] = self.product_price(response)
        product['currency'] = self.product_currency(response)
        product['category'] = self.product_categories(response)
        product['gender'] = self.product_gender(product['category'])
        product['description'] = self.product_description(response)
        product['skus'] = {}
        product['image_urls'] = []

        images_data_urls = [self.product_images_data_url(response)]
        variation_links = self.product_variation_links(response)
        color_variations = self.color_variations(response)

        return self.get_next_color_variation(color_variations, variation_links, product, images_data_urls)

    def get_next_color_variation(self, color_variations, variation_links, product, images_data_urls):
        if color_variations:
            return Request(color_variations.pop(),
                           meta={"color_variations": color_variations,
                                 "variation_links": variation_links,
                                 "product": product,
                                 "images_data_urls": images_data_urls},
                           callback=self.parse_color_variation)

        return self.get_next_variation(variation_links, product, images_data_urls)

    def parse_color_variation(self, response):
        variation_links = response.meta['variation_links']
        color_variations = response.meta['color_variations']
        product = response.meta['product']
        images_data_urls = response.meta['images_data_urls']

        variation_links += self.product_variation_links(response)
        images_data_urls.append(self.product_images_data_url(response))
        return self.get_next_color_variation(color_variations, variation_links, product, images_data_urls)

    def get_next_variation(self, variation_links, product, images_data_urls):
        if variation_links:
            return Request(variation_links.pop(),
                           meta={"variation_links": variation_links,
                                 "product": product,
                                 "images_data_urls": images_data_urls},
                           callback=self.parse_variation, dont_filter=True)

        return self.get_next_image_data(product, images_data_urls)

    def parse_variation(self, response):
        variation_links = response.meta['variation_links']
        product = response.meta['product']
        images_data_urls = response.meta['images_data_urls']

        sku = {}
        sku['color'] = self.variation_color(response)
        sku['currency'] = self.variation_currency(response)
        sku['price'] = self.variation_price(response)
        sku['out_of_stock'] = self.variation_out_of_stock(response)
        sku['size'] = self.variation_size(response)

        if sku['size'] in self.possible_one_sizes:
            sku['size'] = "One Size"

        previous_price = self.variation_previous_price(response)
        if previous_price and previous_price != sku['price']:
            sku['previous_price'] = previous_price

        product['skus'].update({"{0}_{1}".format(sku['color'], sku['size']): sku})
        return self.get_next_variation(variation_links, product, images_data_urls)

    def get_next_image_data(self, product, images_data_urls):
        if images_data_urls:
            return Request(images_data_urls.pop(),
                           meta={'product': product, "images_data_urls": images_data_urls},
                           callback=self.parse_images_data)

        return product

    def parse_images_data(self, response):
        product = response.meta['product']
        images_data_urls = response.meta['images_data_urls']

        images_data = json.loads(re.sub(r'\\', '', response.body.split('(', 1)[-1].rsplit(')', 1)[0]))
        for image_data in images_data['items']:
            product['image_urls'].append(image_data['src'])

        return self.get_next_image_data(product, images_data_urls)

    def color_variations(self, response):
        return response.xpath(".//*[contains(@class,'emptyswatch')]//a/@href").extract()

    def product_variation_links(self, node):
        variation_links = node.xpath(".//*[@id='va-size']//option[not(contains(text(),'Select'))]/@value").extract()
        ajax_variation_links = []

        for variation_link in variation_links:
            ajax_variation_links.append("{0}&format=ajax".format(variation_link))

        return ajax_variation_links

    def product_gender(self, categories):
        categories = [category.lower() for category in categories]
        gender = [gender for gender in self.genders if gender in categories]
        return gender[0] if gender else 'unisex'

    def product_name(self, node):
        return self.get_line_from_node(node.xpath(".//*[@itemprop='name']"))

    def product_retailer_sku(self, node):
        return self.get_line_from_node(node.xpath(".//*[@itemprop='productID']"))

    def product_brand(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//*[@property='og:brand']/@content"))

    def product_price(self, node):
        return self.get_price_digits(
            self.get_line_from_node(node.xpath(".//*[@id='product-content']//*[@class='price-sales']")))

    def product_currency(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//*[@property='product:price:currency']/@content"))

    def product_categories(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//*[@name='categorytype']/@value")).split('-')

    def product_description(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//*[@property='og:description']/@content"))

    def product_images_data_url(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//*[@data-images]/@data-images"))

    def variation_color(self, node):
        return self.get_line_from_node(node.xpath(".//*[@itemprop='color']"))

    def variation_size(self, node):
        return self.get_line_from_node(node.xpath(".//*[@id='va-size']//option[@selected]"))

    def variation_price(self, node):
        return self.get_price_digits(self.get_attribute_value_from_node(node.xpath(".//*[@itemprop='price']/@content")))

    def variation_previous_price(self, node):
        previous_price = self.get_line_from_node(node.xpath("(.//*[@class='price-standard'])[1]"), deep=False)
        return self.get_price_digits(previous_price) if previous_price else ''

    def variation_currency(self, node):
        return self.get_currency(self.get_attribute_value_from_node(node.xpath(".//*[@itemprop='price']/@content")))

    def variation_out_of_stock(self, node):
        return True if node.xpath(".//*[@class='quantity-na']") else False

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

    def get_price_digits(self, price):
        return re.sub('[^0-9^-]', '', price)

    def get_currency(self, price):
        return re.sub(r'[\d,.\s]', '', price)


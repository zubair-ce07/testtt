from marcJacobsWebCrawler.items import MarcJacobsProductItem, MarcJacobsSizeItem, \
    MarcJacobsVariantionItem
from scrapy.loader import ItemLoader
from scrapy import Spider
import urllib
import copy
import json
import re


class MarcJacobsSpider(Spider):
    name = 'marcjacobsspider'
    start_urls = ['http://www.marcjacobs.com/']
    marc_jacobs_css = {'locale': ".current-country a span::text",
                       'image_url': ".product-images::attr(data-images)",
                       'display_color_name': ".Color .selected a::text",
                       'title': "meta[property$=':title']::attr(content)",
                       'brand': "meta[property$=':brand']::attr(content)",
                       'price': "meta[property$=':amount']::attr(content)",
                       'product_link': ".product-page-link::attr(data-href)",
                       'variation_links': ".Color .emptyswatch a::attr(href)",
                       'size_names': "#va-size option:not([value=''])::text",
                       'currency': "meta[property$=':currency']::attr(content)",
                       'menu_links': "#navigation .mobile-hidden a::attr(href)",
                       'description': "meta[property$=':description']::attr(content)",
                       'original_price': ".product-detail-wrapper .price-standard::text",
                       'discounted_price': ".product-detail-wrapper .price-sales::text", }

    def __init__(self, **kwargs):
        super(MarcJacobsSpider, self).__init__(**kwargs)
        self.whitespace_remover = re.compile(r'\s+')
        self.seen_skus = set()

    def parse(self, response):
        menu_links = response.css(self.marc_jacobs_css['menu_links']).extract()
        for link in menu_links:
            yield response.follow(link, self.parse_product)

    def parse_product(self, response):
        product_links = response.css(self.marc_jacobs_css['product_link']).extract()
        for product_link in product_links:
            store_keeping_unit = product_link.split('.html')[0].split('/')[-1]
            if store_keeping_unit in self.seen_skus:
                continue

            self.seen_skus.add(store_keeping_unit)
            yield response.follow(product_link, self.parse_variation)

    def parse_variation(self, response):
        variation_links = response.css(self.marc_jacobs_css['variation_links']).extract()
        if variation_links:
            next_color_link = variation_links.pop()
            yield response.follow(next_color_link, self.collect_responses,
                                  meta={'responses': [response], 'color_links': variation_links})
        else:
            yield self.parse_responses([response])

    def collect_responses(self, response):
        color_links = response.meta['color_links']
        responses = response.meta['responses']
        responses.append(response)

        if color_links:
            next_color_link = color_links.pop()
            yield response.follow(next_color_link, self.collect_responses,
                                  meta={'responses': responses, 'color_links': color_links})
        else:
            yield self.parse_responses(responses)

    def parse_responses(self, responses):
        product = self.load_product_item(responses[0])
        for response in responses:
            product = self.add_variation(response, product)
        return product

    def add_variation(self, response, product):
        variation_item = self.add_size(response, self.load_variation_item(response))
        product.setdefault('variations', []).append(variation_item)
        return product

    def add_size(self, response, variation_item):
        size_items = self.load_size_items(response)
        variation_item.setdefault('sizes', []).append(size_items)
        return variation_item

    def load_size_items(self, response):
        loaded_sizes = list()
        size_item = self.load_size_item(response)
        size = self.remove_whitespaces(copy.deepcopy(size_item))

        size_names = response.css(self.marc_jacobs_css['size_names']).extract()
        size_names = map(lambda size_name: self.whitespace_remover.sub('', size_name), size_names)

        for size_name in size_names:
            loaded_sizes.append({'size_name': size_name, 'price': size['price'],
                                 'is_discounted': size['is_discounted'],
                                 'discounted_price': size['discounted_price']})
        return loaded_sizes

    def load_size_item(self, response):
        is_discounted = self.is_discounted(response)
        price_css = self.generate_price_css(is_discounted)
        size_items = ItemLoader(item=MarcJacobsSizeItem(), response=response)
        size_items.add_css('price', price_css[0])
        size_items.add_value('is_discounted', is_discounted)
        size_items.add_css('discounted_price', price_css[-1])
        return size_items.load_item()

    def load_variation_item(self, response):
        json_url = response.css(self.marc_jacobs_css['image_url']).extract()
        image_urls = self.extract_image_urls(json_url[0])
        variation_item = ItemLoader(item=MarcJacobsVariantionItem(), response=response)
        variation_item.add_value('image_urls', image_urls)
        variation_item.add_css('display_color_name', self.marc_jacobs_css['display_color_name'])
        return variation_item.load_item()

    def load_product_item(self, response):
        product_item = ItemLoader(item=MarcJacobsProductItem(), response=response)
        product_item.add_value('product_url', response.url)
        product_item.add_css('brand', self.marc_jacobs_css['brand'])
        product_item.add_css('title', self.marc_jacobs_css['title'])
        product_item.add_css('locale', self.marc_jacobs_css['locale'])
        product_item.add_css('locale', self.marc_jacobs_css['locale'])
        product_item.add_css('currency', self.marc_jacobs_css['currency'])
        product_item.add_css('description', self.marc_jacobs_css['description'])
        product_item.add_value('store_keeping_unit', response.url.split('.html')[0].split('/')[-1])
        return product_item.load_item()

    def extract_image_urls(self, url):
        loaded_json = self.load_json(url)
        image_urls = []

        for item in loaded_json['items']:
            image_urls.append(item['src'])
        return image_urls

    def load_json(self, url):
        url = urllib.urlopen(url)
        json_data = url.read()
        purify_data = json_data.split('handleJSON(')[1].split(');')[0]
        return json.loads(purify_data)

    def remove_whitespaces(self, item):
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = self.whitespace_remover.sub('', value)
        return item

    def is_discounted(self, response):
        if response.css(self.marc_jacobs_css['original_price']):
            return True
        return False

    def generate_price_css(self, is_discounted):
        if is_discounted:
            return [self.marc_jacobs_css['original_price'],
                    self.marc_jacobs_css['discounted_price']]
        else:
            return [self.marc_jacobs_css['price']]

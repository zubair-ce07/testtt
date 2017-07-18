from aldoWebCrawler.items import AldoProductItem, AldoSizeItem, AldoVariantionItem
from scrapy.loader import ItemLoader
from scrapy import Spider
import copy


class AldoSpider(Spider):
    name = 'aldospider'
    start_urls = ['https://www.aldoshoes.com/ca/en/']
    aldo_css = {'brand': "meta[property$=':site']::attr(content)",
                'title': "meta[property$=':title']::attr(content)",
                'locale': "meta[property$=':locale']::attr(content)",
                'size_names': "#PdpProductSizeSelectorOpts li::text",
                'image_urls': "meta[property$=':image']::attr(content)",
                'currency': "meta[property$=':currency']::attr(content)",
                'product_link': ".c-product-tile__link-product::attr(href)",
                'description': "meta[property$=':description']::attr(content)",
                'menu_links': ".c-navigation-mega-menu button+ul a::attr(href)",
                'original_price': ".c-product-price__formatted-price--original::text",
                'display_color_name': ".c-product-option__label-current-selection::text",
                'discounted_price': ".c-product-price__formatted-price--is-reduced::text",
                'variation_links': ".o-style-option__list-item a:not([class*=is-checked])::attr(href)",
                'price': "meta[property$=':amount']::attr(content)", }

    def __init__(self, **kwargs):
        super(AldoSpider, self).__init__(**kwargs)
        self.seen_skus = set()

    def parse(self, response):
        menu_links = response.css(self.aldo_css['menu_links']).extract()
        for link in menu_links:
            yield response.follow(link, self.parse_product)

    def parse_product(self, response):
        product_links = response.css(self.aldo_css['product_link']).extract()
        for product_link in product_links:
            store_keeping_unit = product_link.split('/')[-1].split('-')[0]
            if store_keeping_unit in self.seen_skus:
                continue

            self.seen_skus.add(store_keeping_unit)
            yield response.follow(product_link, self.parse_variation)

    def parse_variation(self, response):
        variation_links = response.css(self.aldo_css['variation_links']).extract()
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
        size = copy.deepcopy(size_item)

        size_names = response.css(self.aldo_css['size_names']).extract()
        for size_name in size_names:
            loaded_sizes.append({'size_name': size_name, 'price': size['price'],
                                 'is_discounted': size['is_discounted'],
                                 'discounted_price': size['discounted_price']})
        return loaded_sizes

    def load_size_item(self, response):
        is_discounted = self.is_discounted(response)
        price_css = self.generate_price_css(is_discounted)
        size_items = ItemLoader(item=AldoSizeItem(), response=response)
        size_items.add_css('price', price_css[0])
        size_items.add_value('is_discounted', is_discounted)
        size_items.add_css('discounted_price', price_css[-1])
        return size_items.load_item()

    def load_variation_item(self, response):
        variation_item = ItemLoader(item=AldoVariantionItem(), response=response)
        variation_item.add_css('image_urls', self.aldo_css['image_urls'])
        variation_item.add_css('display_color_name', self.aldo_css['display_color_name'])
        return variation_item.load_item()

    def load_product_item(self, response):
        product_item = ItemLoader(item=AldoProductItem(), response=response)
        product_item.add_value('product_url', response.url)
        product_item.add_css('brand', self.aldo_css['brand'])
        product_item.add_css('title', self.aldo_css['title'])
        product_item.add_css('locale', self.aldo_css['locale'])
        product_item.add_css('locale', self.aldo_css['locale'])
        product_item.add_css('currency', self.aldo_css['currency'])
        product_item.add_css('description', self.aldo_css['description'])
        product_item.add_value('store_keeping_unit', response.url.split('/')[-1].split('-')[0])
        return product_item.load_item()

    def is_discounted(self, response):
        if response.css(self.aldo_css['discounted_price']):
            return True
        return False

    def generate_price_css(self, is_discounted):
        if is_discounted:
            return [self.aldo_css['original_price'], self.aldo_css['discounted_price']]
        else:
            return [self.aldo_css['price']]

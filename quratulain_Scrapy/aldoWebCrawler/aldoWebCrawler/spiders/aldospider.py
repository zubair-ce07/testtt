from aldoWebCrawler.items import AldoProductItem, AldoSizeItem, AldoVariantionItem
from scrapy.loader import ItemLoader
from scrapy.contrib.spiders import CrawlSpider


class AldoSpider(CrawlSpider):
    name = 'aldospider'
    start_urls = ['https://www.aldoshoes.com/ca/en/']
    aldo_css = {'product_link': '.c-product-tile__link-product::attr(href)',
                'menu_links': '.c-navigation-mega-menu button+ul a::attr(href)',
                'variation_links': '.o-style-option__list-item a:not([class*=is-checked])::attr(href)',
                'size_name': '#PdpProductSizeSelectorOpts li::text',
                'image_urls': 'meta[property$=\':image\']::attr(content)',
                'display_color_name': '.c-product-option__label-current-selection::text',
                'brand': 'meta[property$=\':site\']::attr(content)',
                'title': 'meta[property$=\':title\']::attr(content)',
                'locale': 'meta[property$=\':locale\']::attr(content)',
                'currency': 'meta[property$=\':currency\']::attr(content)',
                'description': 'meta[property$=\':description\']::attr(content)',
                'original_price': '.c-product-price__formatted-price--original::text',
                'discounted_price': '.c-product-price__formatted-price--is-reduced::text',
                'price': 'meta[property$=\':amount\']::attr(content)', }

    def __init__(self, **kwargs):
        super(AldoSpider, self).__init__(**kwargs)
        self.products = set()

    def parse(self, response):
        menu_links = response.css(self.aldo_css['menu_links']).extract()
        for link in menu_links:
            yield response.follow(link, self.parse_product)

    def parse_product(self, response):
        product_links = response.css(self.aldo_css['product_link']).extract()
        for product_link in product_links:
            store_keeping_unit = product_link.split('/')[-1].split('-')[0]
            if store_keeping_unit in self.products:
                continue
            self.products.add(store_keeping_unit)
            yield response.follow(product_link, self.parse_variation)

    def parse_variation(self, response):
        variation_links = response.css(self.aldo_css['variation_links']).extract()
        variation_item = self.add_variation(response)
        product = self.load_product_item(response, variation_item['variations'])

        for link in variation_links:
            request = response.follow(link, self.add_variation, meta={'product_item': product})
            print(request)
            yield request

    def add_variation(self, response):
        product = response.meta.get('product_item', AldoProductItem())
        variation_item = self.load_variation_item(response, self.load_size_items(response))
        product.setdefault('variations', []).append(variation_item)
        return product

    def load_size_items(self, response):
        sizes = response.css(self.aldo_css['size_name']).extract()
        loaded_sizes = list()
        for size in sizes:
            loaded_sizes.append(self.load_size_item(response, size))
        return loaded_sizes

    def load_size_item(self, response, size):
        is_discounted = self.is_discounted(response)
        price_css = self.generate_price_css(is_discounted)
        size_items = ItemLoader(item=AldoSizeItem(), response=response)
        size_items.add_value('is_discounted', is_discounted)
        size_items.add_value('size_name', size)
        size_items.add_css('price', price_css[0])
        size_items.add_css('discounted_price', price_css[-1])
        return size_items.load_item()

    def load_variation_item(self, response, size_items):
        variation_items = ItemLoader(item=AldoVariantionItem(), response=response)
        variation_items.add_value('sizes', size_items)
        variation_items.add_css('image_urls', self.aldo_css['image_urls'])
        variation_items.add_css('display_color_name', self.aldo_css['display_color_name'])
        return variation_items.load_item()

    def load_product_item(self, response, variation_items):
        product_items = ItemLoader(item=AldoProductItem(), response=response)
        product_items.add_value('product_url', response.url)
        product_items.add_value('variations', variation_items)
        product_items.add_value('store_keeping_unit', response.url.split('/')[-1])
        product_items.add_css('brand', self.aldo_css['brand'])
        product_items.add_css('title', self.aldo_css['title'])
        product_items.add_css('locale', self.aldo_css['locale'])
        product_items.add_css('locale', self.aldo_css['locale'])
        product_items.add_css('currency', self.aldo_css['currency'])
        product_items.add_css('description', self.aldo_css['description'])
        return product_items.load_item()

    def is_discounted(self, response):
        if response.css(self.aldo_css['discounted_price']):
            return True
        return False

    def generate_price_css(self, is_discounted):
        if is_discounted:
            return [self.aldo_css['original_price'], self.aldo_css['discounted_price']]
        else:
            return [self.aldo_css['price']]

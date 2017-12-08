import urllib.parse
import json
import re

from scrapy import Request, Spider
from slugify import slugify

from FirstScrapyTask.items import ShopBopItem


class ShopBopSpider(Spider):
    ignore_links = [
        'All Clothing', 'All Shoes', 'All Bags', 'All Jewelry & Accessories',
        'What\'s New', 'Gifts', 'Designers', 'Sale', 'Discover', 'What\'s New By Category',
        'Shop By', 'Names to Know', 'Sale by Category', 'New Designers'
    ]
    base_url = 'https://www.shopbop.com'
    name = 'shopbop'
    start_urls = ['https://www.shopbop.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {'FirstScrapyTask.pipelines.ValidationPipeline': 100},
        'DOWNLOADER_MIDDLEWARES': {'FirstScrapyTask.middlewares.UserAgentMiddleware': 500,
                                   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None}
    }

    def parse(self, response):
        for parent_category in response.css('.nested-navigation-section'):
            parent = parent_category.css('.sub-navigation-header::text').extract_first()
            if parent in self.ignore_links or not parent:
                continue
            for child_category in parent_category.css('.sub-navigation-list li'):
                url = child_category.css('::attr(href)').extract_first()
                child = child_category.css('.sub-navigation-list-item-link-text::text').extract_first().strip()
                if child not in self.ignore_links:
                    product_category = '/'.join(category.strip().lower() for category in (parent, child))
                    meta = {'product_category': product_category}
                    yield self.make_request(url,meta)

    def make_request(self, url, meta):
        url = urllib.parse.urljoin(self.base_url, url)
        return Request(url=url, callback=self.parse_product_urls, meta=meta)

    def parse_product_urls(self, response):
        products = response.css('.products.flex-flow-inline .photo::attr(href)').extract()
        for url in products:
            url = urllib.parse.urljoin(self.base_url, url)
            yield Request(url=url, callback=self.parse_product, meta=response.meta)
        pagination = response.css('.next::attr(data-next-link)').extract_first()
        if pagination:
            yield self.make_request(pagination, response.meta)

    def parse_product(self, response):
        product_json = json.loads(response.css('script').re_first('{"product.+'))
        product = ShopBopItem()
        product['category'] = response.meta['product_category']
        product['title'] = response.css('div#product-title::text').extract_first()
        product['product_url'] = response.url
        product['locale'] = response.css('body#top::attr(data-locale)').extract_first()
        product['currency'] = response.css('body#top::attr(data-currency)').extract_first()
        product['description'] = self.get_description(product_json)
        product['product_id'] = product_json['product']['styleNumber']
        product['variations'] = {}
        colors_sizes = []
        for color in product_json['product']['styleColors']:
            image_urls = [image_url['url'] for image_url in color['images']]
            for color_size in color['styleColorSizes']:
                colors_sizes.append({
                    'size': color_size['size']['label'],
                    'is_available': color_size['inStock'],
                    'price': color['prices'][0]['retailAmount'],
                    'discounted_price': color['prices'][0]['saleAmount'],
                    'is_discounted': color['prices'][0]['onSale']
                })
            product['variations'][slugify(color['color']['label'])] = {
                'code': color['color']['code'],
                'image_urls': image_urls,
                'sizes': colors_sizes
            }
            colors_sizes = []
        yield product

    def get_description(self, product_json):
        description = product_json['product']['longDescription'].split('<br>')
        return [re.sub('<.*?>', ' ', row) for row in description if row != '']

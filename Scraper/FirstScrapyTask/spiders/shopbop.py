import urllib.parse
import json

from scrapy import Request, Spider
from slugify import slugify

from FirstScrapyTask.items import ShopBopItem


class ShopBopSpider(Spider):

    required_links = ['Clothing', 'Shoes', 'Bags', 'Accessories', 'Jewelry']
    ignore_links = ['All Clothing', 'All Shoes', 'All Bags', 'All Jewelry & Accessories']
    base_url = 'https://www.shopbop.com'
    name = 'shopbop'
    start_urls = ['https://www.shopbop.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        for parent_category in response.css('.nested-navigation-section'):
            parent = parent_category.css('.sub-navigation-header::text').extract_first()
            if parent not in self.required_links:
                continue
            else:
                for child_category in parent_category.css('.sub-navigation-list li'):
                    url = child_category.css('a::attr(href)').extract_first()
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
            yield Request(url=url, callback=self.parse_products, meta=response.meta)
        pagination = response.css('.next::attr(data-next-link)').extract_first()
        if pagination:
            yield self.make_request(pagination, response.meta)

    def parse_products(self, response):
        product_json = json.loads(response.css('script').re_first('{"product.+'))
        product = ShopBopItem()
        product['category'] = response.meta['product_category']
        product['title'] = response.css('div#product-title::text').extract_first()
        product['product_url'] = response.url
        product['locale'] = response.css('body#top::attr(data-locale)').extract_first()
        product['currency'] = response.css('body#top::attr(data-currency)').extract_first()
        product['description'] = list(filter(None, product_json['product']['longDescription'].split('<br>')))
        product['product_id'] = product_json['product']['styleNumber']
        product['variations'] = {}
        colors, colors_sizes, colors_prices = [], [], []
        variation_item = []
        for color in product_json['product']['styleColors']:
            colors.append(color['color']['label'])
            colors_sizes.append(color['styleColorSizes'])
            colors_prices.append(color['prices'])
            image_urls = [image_url['url'] for image_url in color['images']]
            variation_item.append({'code': color['color']['code'], 'image_urls': image_urls, 'sizes': []})

        variation_item = self.create_variation_item(colors_sizes, colors_prices, variation_item)
        for index,color in enumerate(colors):
            product['variations'][slugify(color)] = variation_item[index]
        yield product

    def create_variation_item(self, colors_sizes, colors_prices, variation_item):
        final_prices = []
        for per_color_price in colors_prices:
            for price in per_color_price:
                final_prices.append({
                    'is_discounted': price['onSale'],
                    'sale_price': price['retailAmount'],
                    'discounted_price': price['saleAmount'] if price['onSale'] else ''
                })
        for index,per_color_size in enumerate(colors_sizes):
            for size in per_color_size:
                variation_item[index]['sizes'].append({
                    'size': size['size']['label'],
                    'is_available': size['inStock'] ,
                    'price': final_prices[index]['sale_price'],
                    'discounted_price': final_prices[index]['discounted_price'],
                    'is_discounted': final_prices[index]['is_discounted']
                })
        return variation_item

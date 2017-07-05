import json
import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from training_spider.items import TrainingSpiderItem


class AdidasSpider(CrawlSpider):
    name = 'adidas'
    start_urls = [
        'http://shop.adidas.com.my/'
    ]
    rules = (Rule(LinkExtractor(restrict_css='.mm-item .cateNaviLink')),
             Rule(LinkExtractor(restrict_css='.toolbar-bottom .next')),
             Rule(LinkExtractor(restrict_css='.products-grid .product-image'), follow=True,
                  callback='parse_products'))

    def parse_products(self, response):
        product_id = response.css('#pdpMain script::text').re_first(r'p = \'(.*)\'')
        model = response.css('#pdpMain script::text').re_first(r'model = \'(.*)\'')

        item = TrainingSpiderItem()
        item['product_id'] = product_id
        item['product_name'] = response.css('.productname .name::text').extract_first()
        item['product_url'] = response.url
        item['country'] = 'my'
        item['currency'] = \
            response.css('.productinfo .price::text').extract_first().strip('\t\n\r')[0:2]
        main_image = 'https:{}'. \
            format(response.css('.product-image img::attr(src)').extract_first())
        images_path = 'https:{}'.format(response.css('#pdpMain script::text'
                                                     ).re_first(r'swatchpath = \'(.*)\''))
        product_colors_url = \
            'http://sp-ad-media.s3.amazonaws.com/json/my/prd/{}.json'.format(model)
        return Request(self.get_product_size_quanties_url(response, product_id, model),
                       callback=self.parse_product_size_quantity,
                       meta={'product_colors_url': product_colors_url,
                             'images_path': images_path,
                             'main_image': main_image, 'item': item})

    def parse_product_size_quantity(self, response):
        product_size_quantity = json.loads(json.loads(response.text).get('qtys')).get('options')
        return Request(
            response.meta.get('product_colors_url'), callback=self.parse_product_colors,
            meta={'product_size_quantity': product_size_quantity,
                  'item': response.meta.get('item'),
                  'images_path': response.meta.get('images_path'),
                  'main_image': response.meta.get('main_image')})

    def parse_product_colors(self, response):
        item = response.meta.get('item')
        item['variations'] = self.get_variations(json.loads(response.text),
                                                 response.meta.get('product_size_quantity'),
                                                 response.meta.get('images_path'),
                                                 response.meta.get('main_image'))
        yield item

    def get_product_size_quanties_url(self, response, product_id, model):
        url = response.css('#pdpMain script::text').re_first(r'inventoryFetchUrl = \'(.*)\'')
        curret_time = response.css('.page script::text').re_first(r'curretTime = \"(.*)\"')
        store_id = response.css('#pdpMain script::text').re_first(r'storeId = \'(.*)\'')

        return 'http:{}?pid={}&model={}&span={}&store={}'. \
            format(url, product_id, model, curret_time, store_id)

    def get_variations(self, response, product_size_quantity, images_path, main_image):
        variations = []
        for product_color in response.get('result').get('adi_my').get('color').values():
            color_code = product_color.get('code')
            color_slug = '{}_{}'.format(product_color.get('label'), color_code)
            sizes = self.get_sizes(product_color, product_size_quantity, color_code)
            images_url = self.get_images_url(product_color, images_path)
            main_image = main_image.replace(re.search(r'.*/(.*)_.*_.*', main_image).group(1),
                                            product_color.get('articlenumber'))
            variations.append({color_slug: {'sizes': sizes,
                                            'images_url': images_url,
                                            'main_image': main_image}})
        return variations

    def get_sizes(self, product_color, product_size_quantity, color_code):
        sizes = []
        for size in product_color.get('size').values():
            name = size.get('label')
            size_code = size.get('code')
            is_available = False
            if int(float(product_size_quantity.get(color_code).get(size_code).get('qty'))):
                is_available = True
            price = size.get('price')
            sale_price = size.get('special_price') or '-'
            sizes.append({'name': name, 'is_available': is_available,
                          'price': price, 'sale_price': sale_price})
        return sizes

    def get_images_url(self, product_color, images_path):
        images_relative_urls = product_color.get('image').get('swatch')[0].split('|')
        return ['{}{}'.format(images_path, url) for url in images_relative_urls]

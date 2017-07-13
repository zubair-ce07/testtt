import json
import re
from urllib.parse import urljoin

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from training_spider.items import TrainingSpiderItem


class AdidasSpider(CrawlSpider):
    name = 'adidas'
    start_urls = [
        'http://shop.adidas.com.my/'
    ]

    rules = (Rule(LinkExtractor(restrict_css='.cateNaviLink')),
             Rule(LinkExtractor(restrict_css='.toolbar-bottom .next')),
             Rule(LinkExtractor(restrict_css='.product-image'), follow=True,
                  callback='parse_products'))

    product_id_re = re.compile(r'p = \'(.*)\'')
    model_re = re.compile(r'model = \'(.*)\'')
    size_url_re = re.compile(r'inventoryFetchUrl = \'(.*)\'')
    curret_time_re = re.compile(r'curretTime = \"(.*)\"')
    store_id_re = re.compile(r'storeId = \'(.*)\'')
    images_path_re = re.compile(r'swatchpath = \'(.*)\'')

    def parse_products(self, response):
        raw_script = response.css('#pdpMain script:last-child::text')
        product_id = raw_script.re_first(self.product_id_re)

        item = TrainingSpiderItem()
        item['product_id'] = product_id
        item['product_name'] = response.css('.name::text').extract_first()
        item['product_url'] = response.url
        item['country'] = 'my'
        item['currency'] = response.css('.price::text').extract_first().strip()[0:2]
        main_image = response.css('.product-image img::attr(src)').extract_first()
        main_image = response.urljoin(main_image)
        images_path = raw_script.re_first(self.images_path_re)
        images_path = response.urljoin(images_path)
        product_colors_url = raw_script.re_first(r'jQuery.getJSON\(\'(.*)\',')
        product_colors_url = response.urljoin(product_colors_url)
        url = self.get_product_size_quantities_url(response, raw_script, product_id)
        return Request(url, callback=self.parse_product_size_quantity,
                       meta={'item': item,
                             'main_image': main_image,
                             'images_path': images_path,
                             'product_colors_url': product_colors_url})

    def parse_product_size_quantity(self, response):
        product_size_quantity = json.loads(
            json.loads(response.text).get('qtys', {})
        ).get('options')
        product_color_url = response.meta.get('product_colors_url')
        return Request(
            product_color_url, callback=self.parse_product_colors,
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

    def get_product_size_quantities_url(self, html_response, raw_script, product_id):
        url = raw_script.re_first(self.size_url_re)
        url = html_response.urljoin(url)
        model = raw_script.re_first(self.model_re)
        curret_time = raw_script.re_first(self.curret_time_re)
        store_id = raw_script.re_first(self.store_id_re)

        return '{}?pid={}&model={}&span={}&store={}'. \
            format(url, product_id, model, curret_time, store_id)

    def get_variations(self, colors_json, product_size_quantity, images_path, main_image):
        variations = []
        colors = colors_json.get('result', {}).get('adi_my', {}).get('color', {}).values()
        for color in colors:
            color_code = color.get('code')
            color_slug = '{}_{}'.format(color.get('label'), color_code)
            sizes = self.get_sizes(color, product_size_quantity, color_code)
            images_url = self.get_images_url(color, images_path)
            article_number = main_image.split('/')[-1].split('_')[0]
            main_image = main_image.replace(article_number, color.get('articlenumber'))
            variations.append({color_slug: {'sizes': sizes,
                                            'images_url': images_url,
                                            'main_image': main_image}})
        return variations

    def get_sizes(self, product_color, product_size_quantity, color_code):
        sizes = []
        for size in product_color.get('size', {}).values():
            name = size.get('label')
            size_code = size.get('code')
            is_available = False
            size_quantity = product_size_quantity.get(color_code, {}) \
                .get(size_code, {}).get('qty')
            if size_quantity and int(float(size_quantity)):
                is_available = True
            price = size.get('price')
            sale_price = size.get('special_price') or '-'
            sizes.append({'name': name, 'is_available': is_available,
                          'price': price, 'sale_price': sale_price})
        return sizes

    def get_images_url(self, product_color, images_path):
        image_urls = []
        images_relative_urls = product_color.get('image', {}).get('swatch', [])
        if images_relative_urls:
            images_relative_urls = images_relative_urls[0].split('|')
            image_urls = [urljoin(images_path, url) for url in images_relative_urls]
        return image_urls

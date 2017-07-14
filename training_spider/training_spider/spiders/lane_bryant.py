import json
import re
from urllib.parse import urljoin

from scrapy import Request, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from training_spider.items import TrainingSpiderItem


class AdidasSpider(CrawlSpider):
    name = 'lane_prepairing'
    start_urls = [
        'http://www.lanebryant.com'
    ]

    rules = (
        Rule(
            LinkExtractor(restrict_css='.mar-nav .grid__item'),
            follow=True,
            callback='parse_pagination'
        ),
        Rule(
            LinkExtractor(restrict_css='.mar-prd-product-item'),
            follow=True,
            callback='parse_products'
        )
    )

    url_params_re = re.compile(r'\?N=\d+&No=\d+')

    def parse_pagination(self, response):
        next_page_url = None
        try:
            page_contents = json.loads(response.text)
            product_grid = page_contents.get('product_grid', {}).get('html_content')
            if product_grid:
                selector = Selector(text=product_grid)
                products_urls = selector.css(
                    '.mar-prd-item-image-container::attr(href)').extract()
                for url in products_urls:
                    yield Request(response.urljoin(url), callback=self.parse_products)

                next_page_url = page_contents.get('nextPageUrl')
                if not next_page_url:
                    return
        except ValueError:
            endpoints = json.loads(response.css('#endpoints::text').extract_first())
            endpoints = endpoints.get('data', {}).get('endpoints', {})
            next_page_path = endpoints.get('plpData')
            url_params = response.css(
                '#nextPageUrlOld::attr(value)').re_first(self.url_params_re)

            if not url_params or not next_page_path:
                return
            next_page_url = urljoin(next_page_path, url_params)

        yield Request(response.urljoin(next_page_url), callback=self.parse_pagination)

    def parse_products(self, response):
        product_id = response.css('#pdpProductID::attr(value)').extract_first()
        item = TrainingSpiderItem()
        item['product_id'] = product_id
        item['product_name'] = response.css('.mar-product-title::text').extract_first()
        item['product_url'] = response.url
        item['country'] = 'United States'

        product = json.loads(response.css('#pdpInitialData::text').extract_first())
        product = product['pdpDetail']['product'][0]
        server_url = product['scene7_params']['server_url']
        server_url = response.urljoin(server_url)
        account_id = product['scene7_params']['account_id']
        sizes = product['all_available_sizes'][0]['values']
        sizes = [self.get_size(sku, sizes) for sku in product['skus']]
        colors = product['all_available_colors'][0]['values']
        colors = [self.get_colors(response, server_url,
                                  account_id, sizes, color) for color in colors]
        return self.request_image_json_urls(colors, item, server_url)

    def request_image_json_urls(self, colors, item, server_url, variations=None):
        if colors:
            color = colors.pop(0)
            images_json_url = color.get('images_josn_urls')
            return Request(images_json_url, callback=self.parse_images_json_urls,
                           meta={'color': color,
                                 'item': item,
                                 'remaining_colors': colors,
                                 'server_url': server_url,
                                 'variations': variations})
        else:
            item['variations'] = variations
            return item

    def parse_images_json_urls(self, response):
        meta = response.meta
        color = meta['color']
        server_url = meta['server_url']
        variations = meta['variations'] or []

        images_json = json.loads(response.css('::text').re_first(r'{.*}'))
        images_json = images_json['set']['item']
        if isinstance(images_json, list):
            image_urls = [
                urljoin(server_url, img_json['i']['n']) for img_json in images_json
            ]
        else:
            image_urls = urljoin(server_url, images_json['i']['n'])

        variation_key = '{}_{}'.format(color['color_id'], color['color_name'])
        variation_value = {'sizes': color.get('sizes'),
                           'main_images': color.get('main_image'),
                           'image_urls': image_urls}

        variations.append({variation_key: variation_value})

        return self.request_image_json_urls(
            meta.get('remaining_colors'), meta.get('item'), server_url, variations)

    def get_colors(self, html_response, server_url, account_id, sizes, color):
        color_id = color.get('id')
        color_name = color.get('name')
        images_josn_urls = '{}{}/{}?req=set,json&id={}'.format(
            server_url, account_id, color.get('imageset'), color_id)
        main_image = html_response.urljoin(color.get('sku_image'))

        size_colors = []
        for size in sizes:
            size_key = list(size.keys())[0]
            if color_id in size_key:
                size_colors.append(size.get(size_key))

        return {'color_id': color_id,
                'color_name': color_name,
                'sizes': size_colors,
                'images_josn_urls': images_josn_urls,
                'main_image': main_image}

    def get_size(self, sku, sizes):
        for size in sizes:
            if size['id'] == sku['size']:
                name = size['value']
                prices = sku.get('prices', {})

                size_key = sku.get('color', 'color')
                size_value = {
                    'name': name,
                    'is_available': True,
                    'price': prices.get('list_price'),
                    'sale_price': prices.get('sale_price') or '-'
                }
                return {size_key: size_value}

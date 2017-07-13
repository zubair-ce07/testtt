import json
from urllib.parse import urljoin

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from training_spider.items import TrainingSpiderItem


class AdidasSpider(CrawlSpider):
    name = 'lanebryant'
    start_urls = [
        'http://www.lanebryant.com'
    ]
    rules = (Rule(LinkExtractor(restrict_css='.mar-nav .grid__item'),
                  callback='parse_pagination', follow=True),
             Rule(LinkExtractor(restrict_css='.mar-prd-product-item'), follow=True,
                  callback='parse_products'))

    def parse_pagination(self, response):
        try:
            page_contents = json.loads(response.text)
            product_grid = HtmlResponse(
                url='abc', body=page_contents.get('product_grid', {}).get('html_content'),
                encoding='utf-8')
            products_urls = product_grid.css(
                '.mar-prd-item-image-container::attr(href)').extract()
            for url in products_urls:
                yield Request(response.urljoin(url), callback=self.parse_products)
            
            next_page_url = page_contents.get('nextPageUrl')
            yield Request(response.urljoin(next_page_url), callback=self.parse_pagination)
        except ValueError:
            next_page_path = json.loads(
                response.css('#endpoints::text').extract_first()
            ).get('data', {}).get('endpoints', {}).get('plpData')
            url_params = response.css(
                '#nextPageUrlOld::attr(value)').re_first('\?N=\d+&No=\d+')

            next_page_url = urljoin(next_page_path, url_params)
            yield Request(response.urljoin(next_page_url), callback=self.parse_pagination)

    def parse_products(self, response):
        product_id = response.css('#pdpProductID::attr(value)').extract_first()
        item = TrainingSpiderItem()
        item['product_id'] = product_id
        item['product_name'] = response.css('.mar-product-title::text').extract_first()
        item['product_url'] = response.url
        item['country'] = 'United States'

        product = json.loads(
            response.css('#pdpInitialData::text').extract_first()
        ).get('pdpDetail', {}).get('product', [{}])[0]
        server_url = product.get('scene7_params', {}).get('server_url')
        server_url = response.urljoin(server_url)
        account_id = product.get('scene7_params', {}).get('account_id')
        skus = self.get_skus(product.get('skus', {}))
        sizes = self.get_sizes(product.get('all_available_sizes', [{}])[0], skus)
        colors = [self.get_colors(response ,color, sizes, server_url, account_id)
                  for color in product.get('all_available_colors', [{}])[0].get('values')]
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
        color = meta.get('color')
        server_url = meta.get('server_url')
        variations = meta.get('variations') or []

        images_json = json.loads(response.css('::text').re_first(r'{.*}'))\
            .get('set', {}).get('item')
        if isinstance(images_json, list):
            image_urls = [urljoin(server_url, img_json.get('i', {}).get('n'))
                          for img_json in images_json]
        else:
            image_urls = urljoin(server_url, images_json.get('i', {}).get('n'))
        
        variations.append({'{}_{}'.format(color.get('color_id'), color.get('color_name')):
                               {'sizes': color.get('sizes'),
                                'main_images': color.get('main_image'),
                                'image_urls': image_urls}
                           })
        return self.request_image_json_urls(
            meta.get('remaining_colors'), meta.get('item'), server_url, variations)

    def get_colors(self, html_response, color, sizes, server_url, account_id):
        color_id = color.get('id')
        return {'color_id': color_id, 'color_name': color.get('name'),
                'sizes': [size.get(key) for size in sizes
                          for key in size.keys() if color.get('id') in key],
                'images_josn_urls': '{}{}/{}?req=set,json&id={}'.format(
                    server_url, account_id, color.get('imageset'), color_id),
                'main_image': html_response.urljoin(color.get('sku_image'))}

    def get_sizes(self, sizes, skus):
        return [
            {key: {'name': size.get('value'), 'is_available': True,
                   'price': sku.get(key, {}).get('price'),
                   'sale_price': sku.get(key, {}).get('sale_price')}
             }
            for size in sizes.get('values')
            for sku in skus for key in sku.keys() if size.get('id') in key]

    def get_skus(self, skus):
        return [{'{}_{}'.format(sku.get('color'), sku.get('size')):
                  {'price':  sku.get('prices', {}).get('list_price'),
                 'sale_price': sku.get('prices', {}).get('sale_price') or '-'}
                 }
                for sku in skus]

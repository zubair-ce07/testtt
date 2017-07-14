import json
import re

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from marc_jacobs.items import MarcJacobsItem


class MarcJacobsSpider(CrawlSpider):
    name = 'marc_jacobs'
    start_urls = [
        'https://www.marcjacobs.com/'
    ]
    rules = (Rule(LinkExtractor(restrict_css='.mobile-hidden .menu-vertical')),
             Rule(LinkExtractor(restrict_css='.infinite-scroll-placeholder', tags=('div',),
                                attrs=('data-grid-url',))),
             Rule(LinkExtractor(restrict_css='.product-page-link', tags=('div',),
                                attrs=('data-href',)),
                  callback='parse_products', follow=True))

    def parse_products(self, response):
        item = MarcJacobsItem()
        item['url'] = response.url
        item['name'] = response.css('#name::attr(value)').extract_first()
        item['brand'] = response.css('#brand::attr(value)').extract_first()
        item['description'] = self.get_description(response)
        product_colors = [{'color_name': color.css('::text').extract_first(),
                           'color_url': color.css('::attr(href)').extract_first()}
                          for color in response.css('.color-swatch a')]
        color_requests = []
        for product_color in product_colors:
            url = product_color.get('color_url')
            color_name = product_color.get('color_name')
            request = Request(url, callback=self.parse_product_colors)
            color_requests.append({'request': request, 'color_name': color_name})

        return self.request_product_color(color_requests, item)

    def request_product_color(self, color_requests, item,
                              skus=None, img_colors_json_urls=None):
        if color_requests:
            color_request = color_requests.pop(0)
            color_name = color_request.get('color_name')
            request = color_request.get('request')
            request.meta['color_name'] = color_name
            request.meta['color_requests'] = color_requests
            request.meta['item'] = item
            request.meta['skus'] = skus
            request.meta['img_colors_json_urls'] = img_colors_json_urls

            return request
        else:
            item['skus'] = skus
            image_color_requests = []
            for img_json_url in img_colors_json_urls:
                url = img_json_url.get('url')
                color_name = img_json_url.get('color_name')
                request = Request(url, callback=self.parse_image_colors)
                image_color_requests.append({'request': request, 'color_name': color_name})

            return self.request_image_colours(image_color_requests, item)

    def parse_product_colors(self, response):
        meta = response.meta
        color_name = meta.get('color_name')
        skus = self.get_skus(response, meta, color_name)

        url = response.css('.product-images::attr(data-images)').extract_first()
        img_colors_json_urls = meta.get('img_colors_json_urls') or []
        img_colors_json_urls.append({'color_name': color_name, 'url': url})

        return self.request_product_color(
            meta.get('color_requests'), meta.get('item'), skus, img_colors_json_urls)

    def request_image_colours(self, image_color_requests, item, image_urls=None):
        if image_color_requests:
            img_json = image_color_requests.pop(0)
            color_name = img_json.get('color_name')
            request = img_json.get('request')
            request.meta['color_name'] = color_name
            request.meta['item'] = item
            request.meta['image_color_requests'] = image_color_requests
            request.meta['image_urls'] = image_urls

            return request
        else:
            item['image_urls'] = image_urls
            return item

    def parse_image_colors(self, response):
        meta = response.meta
        image_urls = meta.get('image_urls') or []

        image_colors_json = json.loads(re.search(r'{.*}', response.text).group(0))
        image_urls.append({
            meta.get('color_name'): [img_url['src'] for img_url in image_colors_json['items']]
        })

        return self.request_image_colours(
            meta.get('image_color_requests'), meta.get('item'), image_urls)

    def get_skus(self, response, meta, color_name):
        skus = meta.get('skus') or []
        previous_price = response.css('.product-price span::text'). \
                             extract_first().strip() or '-'
        currency, price = response.css(
            'span[itemprop="price"]::attr(content)').extract_first().split()
        sizes = response.css('#Quantity option::text').extract()
        sizes = list(filter(None, [size.strip() for size in sizes])) or ['-']

        for size in sizes:
            skus.append({'sku_id': '{}_{}'.format(color_name, size),
                         'color': color_name,
                         'size': size,
                         'previous_price': previous_price,
                         'price': price,
                         'currency': currency})
        return skus

    def get_description(self, response):
        description = response.css('.tab-content::text').extract()
        return list(filter(None, [desc.strip() for desc in description]))

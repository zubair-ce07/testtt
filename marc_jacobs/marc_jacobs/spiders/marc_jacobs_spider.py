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
    rules = (Rule(LinkExtractor(restrict_css='#navigation li.mobile-hidden .menu-vertical li',
                                )),
             Rule(LinkExtractor(restrict_css='.infinite-scroll-placeholder', tags=('div',),
                                attrs=('data-grid-url',))),
             Rule(LinkExtractor(restrict_css='.product-page-link', tags=('div',),
                                attrs=('data-href',)), callback='parse_products', follow=True))

    def parse_products(self, response):
        item = MarcJacobsItem()
        item['url'] = response.url
        item['name'] = response.css('#name::attr(value)').extract_first()
        item['brand'] = response.css('#brand::attr(value)').extract_first()
        item['description'] = self.get_description(response)
        product_colors = [{'color_name': color.css('::text').extract_first(),
                           'color_url': color.css('::attr(href)').extract_first()}
                          for color in response.css('.value .swatches .color-swatch a')]
        return self.request_product_color(product_colors, item)

    def request_product_color(self, product_colors, item, skus=None, img_colors_json_urls=None):
        if product_colors:
            color = product_colors.pop(0)
            return Request(
                color.get('color_url'), callback=self.parse_product_colors,
                meta={'img_colors_json_urls': img_colors_json_urls, 'item': item, 'skus': skus,
                      'product_colors': product_colors, 'color_name': color.get('color_name')})
        else:
            item['skus'] = skus
            return self.request_image_colours(img_colors_json_urls, item)

    def parse_product_colors(self, response):
        meta = response.meta
        color = meta.get('color_name')
        skus = meta.get('skus') or []
        img_colors_json_urls = meta.get('img_colors_json_urls') or []
        previous_price = response.css('#product-content .product-price span::text').\
                             extract_first().strip('\r\t\n') or '-'
        currency, price = response.css(
            '#product-content span[itemprop="price"]::attr(content)').extract_first().split()
        for size in self.get_sizes(response):
            skus.append({'sku_id': '{}_{}'.format(color, size),
                         'color': color,
                         'size': size,
                         'previous_price': previous_price,
                         'price': price,
                         'currency': currency})
        img_colors_json_urls.append({
            'color': color,
            'url': response.css('.product-images::attr(data-images)').extract_first()})
        return self.request_product_color(
            meta.get('product_colors'), meta.get('item'), skus, img_colors_json_urls)

    def request_image_colours(self, img_colors_json_urls, item, image_urls=None):
        if img_colors_json_urls:
            json_url = img_colors_json_urls.pop(0)
            return Request(
                json_url.get('url'), callback=self.parse_image_colors,
                meta={'color': json_url.get('color'), 'image_urls': image_urls,
                      'item': item, 'img_colors_json_urls': img_colors_json_urls})
        else:
            item['image_urls'] = image_urls
            return item

    def parse_image_colors(self, response):
        meta = response.meta
        image_urls = meta.get('image_urls') or []

        image_colors_json = json.loads(re.search(r'{.*}', response.text).group(0))
        image_urls.append(
            {meta.get('color'): [img_url['src'] for img_url in image_colors_json['items']]})

        return self.request_image_colours(
            meta.get('img_colors_json_urls'), meta.get('item'), image_urls)

    def get_description(self, response):
        description = response.css('.tabs-menu .tab-content::text').extract()
        return [desc.strip() for desc in description if desc.strip()]

    def get_sizes(self, response):
        sizes = response.css('#va-size option::text').extract()
        return [size.strip() for size in sizes[1:] if size.strip()] or ['-']

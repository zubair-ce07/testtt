
import os
import re
import json
from string import ascii_uppercase

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler_tasks.items import GenericProduct


class SkechersSpider(CrawlSpider):
    name = 'skechers'
    allowed_domains = ['skechers.com']
    start_urls = ['https://www.skechers.com/en-gb']
    rules = (
        Rule(LinkExtractor(allow=('\w+/style/[0-9]+/\w+',)), callback='parse_product'),
        Rule(LinkExtractor(allow=('/all(\?technology)?(\?brand)?', '\?genders=', '/?-?shoes', 'performance$')),
             follow=True),
    )
    gender_dict = {
        'M': 'men',
        'W': 'women',
        'B': 'boy',
        'G': 'girl'
    }

    def parse_product(self, response):
        parent = response.css('section div.product-details')
        skx_obj = self.read_skx_style_script_tag(parent)

        item = GenericProduct()
        item['brand'] = ''
        item['market'] = ''
        item['category'] = ''
        item['merch_info'] = []
        item['url'] = response.url
        item['product_id'] = skx_obj['stylecode']
        item['name'] = skx_obj['name']
        item['description'] = skx_obj['shortdescription']
        item['gender'] = SkechersSpider.gender_dict.get(skx_obj['gender'], 'other')
        item['care'] = parent.css('div.product-info div.toggle-description li::text').extract()

        currency = parent.css('div.price-bar meta[itemprop="price"]::attr(content)').extract_first()
        item['skus'] = self.create_skus(skx_obj, currency)

        main_image_url = parent.css('a#magic-zoom-main-image::attr(href)').extract_first()
        item['image_urls'] = self.create_image_urls(main_image_url, skx_obj['products'])

        return item

    def read_skx_style_script_tag(self, parent):
        raw_text = parent.xpath("//script[contains(., 'Skx.style =')]/text()")
        pattern = re.compile(r"Skx.style =.*[$}]")
        raw_obj = raw_text.re(pattern)[0].replace('Skx.style = ', '')
        return json.loads(raw_obj)

    def create_skus(self, skx_obj, currency):
        skus = {}
        for product in skx_obj['products']:
            available_sizes = [size for size in product['sizes'] if size['instock']]
            for size in available_sizes:
                skus[size['upccode']] = {
                    'currency': currency,
                    'size': size['size'],
                    'price': size['price'],
                    'colour': product['color']
                }
        return skus

    def create_image_urls(self, image_url, products):
        image_urls = [image_url]
        url, ext = os.path.splitext(image_url)
        image_count = next((p['numimages'] for p in products if p['image'] in image_url), 0)
        for i in range(1, image_count):
            image_urls.append(url + '_' + ascii_uppercase[i] + ext)
        return image_urls

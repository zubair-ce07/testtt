
import os
import re
import json
from string import ascii_uppercase

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.spiders import Spider
from crawler_tasks.items import GenericProduct


class SkechersSpider(Spider):
    name = 'skechers'
    allowed_domains = ['skechers.com']
    gender_names = {
        'M': 'men',
        'W': 'women',
        'B': 'boy',
        'G': 'girl'
    }

    def start_requests(self):
        products_listing_urls = [
            'https://www.skechers.com/en-gb/api/html/products/styles/listing?genders=M',
            'https://www.skechers.com/en-gb/api/html/products/styles/listing?genders=W',
            'https://www.skechers.com/en-gb/api/html/products/styles/listing?genders=G,B'
        ]
        for url in products_listing_urls:
            yield Request(url, callback=self.parse_product_list, meta={'scraped_count': 0})

    def parse_product_list(self, response):
        base_url = 'https://www.skechers.com'
        json_response = json.loads(response.text)
        total_products = json_response['totalRows']

        products_html = HtmlResponse(url='', body=json_response['stylesHtml'].encode('ascii', 'ignore'))
        product_urls = products_html.css('div.product a.prodImg-wrapper::attr(href)').extract()
        for url in product_urls:
            yield Request(base_url + url, callback=self.parse_product)

        scraped_count = response.meta['scraped_count'] + len(product_urls)
        if scraped_count < total_products:
            next_url = response.request.url.split('&bookmark')[0] + '&bookmark=' + json_response['bookmark']
            yield Request(next_url, callback=self.parse_product_list, meta={'scraped_count': scraped_count})

    def parse_product(self, response):
        parent = response.css('section div.product-details')
        skx_obj = self.create_obj_from_skx_stlye(parent)

        item = GenericProduct()
        item['brand'] = ''
        item['market'] = ''
        item['category'] = ''
        item['merch_info'] = []
        item['url'] = response.url
        item['product_id'] = skx_obj['stylecode']
        item['name'] = skx_obj['name']
        item['description'] = skx_obj['shortdescription']
        item['gender'] = SkechersSpider.gender_names.get(skx_obj['gender'], 'other')
        item['care'] = parent.css('div.product-info div.toggle-description li::text').extract()

        currency = parent.css('div.price-bar meta[itemprop="priceCurrency"]::attr(content)').extract_first()
        item['skus'] = self.create_skus(skx_obj, currency)

        main_image_url = parent.css('a#magic-zoom-main-image::attr(href)').extract_first()
        item['image_urls'] = self.create_image_urls(main_image_url, skx_obj['products'])

        return item

    def create_obj_from_skx_stlye(self, parent):
        pattern = re.compile(r"Skx.style =.*[$}]")
        raw_text = parent.xpath("//script[contains(., 'Skx.style =')]/text()").re(pattern)[0]
        return json.loads(raw_text.replace('Skx.style = ', ''))

    def create_skus(self, skx_obj, currency):
        skus = {}
        for product in skx_obj['products']:
            for size in product['sizes']:
                skus[size['upccode']] = {
                    'currency': currency,
                    'colour': product['color'],
                    'size': size['size'],
                    'price': size['price'],
                    'discount_price': size['discountprice']
                }
        return skus

    def create_image_urls(self, image_url, products):
        image_urls = [image_url]
        url, ext = os.path.splitext(image_url)
        image_count = next((p['numimages'] for p in products if p['image'] in image_url), 0)
        if ext == '.gif':
            ext = '.jpg'
        for i in range(1, image_count):
            image_urls.append(url + '_' + ascii_uppercase[i] + ext)
        return image_urls

import re
import json
import urllib.parse
import string

import scrapy

from FirstScrapyTask.items import SkechersItem


class SkechersSpider(scrapy.Spider):

    max_image_count = 6
    image_url_t = '{}_{}.jpg'
    base_url = 'https://www.skechers.com'
    gender_mapping = {'M': 'Men', 'W': 'Women', 'B': 'Boys','G': 'Girls', 'U': 'Men/Women/Accessories'}
    api_mapping = {'wom': 'https://www.skechers.com/en-us/api/html/products/styles/listing?genders=W&bookmark=',
                   'men': 'https://www.skechers.com/en-us/api/html/products/styles/listing?genders=M&bookmark=',
                   'kids': 'https://www.skechers.com/en-us/api/html/products/styles/listing?genders=G,B&bookmark=',
                   'apparel': 'https://www.skechers.com/en-us/api/html/products/apparel?bookmark=',
                   'socks': 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/socks&bookmark=',
                   'bags': 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/bags&bookmark=',
                   'watches': 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/watches&bookmark=',
                   'sunglasses': 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/sunglasses&bookmark=',
                   'care-products': 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/care-products&bookmark='}

    name = 'skechers'
    start_urls = ['https://www.skechers.com/en-us/accessories?category=/accessories/watches',
                  'https://www.skechers.com/en-us/accessories?category=/accessories/bags',
                  'https://www.skechers.com/en-us/accessories?category=/accessories/sunglasses',
                  'https://www.skechers.com/en-us/accessories?category=/accessories/care-products',
                  'https://www.skechers.com/en-us/accessories?category=/accessories/socks',
                  'https://www.skechers.com/en-us/apparel',
                  'https://www.skechers.com/en-us/kids/all',
                  'https://www.skechers.com/en-us/women/all',
                  'https://www.skechers.com/en-us/men/all']
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        product_urls = response.css('div::attr(data-clicked-style-url)').extract()
        api = self.get_api(response)
        bookmark = self.get_bookmarks(response)

        for url in product_urls:
            url = urllib.parse.urljoin(self.base_url , url)
            request = scrapy.Request(url=url, callback=self.parse_style_info)
            yield request

        if bookmark:
            parse_result = urllib.parse.urlparse(api)
            url = urllib.parse.urlunparse((parse_result.scheme, parse_result.netloc, parse_result.path, '', parse_result.query + bookmark, ''))
            request = scrapy.Request(url=url, callback=self.parse_style_urls , meta={'api' : api})
            yield request

    def parse_style_urls(self, response):
        api = response.meta['api']
        response_result = json.loads(response.text)
        product_urls = re.findall('\/en-us.*\s' ,response_result['stylesHtml'])

        for url in product_urls:
            url = urllib.parse.urljoin(self.base_url , re.search('/en.*?(?=")' , url).group(0))
            request = scrapy.Request(url=url, callback=self.parse_style_info)
            yield request

        if response_result['bookmark']:
            parse_result = urllib.parse.urlparse(api)
            url = urllib.parse.urlunparse((parse_result.scheme, parse_result.netloc, parse_result.path, '', parse_result.query + response_result['bookmark'], ''))
            request = scrapy.Request(url=url, callback=self.parse_style_urls , meta={'api' : api})
            yield request

    def parse_style_info(self, response):

        product = SkechersItem()
        product_style_id = response.css('.pull-right.product-label::text').extract_first()
        product_style_color = response.css('.js-color-code::text').extract_first()
        product_id_number = int(re.search('\d.*(?= )', product_style_id).group(0))

        product['name'] = response.css('.product-title::text').extract_first()
        product['url'] = response.url
        product['gender'] = self.get_gender(response)
        product['brand'] = 'Skechers'
        product['description'] = response.css('.toggle-expand.toggle-description div::text').extract_first()
        product['product_id'] = '{}{}'.format(product_style_id, product_style_color)
        product['category'] = product['name'].split('-')
        product['category'].append(product['gender'])
        product['image_urls'] = self.get_image_urls(response)
        product['skus'] = {}
        price_final = response.css('.price-final::text').extract_first()
        currency = price_final[0]
        color = response.css('.product-label.js-color::text').extract_first()

        sizes_info = self.get_size(response)
        for size in sizes_info:
            product['skus'][str(product_id_number)] = {'currency': currency, 'size' : size, 'price' : price_final , 'color':color}
            product_id_number = product_id_number + 1

        yield product

    def get_bookmarks(self , response):

        script_tag = response.css('div.js-listing.listing.droplet.styles-droplet.clearfix script').extract_first()
        bookmark = re.search('g1AAAA.*(?=\')', script_tag).group(0)
        return bookmark

    def get_image_urls(self, response):

        image_urls = []
        image_path = response.css('.responsiveImg::attr(src)').extract_first().replace('.jpg' , '')
        product_info = self.get_json(response)

        img_count = int(product_info['products'][0]['numimages'])
        if img_count > self.max_image_count:
            img_count = self.max_image_count

        character = iter(string.ascii_uppercase)
        while img_count:
            image_urls.append(self.image_url_t.format(image_path ,next(character)))
            img_count = img_count - 1

        return image_urls

    def get_gender(self , response):

        product_info = self.get_json(response)
        gender = product_info['gender']

        return self.gender_mapping[gender]

    def get_size(self, response):

        product_info = self.get_json(response)
        sizes = []

        for size in product_info['products'][0]['sizes']:
            sizes.append(size['size'])

        if sizes:
            return sizes
        else:
            return 'N/A'

    def get_json(self , response):

        product_info = re.search('{"stylecode.*(?=;)', response.text).group(0)
        return json.loads(product_info)

    def get_api(self , response):

        for key in self.api_mapping:
            if key in response.url:
                return self.api_mapping[key]
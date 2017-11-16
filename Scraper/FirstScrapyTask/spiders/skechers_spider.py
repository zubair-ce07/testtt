import re
import json
import urllib.parse
import string

import scrapy
from scrapy.spiders import Rule , CrawlSpider
from scrapy.linkextractors import LinkExtractor

from FirstScrapyTask.items import SkechersItem


class SkechersSpider(CrawlSpider):

    max_image_limit = 6
    image_url_t = '{}_{}.jpg'
    base_url = 'https://www.skechers.com'
    gender_mapping = {'M': 'Men', 'W': 'Women', 'B': 'Boys','G': 'Girls', 'U': 'Men/Women/Accessories'}
    base_api = 'https://www.skechers.com/en-us/api/html/products'

    api_accessories_t = '{}{}?category={}&bookmark='
    api_apparel_t = '{}{}?bookmark='
    api_gender_t = '{}{}?genders={}&bookmark='


    name = 'skechers'
    start_urls = ['https://www.skechers.com/en-us/']
    rules = (

        Rule(LinkExtractor(allow=('all$', 'apparel$','accessories')) , callback='parse_start_page_urls'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse_start_page_urls(self, response):
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
        script_currency = response.css('script:contains("skx_currency_code")').extract_first()
        currency = re.search('\'[A-Z]{3}\'', script_currency).group(0)
        color = response.css('.product-label.js-color::text').extract_first()

        sizes_info = self.get_size(response)
        for size in sizes_info:
            product['skus'][str(product_id_number)] = {'currency': currency, 'size' : size, 'price' : price_final , 'color':color}
            product_id_number = product_id_number + 1

        yield product

    def get_bookmarks(self , response):

        script_tag = response.css('script:contains("if (Skx.refinement)")').extract_first()
        bookmark = re.search('g1AAAA.*(?=\')', script_tag).group(0)
        return bookmark

    def get_image_urls(self, response):

        image_urls = []
        image_path = response.css('.responsiveImg::attr(src)').extract_first().replace('.jpg' , '')
        product_info = self.get_json(response)

        img_count = int(product_info['products'][0]['numimages'])
        if img_count > self.max_image_limit:
            img_count = self.max_image_limit

        image_characters = string.ascii_uppercase[:img_count]

        for character in image_characters:
            image_urls.append(self.image_url_t.format(image_path, character))

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

        script_tag = response.css('script:contains("Skx.style ")').extract_first()
        product_info = re.search('{"stylecode.*(?=;)', script_tag).group(0)
        return json.loads(product_info)

    def get_api(self , response):

        script_tag = response.css('script:contains("if (Skx.refinement)")').extract_first()
        base_api_attributes = json.loads(re.search('{"genders.*(?=;)', script_tag).group(0))
        if base_api_attributes['genders']:
            gender = ','.join(base_api_attributes['genders'])
            return self.api_gender_t.format(self.base_api , base_api_attributes['page'] , gender)

        else:
            if base_api_attributes['category'] == 'null':
                return self.api_apparel_t.format(self.base_api , base_api_attributes['page'])
            else:
                return self.api_accessories_t.format(self.base_api, base_api_attributes['page'] , base_api_attributes['category'])
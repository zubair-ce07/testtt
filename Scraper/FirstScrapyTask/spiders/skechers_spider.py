import re
import json
import urllib.parse
import string

from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from FirstScrapyTask.items import SkechersItem


class SkechersSpider(CrawlSpider):

    max_image_limit = 6
    image_url_t = '{}_{}.jpg'
    base_url = 'https://www.skechers.com'
    gender_mapping = {
        'M': 'Men',
        'W': 'Women',
        'B': 'Boys',
        'G': 'Girls',
        'U': 'Men/Women/Accessories'
    }
    base_api = 'https://www.skechers.com/en-us/api/html/products'
    api_accessories_t = '{}{}?category={}&bookmark='
    api_apparel_t = '{}{}?bookmark='
    api_gender_t = '{}{}?genders={}&bookmark='
    name = 'skechers'
    start_urls = ['https://www.skechers.com/en-us/']
    rules = (
        Rule(LinkExtractor(allow=('all$', 'apparel$', 'accessories')), callback='parse_start_page_urls'),
    )
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse_start_page_urls(self, response):
        category = response.css('.js-page-title::text').extract()
        sub_category = response.css('.selected::text').extract_first()
        if sub_category:
            category.append(sub_category)
        product_urls = response.css('div::attr(data-clicked-style-url)').extract()
        meta={'category' : category}
        for url in product_urls:
            url = urllib.parse.urljoin(self.base_url , url)
            yield Request(url=url, callback=self.parse_product , meta=meta)
        api = self.get_api(response)
        bookmark = response.css('script').re_first('bookmark =  \'(.+)\'')
        if bookmark:
            yield self.pagination_request(api=api, bookmark=bookmark, category=category)

    def parse_product_urls(self, response):
        category = response.meta['category']
        response_result = json.loads(response.text)
        product_urls = re.findall('\/en-us.*\s',response_result['stylesHtml'])
        meta = {'category': category}
        for url in product_urls:
            url = urllib.parse.urljoin(self.base_url , re.match('(.*?)\"', url).group(1))
            yield Request(url=url, callback=self.parse_product , meta=meta)
        api = response.meta['api']
        if response_result['bookmark']:
            yield self.pagination_request(api=api, bookmark=response_result['bookmark'], category=category)
    
    def pagination_request(self , api , bookmark, category):
        parse_result = urllib.parse.urlparse(api)
        url = urllib.parse.urlunparse((parse_result.scheme, parse_result.netloc, parse_result.path, '', parse_result.query + bookmark, ''))
        meta = {'api': api , 'category':category}
        return Request(url=url, callback=self.parse_product_urls, meta=meta)

    def parse_product(self, response):
        product = SkechersItem()
        product_style_id = response.css('.pull-right.product-label::text').extract_first()
        product_style_color = response.css('.js-color-code::text').extract_first()
        product_id = int(re.search('\d.*(?= )', product_style_id).group(0))
        product_info = json.loads(response.css('script').re_first('Skx.style = ({.+})'))
        image_path = response.css('.responsiveImg::attr(src)').extract_first().replace('.jpg', '')

        product['name'] = response.css('.product-title::text').extract_first()
        product['url'] = response.url
        product['brand'] = 'Skechers'
        product['description'] = response.css('.toggle-expand.toggle-description div::text').extract_first()
        product['product_id'] = '{}{}'.format(product_style_id, product_style_color)
        product['gender'] = self.gender_mapping[product_info['gender']]
        product['image_urls'] = self.get_image_urls(image_path , product_info['products'][0]['numimages'])
        product['category'] = response.meta['category']
        product['skus'] = self.create_skus(response, product_id, product_info['products'][0]['sizes'])
        yield product

    def create_skus(self, response, product_id, product_sizes):
        unique_sizes = set (size['size'] for size in product_sizes)
        price = response.css('.price-final::text').extract_first()
        currency = response.css('script').re_first('skx_currency_code: \'(.+)\'')
        color = response.css('.product-label.js-color::text').extract_first()
        skus = dict()
        for index, size in enumerate(unique_sizes):
            skus[str(product_id + index)] = {
                'currency': currency,
                'size': size,
                'price': price,
                'color': color
            }
        return skus
    
    def get_image_urls(self, image_path , img_count):
        img_count = min(int(img_count), self.max_image_limit)
        letters = string.ascii_uppercase[:img_count]
        return [self.image_url_t.format(image_path, letter) for letter in letters]

    def get_api(self , response):
        base_api_attributes = json.loads(response.css('script').re_first('Skx.refinement.values = ({.+})'))
        if base_api_attributes['genders']:
            gender = ','.join(base_api_attributes['genders'])
            return self.api_gender_t.format(self.base_api , base_api_attributes['page'] , gender)
        else:
            if not base_api_attributes['category']:
                return self.api_apparel_t.format(self.base_api , base_api_attributes['page'])
            else:
                return self.api_accessories_t.format(self.base_api, base_api_attributes['page'] , base_api_attributes['category'])

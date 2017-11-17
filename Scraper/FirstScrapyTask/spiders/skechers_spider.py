import re
import json
import urllib.parse
import string

from scrapy import Request
from scrapy.spiders import Rule , CrawlSpider
from scrapy.linkextractors import LinkExtractor

from FirstScrapyTask.items import SkechersItem


class SkechersSpider(CrawlSpider):

    max_image_limit = 6
    image_url_t = '{}_{}.jpg'
    base_url = 'https://www.skechers.com'
    gender_mapping = {'M': 'Men',
                      'W': 'Women',
                      'B': 'Boys',
                      'G': 'Girls',
                      'U': 'Men/Women/Accessories'}
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
            request = Request(url=url, callback=self.parse_style_info)
            yield request

        if bookmark:
            yield self.request_for_next_page(api=api , bookmark= bookmark)

    def parse_style_urls(self, response):
        api = response.meta['api']
        response_result = json.loads(response.text)
        product_urls = re.findall('\/en-us.*\s',response_result['stylesHtml'])

        for url in product_urls:
            url = urllib.parse.urljoin(self.base_url , re.match('(.*?)\"', url).group(1))
            request = Request(url=url, callback=self.parse_style_info)
            yield request

        if response_result['bookmark']:
            yield self.request_for_next_page(api=api, bookmark=response_result['bookmark'])

    def parse_style_info(self, response):

        product = SkechersItem()
        product_style_id = response.css('.pull-right.product-label::text').extract_first()
        product_style_color = response.css('.js-color-code::text').extract_first()
        product_id_number = int(re.search('\d.*(?= )', product_style_id).group(0))

        product['name'] = response.css('.product-title::text').extract_first()
        product['url'] = response.url
        product['brand'] = 'Skechers'
        product['description'] = response.css('.toggle-expand.toggle-description div::text').extract_first()
        product['product_id'] = '{}{}'.format(product_style_id, product_style_color)
        product_info = self.get_json(response)
        image_path = response.css('.responsiveImg::attr(src)').extract_first().replace('.jpg' , '')

        product['gender'] = self.get_gender(product_info['gender'])
        product['image_urls'] = self.get_image_urls(image_path , product_info['products'][0]['numimages'])
        product['skus'] = {}
        product['category'] = product['name'].split('-')
        product['category'].append(product['gender'])

        price_final = response.css('.price-final::text').extract_first()
        currency = response.css('script').re_first('skx_currency_code: \'(.+)\'')
        color = response.css('.product-label.js-color::text').extract_first()

        sizes_info = self.get_size(product_info['products'][0]['sizes'])
        for size in sizes_info:
            product['skus'][str(product_id_number)] = {'currency': currency,
                                                       'size' : size,
                                                       'price' : price_final ,
                                                       'color':color}
            product_id_number = product_id_number + 1

        yield product

    def get_bookmarks(self , response):

        return response.css('script').re_first('bookmark =  \'(.+)\'')

    def get_image_urls(self, image_path , img_count):

        image_urls = []
        img_count = min(int(img_count), self.max_image_limit)
        for character in string.ascii_uppercase[:img_count]:
            image_urls.append(self.image_url_t.format(image_path, character))
        return image_urls

    def get_gender(self , gender):

        return self.gender_mapping[gender]

    def get_size(self, product_sizes):

        sizes = []
        for size in product_sizes:
            sizes.append(size['size'])

        if sizes:
            return sizes
        else:
            return 'N/A'

    def get_json(self , response):

        return json.loads(response.css('script').re_first('Skx.style = ({.+})'))

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

    def request_for_next_page(self , api , bookmark):

        parse_result = urllib.parse.urlparse(api)
        url = urllib.parse.urlunparse((parse_result.scheme, parse_result.netloc, parse_result.path, '', parse_result.query + bookmark, ''))
        pagination_request = Request(url=url, callback=self.parse_style_urls, meta={'api': api})
        return pagination_request

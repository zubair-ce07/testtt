import json

from copy import deepcopy
from scrapy import Request

from scrapyproduct.items import ProductItem, SizeItem
from scrapyproduct.spiderlib import SSBaseSpider
from scrapyproduct.toolbox import (category_mini_item, extract_text_nodes, register_deliveryregion)


class AdiddaaCraaler(SSBaseSpider):
    name = 'adiddas'
    long_name = 'Adiddas'

    country = ''
    max_stock_level = 1

    base_url = 'https://www.adidas.co.uk/'
    seen_identifiers = set()
    detail_page_t = 'https://www.adidas.co.uk/api/products/{}'
    availability_t = '{}/availability'

    headers = {'authority': 'www.adidas.co.uk',
               'method': 'GET',
               'path': '/',
               'scheme': 'https',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'en-US,en;q=0.9',
               'cache-control': 'max-age=0',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

    countries_info = [
        ('uk', 'GBP', 'en', 'https://www.adidas.co.uk/', ['uk']),
    ]

    """custom_settings = {
        'DOWNLOAD_TIMEOUT': 240,
    }"""

    def test_single_item(self):
        item = ProductItem(
            identifier='ED8667',
            country_code='us',
            language_code='en',
            currency='USD',
            category_names=['Test cat'],
            url='https://www.adidas.co.uk/api/products/ED8667',
            referer_url=None,
            brand=self.long_name
        )
        return Request(item['url'], self.parse_detail, meta={'item': item, 'dont_merge_cookies': True})

    def start_requests(self):
        #yield self.test_single_item()
        #return

        for country_code, currency, language, country_url, same_region_dlrs in self.countries_info:
            if self.country and country_code not in self.country:
                continue
            register_deliveryregion(self, country_code, currency, same_region_dlrs, country_url)
            meta = {
                'currency': currency,
                'cookiejar': country_code,
                'country_code': country_code,
                'language': language,
                'dont_merge_cookies': True
            }

            yield Request(country_url, self.parse_homepage, meta=meta, headers=self.headers)

    def parse_homepage(self, response):
        for level1 in response.css('.main-items'):
            for level2 in level1.css('.sub-items > li'):
                yield self.make_request(response, [level1, level2])
                for level3 in level2.css('.sub-sub-items li')[1:]:
                    yield self.make_request(response, [level1, level2, level3])

    def make_request(self, response, selectors):
        categories = [extract_text_nodes(sel.css('a'))[0] for sel in selectors]
        url = selectors[-1].css('a::attr(href)').extract_first()
        meta = deepcopy(response.meta)
        meta['categories'] = categories
        return Request(response.urljoin(url), self.parse_category, meta=meta, dont_filter=True, headers=self.headers)

    def parse_category(self, response):
        for category in response.css('.gl-product-card__media a'):
            url = category.css('::attr(href)').extract_first()
            identifier = url.split('/')[-1].split('.')[0]

            item = ProductItem(
                url=response.urljoin(url),
                identifier=identifier,
                referer_url=response.url,
                category_names=response.meta['categories'],
                language_code=response.meta['language'],
                country_code=response.meta['country_code'],
                currency=response.meta['currency'],
                brand=self.long_name
            )
            yield category_mini_item(item)

            country_id = '{}_{}'.format(item['country_code'], item['identifier'])
            if country_id in self.seen_identifiers:
                continue

            self.seen_identifiers.add(country_id)
            meta = deepcopy(response.meta)
            meta['item'] = item
            yield Request(self.detail_page_t.format(identifier), self.parse_detail, meta=meta, dont_filter=True,
                          headers=self.headers)

        yield self.parse_pagination(response)

    def parse_pagination(self, response):
        next_page = response.css('.pagination__control--next___329Qo a::attr(href)').extract_first()
        if next_page:
            url = response.urljoin(next_page)
            return Request(url, self.parse_category, meta=response.meta, dont_filter=True, headers=self.headers)

    def parse_detail(self, response):
        item = response.meta['item']
        prod_detail = json.loads(response.text)
        item['title'] = prod_detail['name']
        item['base_sku'] = prod_detail['model_number']
        item['color_name'] = prod_detail['attribute_list']['color']
        item['description_text'] = prod_detail['product_description'].get('text', 'N/A')
        item['image_urls'] = self.get_image_urls(prod_detail['view_list'])
        item['old_price_text'] = prod_detail['pricing_information']['standard_price']
        item['new_price_text'] = prod_detail['pricing_information']['currentPrice']

        meta = deepcopy(response.meta)
        meta['item'] = item
        yield Request(self.availability_t.format(response.url), callback=self.parse_size, meta=meta, dont_filter=True,
                      headers=self.headers)

    def parse_size(self, response):
        item = response.meta['item']
        size_detail = json.loads(response.text)
        if size_detail['availability_status'] == 'PREVIEW':
            return item
        item['size_infos'] = self.get_size_infos(size_detail['variation_list'])
        item['available'] = any(size['stock'] for size in item['size_infos'])

        return item

    def get_image_urls(self, images):
        image_urls = []
        for image in images:
            image_urls.append(image['image_url'])
        return image_urls

    def get_size_infos(self, sizes):
        size_infos = []
        for size in sizes:
            size_info = SizeItem(
                size_name=size['size'],
                stock=1 if size['availability'] > 0 else 0,
                size_identifier=size['sku'],
            )
            size_infos.append(size_info)
        return size_infos

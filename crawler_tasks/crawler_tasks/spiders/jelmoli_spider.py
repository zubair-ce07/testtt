import re
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, TextResponse
from crawler_tasks.items import JelmoliProduct


class JelmoliSpider(CrawlSpider):
    name = 'jelmoli'
    allowed_domains = ['jelmoli-shop.ch']
    start_urls = [
        'https://www.jelmoli-shop.ch/'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=('.rendered-data', '[class^="sh"]')),
             process_links='filter_urls', callback='parse_category_url', follow=True),
    )

    words_regex = re.compile('\w+')
    base_url = 'https://www.jelmoli-shop.ch'
    pagination_url = 'https://www.jelmoli-shop.ch/suche/mba/magellan'
    product_page_url_t = 'https://www.jelmoli-shop.ch/p/{}/{}'
    product_skus_url_t = 'https://www.jelmoli-shop.ch/INTERSHOP/rest/WFS/EmpirieCom-JelmoliCH-Site/-;' \
        'loc=de_CH;cur=CHF/inventories/{}/master'
    not_allow_keywords = [
        'marken', 'elektronik', 'spielzeug', 'sportbedarf',
        'fitnessgeraete', 'aktionen', 'werkzeuge', 'sale'
    ]

    def filter_urls(self, links):
        return [
            link for link in links
            if not any(
                keyword in link.url
                for keyword in self.not_allow_keywords)
        ]

    def parse_category_url(self, response):
        raw_json = response.css('.product-listing-json::text').extract_first()
        if not raw_json:
            return

        pre_known = {}
        url = response.url

        if 'herren' in url:
            pre_known['gender'] = 'men'
        elif 'damen' in url:
            pre_known['gender'] = 'women'
        elif 'kinder' in url:
            pre_known['gender'] = 'kids'
        elif any(keyword in url for keyword in ['bettwaesche', 'wohnen']):
            pre_known['industry'] = 'homeware'

        return self.parse_category(raw_json, pre_known)

    def parse_category(self, raw_json, pre_known):
        meta = {
            'pre_known_product_values': pre_known
        }
        request = Request(self.base_url, meta=meta)
        response = TextResponse(url='', body=raw_json.encode(), request=request)
        yield next(self.parse_product_listing(response))

        result = json.loads(raw_json)['result']
        category_id = result['category']['current']['id']
        product_count = result['count']
        per_request_count = len(result['styles'])
        requested_count = per_request_count
        payload = {
            'category': category_id,
            'channel': "web",
            'clientId': "JelmoliCh",
            'locale': "de_CH"
        }
        while requested_count < product_count:
            payload['start'] = requested_count
            payload['count'] = per_request_count
            requested_count += per_request_count
            yield Request(self.pagination_url, body=json.dumps(payload), meta=meta,
                          method='POST', callback=self.parse_product_listing)

    def parse_product_listing(self, response):
        json_response = json.loads(response.text)
        items = json_response.get('searchresult', json_response)['result']['styles']
        pre_known_product_values = response.meta.get('pre_known_product_values', {})

        for item in items:
            try:
                name_without_brand = item['name'].split(' ', 1)[1]
            except IndexError:
                name_without_brand = item['name']

            meta = {
                'product_id': item['masterSku'],
                'name': item.get('nameNoBrand', name_without_brand),
                'brand': item['brand'],
                'description': item['description'],
                'currency': item['price']['currency'],
                'price': item['price']['value'],
                'pre_known_product_values': pre_known_product_values
            }

            words = self.words_regex.findall(item['name'])
            name = '-'.join([word.lower() for word in words])
            url = self.product_page_url_t.format(name, item['masterSku'])
            yield Request(url, meta=meta, callback=self.parse_product)

    def parse_product_care(self, response):
        desc1_selector = response.css('[itemprop="description"]')
        if not desc1_selector:
            return []

        desc2 = desc1_selector.css('.oocv-description').extract_first()
        if desc2 and '%' in desc2:
            return [desc2]
        else:
            desc1 = desc1_selector.extract_first()
            if '%' in desc1:
                return [desc1]
        return []

    def parse_product(self, response):
        meta = response.meta
        product = JelmoliProduct()
        product['merch_info'] = []
        product['market'] = ''
        product['product_id'] = meta['product_id']
        product['name'] = meta['name']
        product['brand'] = meta['brand']
        product['description'] = meta['description']
        product['url'] = response.url
        product['category'] = response.css('.nav-breadcrumb a::text').extract()
        product['care'] = self.parse_product_care(response)
        product.update(response.meta.get('pre_known_product_values', {}))

        image_urls = response.css('.image-gallery-item img::attr("data-lazysrc")').extract()
        main_image_url = response.css('.zoom-image::attr("data-zoom-uri")').extract_first()
        if image_urls:
            product['image_urls'] = [re.sub('baur_format_.', 'formatz', url) for url in image_urls]
        else:
            product['image_urls'] = [main_image_url]

        meta['product'] = product
        url = self.product_skus_url_t.format(meta['product_id'])
        yield Request(url, meta=meta, callback=self.parse_skus)

    def parse_skus(self, response):
        skus = {}
        currency = response.meta['currency']
        price = response.meta['price']
        json_response = json.loads(response.text)
        for item in json_response['variants']:
            axis_data = item['axisData']
            try:
                skus[item['sku']] = {
                    'colour': axis_data[0]['value'],
                    'size': axis_data[1]['value'],
                    'currency': currency,
                    'price': price
                }
            except IndexError:
                pass
        product = response.meta['product']
        product['skus'] = skus
        return product

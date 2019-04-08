import re
import json

from w3lib.url import add_or_replace_parameter
from scrapy.spiders import CrawlSpider, Request

from savagex_crawler.items import SavagexCrawlerItem


class SavagexCrawler(CrawlSpider):

    name = 'savagex-us-crawl'
    allowed_domains = ['savagex.com']
    start_urls = ['https://www.savagex.com/']

    cookies = {
        'bfx.country': 'US',
        'bfx.language': 'en',
        'bfx.currency': 'USD',
    }

    headers = {
        'x-tfg-storedomain': 'www.savagex.com',
        'x-api-key': 'V0X9UnXkvO4vTk1gYHnpz7jQyAMO64Qp4ONV2ygu',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
        }

    colour_url_t = 'https://www.savagex.com/api/products/{}'
    category_url_t = 'https://www.savagex.com/api/products?aggs=true&includeOutOfStock=true&' \
                     'page=1&size=28&defaultProductCategoryIds={}&categoryTagIds={}&excludeFpls=13506'

    def parse_start_url(self, response):
        yield Request(url=response.url, callback=self.parse_categories)

    def parse_categories(self, response):
        raw_categories = self.raw_category(response)['sections']

        for category_k in [i for i in raw_categories.keys()]:
            for sub_category_k in raw_categories[category_k]['subsections'].keys():
                category = raw_categories[category_k]['defaultProductCategoryIds']
                sub_category = raw_categories[category_k]['subsections'][sub_category_k]['categoryTagIds']

                yield Request(url=self.category_url_t.format(category, '+'.join([str(i)
                              for i in sub_category])), headers=self.headers, cookies=self.cookies,
                              callback=self.parse_pagination, meta={'category': [category_k, sub_category_k]})

    def parse_pagination(self, response):
        pages = json.loads(response.text).get('pages')
        return [Request(url=add_or_replace_parameter(response.url, 'page', page), headers=self.headers,
                        cookies=self.cookies, meta={'category': response.meta['category']},
                        callback=self.parse_listings) for page in range(1, pages)]

    def parse_listings(self, response):
        return [Request(url='https://www.savagex.com/shop/{}'.format(f"{i['permalink']}-{i['master_product_id']}"),
                        headers=self.headers, cookies=self.cookies, meta={'category': response.meta['category']},
                        callback=self.parse_product) for i in json.loads(response.text)['products']]

    def parse_product(self, response):
        item = SavagexCrawlerItem()
        raw_product = self.raw_product(response)

        item['care'] = []
        item['skus'] = {}
        item['lang'] = 'en'
        item['market'] = 'USA'
        item['gender'] = 'women'
        item['image_urls'] = []
        item['url'] = response.url
        item['brand'] = self.product_brand(response)
        item['name'] = self.product_name(raw_product)
        item['category'] = self.product_category(response)
        item['retailer_sku'] = self.product_id(raw_product)
        item['description'] = self.product_description(raw_product)
        item['meta'] = {'requests_queue': self.colour_requests(response, item)}

        return self.next_request_or_item(item)

    def product_name(self, raw_product):
        return raw_product['label']

    def product_category(self, response):
        return response.meta['category']

    def product_id(self, raw_product):
        return raw_product['master_product_id']

    def next_request_or_item(self, item):
        requests = item['meta']['requests_queue']
        if requests:
            request = requests.pop()
            request.meta['item'] = item
            return request
        item.pop('meta')
        return item

    def product_gender(self, response):
        css = '#panel2-1 .bronze-text ::text'
        return response.css(css).extract_first().split(' ')

    def product_pricing(self, response, raw_skus):
        prev_price = raw_skus.get('retail_unit_price')
        pricing = {'currency': response.meta['currency']}
        pricing['price'] = raw_skus.get('default_unit_price')

        if prev_price:
            pricing['previous_price'] = prev_price

        return pricing

    def product_brand(self, response):
        css = '[property="og:title"] ::attr(content)'
        return response.css(css).extract_first().split('|')[-1]

    def parse_colour(self, response):
        self.product_image_urls(response)
        response.meta['item']['skus'].update(self.skus(response))
        return self.next_request_or_item(response.meta['item'])

    def product_image_urls(self, response):
        [response.meta['item']['image_urls'].append(f'https:{i}')
         for i in json.loads(response.text)['image_view_list']]

    def raw_category(self, response):
        category_r = re.compile(r'"productBrowser":(.+),"collections"')
        return json.loads(category_r.search(response.text).group(1)+'}')

    def clean(self, raw_text):
        if type(raw_text) is list:
            return [re.sub('(\r*)(\t*)(\n*)', '', i) for i in raw_text]
        return re.sub('(\r*)(\t*)(\n*)', '', raw_text)

    def skus(self, response):
        skus = {}
        raw_skus = json.loads(response.text)
        common_sku = self.product_pricing(response, raw_skus['suggest']['payload'])
        colour = raw_skus['color']

        for raw_sku in raw_skus['product_id_object_list']:
            sku = common_sku.copy()

            if 'out' in raw_sku['availability']:
                sku['out_of_stock'] = True

            sku['colour'] = colour
            sku['size'] = raw_sku['size'] or 'One Size'
            skus[f'{colour}_{sku["size"]}'] = sku

        return skus

    def product_description(self, raw_product):
        return [raw_product['medium_description'] + raw_product['long_description']]

    def raw_product(self, response):
        sku_r = re.compile(r'__NEXT_DATA__ = {"props":(.*),"page"')
        return json.loads(sku_r.search(response.text).group(1))['initialProps']['pageProps']['product']

    def colour_requests(self, response, item):
        css = '[property="og:price:currency"] ::attr(content)'
        raw_colours = [i["related_product_id"] for i in self.raw_product(response)['related_product_id_object_list']]

        return [Request(callback=self.parse_colour, meta={'item': item, 'currency': response.css(css).extract_first()},
                        url=self.colour_url_t.format(colour_id), headers=self.headers) for colour_id in raw_colours]

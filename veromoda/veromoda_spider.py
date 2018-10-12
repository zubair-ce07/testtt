import json
import re

from scrapy import Request
from w3lib.url import add_or_replace_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class MixinCN:
    retailer = 'veromoda-cn'
    market = 'CN'
    retailer_currency = 'CNY'
    start_urls = ['https://www.veromoda.com.cn/assets/pc/VEROMODA/nav.json']
    allowed_domains = ['veromoda.com.cn']
    gender = Gender.WOMEN.value


class VeromodaCNParseSpider(MixinCN, BaseParseSpider):
    name = MixinCN.retailer + '-parse'

    url_t = 'https://www.veromoda.com.cn/goodsDetails.html?design={}'

    def parse(self, response):
        raw_product = json.loads(response.text)['data']
        product_id = self.product_id(raw_product)

        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate(garment, response, url=self.url(raw_product))

        garment['name'] = self.product_name(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['brand'] = self.product_brand(raw_product)
        garment['skus'] = self.skus(raw_product)
        garment['image_urls'] = self.image_urls(response, raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)

        return self.next_request_or_garment(garment)

    def url(self, raw_product):
        return self.url_t.format(self.product_id(raw_product))

    def product_description(self, raw_product):
        description = raw_product['describe']
        return clean(description.split('，')) if description else []

    def product_care(self, raw_product):
        care = raw_product['goodsInfo']
        return clean(care.split('，')) if care else []

    def product_id(self, raw_product):
        return raw_product['projectCode']

    def product_name(self, raw_product):
        return raw_product['goodsName']

    def product_brand(self, raw_product):
        return raw_product['brand']

    def product_category(self, raw_product):
        return [raw_product['color'][0]['categoryName']]

    def image_urls(self, response, raw_product):
        image_urls = []
        [image_urls.extend([response.urljoin(url) for url in c['picurls']]) for c in raw_product['color']]
        return image_urls

    def skus(self, raw_product):
        skus = {}

        for colour_variant in raw_product['color']:
            money_strs = [colour_variant['originalPrice'], colour_variant['price'], self.retailer_currency]
            sku_common = self.product_pricing_common(self, money_strs=money_strs)
            sku_common['colour'] = colour_variant['colorAlias']

            for size_variant in colour_variant['sizes']:
                sku = sku_common.copy()
                sku['size'] = size_variant['sizeAlias']

                if size_variant['sizeAlias'] == 'ACC':
                    sku['size'] = self.one_size

                if not size_variant['sellStock']:
                    sku['out_of_stock'] = True

                skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus


class VeromodaCNCrawlSpider(MixinCN, BaseCrawlSpider):
    name = MixinCN.retailer + '-crawl'
    parse_spider = VeromodaCNParseSpider()

    categories_re = re.compile('classifyIds=(\d+)')

    headers = {
        'token': 'eyJqdGkiOiI2NVo4I3VCUUEhIiwiaWF0IjoxNTM4OTk0NjQxLCJjaGFubmVsIjoiNiJ9.'
                 '-juQO5Si80WNfBGmn-h6IfXf6ae2Bj4u4L2gtmSbRiY'
    }
    category_url_t = 'https://www.veromoda.com.cn/api/goods/goodsList?classifyIds={}&currentpage=1' \
                     '&sortDirection=desc&sortType=1'
    product_url_t = 'https://www.veromoda.com.cn/detail/VEROMODA/{}.json'

    def parse_start_url(self, response):
        meta = {
            'trail': self.add_trail(response)
        }
        yield from [Request(url=self.category_url_t.format(c), headers=self.headers, callback=self.parse_category,
                            meta=meta) for c in self.categories_re.findall(response.text)]

    def parse_category(self, response):
        yield from self.item_requests(response) + self.pagination_requests(response)

    def item_requests(self, response):
        products = json.loads(response.text)['data']

        meta = {
            'trail': self.add_trail(response)
        }
        return [Request(url=self.product_url_t.format(p['goodsCode']), callback=self.parse_item, meta=meta)
                for p in products]

    def pagination_requests(self, response):
        category = json.loads(response.text)
        if category['currentpage'] is not 1:
            return []

        meta = {
            'trail' : self.add_trail(response)
        }
        return [Request(url=add_or_replace_parameter(response.url, 'currentpage', page_no), headers=self.headers,
                        callback=self.parse_category, meta=meta) for page_no in range(2, category['totalPage'] + 1)]

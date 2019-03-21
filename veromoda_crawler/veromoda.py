import json

from scrapy.spiders import CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from veromoda_crawler.items import VeromodaCrawlerItem


class VeromodaCrawler(CrawlSpider):

    custom_settings = {'DOWNLOAD_DELAY': 2,
                       'CONCURRENT_REQUESTS_PER_IP': 1}

    name = 'veromoda-cn-crawl'
    start_urls = ['https://www.veromoda.com.cn']
    allowed_domains = ['veromoda.com.cn', 'cdn.bestseller.com.cn']

    headers = {'token': 'eyJqdGkiOiJIUzgjV3dGY1daIiwiaWF0IjoxNTUyMzczNzYwLCJjaGFubmVs'
                        'IjoiNiJ9.Ur0x3yaIB3BFVZ6LeTzFvdCprK6VR-xUYo2X4EqaWTU'}

    image_url_t = 'https://www.veromoda.com.cn/{}'
    product_url_t = 'https://cdn.bestseller.com.cn/detail/VEROMODA/{}.json'
    category_url_t = 'https://www.veromoda.com.cn/api/goods/goodsList?classifyIds={}&' \
                     'currentpage=1&sortDirection=desc&sortType=1'

    def parse_start_url(self, response):
        url = 'https://cdn.bestseller.com.cn/classify/h5/VEROMODA/h5_list.json'
        yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        for raw_category in json.loads(response.text)['data']:
            yield Request(url=self.category_url_t.format(raw_category['classifyId']),
                          headers=self.headers, callback=self.parse_pagination)

    def parse_pagination(self, response):
        pages = json.loads(response.text)['totalPage']
        yield Request(url=response.url, callback=self.parse_products,
                      headers=self.headers)

        if pages > 1:
            for page in range(2, pages):
                yield Request(url=add_or_replace_parameter(response.url, 'Page', page),
                              headers=self.headers, callback=self.parse_products)

    def parse_products(self, response):
        for product in json.loads(response.text)['data']:
            yield Request(url=self.product_url_t.format(product['goodsCode']),
                          headers={'Origin': 'https://www.veromoda.com.cn'},
                          meta={'raw_product': product}, callback=self.parse_product)

    def parse_product(self, response):
        item = VeromodaCrawlerItem()
        raw_skus = json.loads(response.text)
        raw_product = response.meta['raw_product']

        item['lang'] = 'zh'
        item['market'] = 'CN'
        item['gender'] = 'women'
        item['skus'] = self.skus(raw_skus)
        item['url'] = self.product_url(response)
        item['name'] = self.product_name(raw_product)
        item['image_urls'] = self.image_urls(raw_skus)
        item['brand'] = self.product_brand(raw_product)
        item['category'] = self.product_category(raw_product)
        item['description'] = self.product_description(raw_product)
        item['retailer_sku'] = self.product_retailer_sku(raw_product)

        return item

    def product_url(self, response):
        return response.url

    def product_name(self, raw_product):
        return raw_product['goodsName']

    def product_brand(self, raw_product):
        return raw_product['brandName']

    def product_category(self, raw_product):
        return raw_product['categoryName']

    def product_description(self, raw_product):
        return raw_product['goodsInfo']

    def product_retailer_sku(self, raw_product):
        return raw_product['goodsCode']

    def product_pricing(self, raw_sku):
        pricing = {'currency': 'YUAN'}
        pricing['price'] = raw_sku['data']['color'][0]['price']

        if raw_sku['data']['color'][0]['discount'] != 1:
            pricing['prev_price'] = raw_sku['data']['color'][0]['originalPrice']

        return pricing

    def skus(self, raw_skus):
        skus = {}
        common_sku = self.product_pricing(raw_skus)

        for colour in raw_skus['data']['color']:
            for size in colour['sizes']:
                sku = common_sku.copy()
                sku['colour'] = colour['color']
                sku['size'] = size['sizeAlias']

                if size['sellStock']:
                    sku['out_of_stock'] = True

                skus[f'{raw_skus["data"]["projectCode"]}_{colour["color"]}_{size["size"]}'] = sku

        return skus

    def image_urls(self, raw_sku):
        return [self.image_url_t.format(url) for i in raw_sku['data']['color'] for url in i['picurls']]

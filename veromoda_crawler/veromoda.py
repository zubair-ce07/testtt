import json

from scrapy.spiders import CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from veromoda_crawler.items import VeromodaCrawlerItem


class VeromodaCrawler(CrawlSpider):

    custom_settings = {'DOWNLOAD_DELAY': 2,
                       'RANDOMIZE_DOWNLOAD_DELAY': False,
                       'CONCURRENT_REQUESTS_PER_IP': 1}

    name = 'veromoda-cn-crawl'
    start_urls = ['https://www.veromoda.com.cn']
    allowed_domains = ['veromoda.com.cn', 'cdn.bestseller.com.cn']

    headers = {
        'brand': 'VEROMODA',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'application/json, text/plain, */*',
        'token': 'eyJqdGkiOiJIUzgjV3dGY1daIiwiaWF0IjoxNTUyMzczNzYwLCJjaGFubmVs'
                 'IjoiNiJ9.Ur0x3yaIB3BFVZ6LeTzFvdCprK6VR-xUYo2X4EqaWTU',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }

    url_t = 'https://www.veromoda.com.cn/api/goods/goodsList?classifyIds={}&' \
            'currentpage=1&sortDirection=desc&sortType=1'

    def parse_start_url(self, response):
        url = 'https://cdn.bestseller.com.cn/classify/h5/VEROMODA/h5_list.json'
        yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        raw_category = json.loads(response.text)
        category_ids = [i['classifyId'] for i in raw_category['data']]

        for category_id in category_ids:
            yield Request(url=self.url_t.format(category_id), headers=self.headers,
                          callback=self.parse_pagination)

    def parse_pagination(self, response):
        pages = json.loads(response.text)['totalPage']
        yield Request(url=response.url, callback=self.parse_products,
                      headers=self.headers)

        if pages > 1:
            for page in range(2, pages):
                next_url = add_or_replace_parameter(response.url, 'Page', page)
                yield Request(url=next_url, headers=self.headers,
                              callback=self.parse_products)

    def parse_products(self, response):
        headers = self.headers.copy()
        products = json.loads(response.text)['data']
        next_url = 'https://cdn.bestseller.com.cn/detail/VEROMODA/{}.json'

        if 'brand' in headers.keys():
            del headers['brand']
            del headers['token']
            del headers['Accept-Language']
            del headers['Accept-Encoding']
            headers['Origin'] = 'https://www.veromoda.com.cn'

        for product in products:
            yield Request(
                url=next_url.format(product['goodsCode']), headers=headers,
                meta={'raw_product': product}, callback=self.parse_product_detail)

    def parse_product_detail(self, response):
        item = VeromodaCrawlerItem()
        raw_sku = self.raw_sku(response)
        raw_product = response.meta['raw_product']

        item['lang'] = 'zh'
        item['market'] = 'cn'
        item['skus'] = self.skus(raw_sku)
        item['url'] = self.product_url(response)
        item['image_urls'] = self.image_urls(raw_sku)
        item['name'] = self.product_name(raw_product)
        item['brand'] = self.product_brand(raw_product)
        item['gender'] = self.product_gender(raw_product)
        item['category'] = self.product_category(raw_product)
        item['description'] = self.product_description(raw_product)
        item['retailer_sku'] = self.product_retailer_sku(raw_product)

        return item

    def product_url(self, response):
        return response.url

    def product_name(self, raw_product):
        return raw_product['goodsName']

    def raw_sku(self, response):
        return json.loads(response.text)

    def product_brand(self, raw_product):
        return raw_product['brandName']

    def product_gender(self, raw_product):
        return raw_product['categoryName']

    def product_category(self, raw_product):
        return raw_product['categoryName']

    def product_description(self, raw_product):
        return raw_product['goodsInfo']

    def product_retailer_sku(self, raw_product):
        return raw_product['goodsCode']

    def image_urls(self, raw_sku):
        url_t = 'https://www.veromoda.com.cn/{}'
        return [url_t.format(url) for i in raw_sku['data']['color'] for url in i['picurls']]

    def product_pricing(self, raw_sku):
        pricing = {'currency': 'YUAN'}
        pricing['price'] = raw_sku['data']['color'][0]['price']

        if raw_sku['data']['color'][0]['discount'] != 1:
            pricing['prev_price'] = raw_sku['data']['color'][0]['originalPrice']

        return pricing

    def skus(self, raw_sku):
        skus = {}
        sku_id = raw_sku['data']['projectCode']
        common_sku = self.product_pricing(raw_sku)

        for colour in raw_sku['data']['color']:
            for size in colour['sizes']:

                sku = common_sku.copy()
                sku['colour'] = colour['color']
                sku['size'] = size['sizeAlias']

                if size['sellStock'] == 0:
                    sku['out_of_stock'] = True

                skus[f'{sku_id}_{colour["color"]}_{size["size"]}'] = sku

        return skus


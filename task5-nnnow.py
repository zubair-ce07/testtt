import json
import scrapy

from scrapy.spiders import CrawlSpider

from ..items import NnnowItem


class NnnowParser:

    def parse_details(self, response):
        nnnow_product = NnnowItem()
        pg_data_detail = \
            json.loads(response.css('script').get().replace('<script>window.DATA= ', '').replace('</script>', ''))
        product_detail = pg_data_detail['ProductStore']['PdpData']['mainStyle']

        nnnow_product['retailer_sku'] = self.extract_retailor_sku(response)
        nnnow_product['gender'] = self.extract_gender(product_detail)
        nnnow_product['category'] = self.extract_category(response)
        nnnow_product['brand'] = self.extract_brand(product_detail)
        nnnow_product['url'] = self.extract_url(response)
        nnnow_product['name'] = self.extract_name(product_detail)
        nnnow_product['description'] = self.extract_description(product_detail)
        nnnow_product['care'] = self.extract_care(product_detail)
        nnnow_product['img_urls'] = self.extract_img_urls(product_detail)
        nnnow_product['skus'] = self.extract_skus(product_detail, response)
        nnnow_product['request_queue'] = self.extract_color_requests(pg_data_detail)

        yield self.get_item_or_req_to_yield(nnnow_product)

    def parse_skus(self, response):
        nnnow_product = response.meta['item']
        pg_data_detail = \
            json.loads(response.css('script').get().replace('<script>window.DATA= ', '').replace('</script>', ''))
        product_detail = pg_data_detail['ProductStore']['PdpData']['mainStyle']

        nnnow_product['img_urls'] += self.extract_img_urls(product_detail)
        nnnow_product['skus'] += self.extract_skus(product_detail, response)

        yield self.get_item_or_req_to_yield(nnnow_product)

    def get_item_or_req_to_yield(self, nnnow_product):
        if nnnow_product['request_queue']:
            request_next = nnnow_product['request_queue'].pop()
            request_next.meta['item'] = nnnow_product
            return request_next

        del nnnow_product['request_queue']
        return nnnow_product

    def extract_color_requests(self, pg_data_detail):
        if 'colors' in pg_data_detail['ProductStore']['PdpData'].keys():
            colors = pg_data_detail['ProductStore']['PdpData']['colors']['colors']['']
            current_color = pg_data_detail['ProductStore']['PdpData']['colors']['selectedColor']['url']
            domain = 'https://www.nnnow.com'
            return [scrapy.Request(domain + color['url'], callback=self.parse_skus)
                    for color in colors if color['url'] not in current_color]

    def extract_retailor_sku(self, response):
        return response.css('[itemprop="sku"]::text').get()[:9]

    def extract_gender(self, product_detail):
        return product_detail['gender']

    def extract_category(self, response):
        return response.css('.nw-breadcrumb-link ::text').getall()

    def extract_brand(self, product_detail):
        return product_detail['brandName']

    def extract_url(self, response):
        return response.url

    def extract_name(self, product_detail):
        return product_detail['name']

    def extract_description(self, product_detail):
        finer_details = product_detail['finerDetails']
        if finer_details['specs']:
            return finer_details['specs']['list']
        return finer_details['whatItIs']['list'] + finer_details['whatItDoes']['list']

    def extract_care(self, product_detail):
        if product_detail['finerDetails']['compositionAndCare']:
            return product_detail['finerDetails']['compositionAndCare']['list']
        return []

    def extract_img_urls(self, product_detail):
        return [imgs['medium'] for imgs in product_detail['images']]

    def extract_skus(self, product_detail, response):
        color = product_detail['colorDetails']['primaryColor']
        currency = response.css('[itemProp="priceCurrency"]::attr(content)').get()
        common_sku = {'Currency': currency, 'Colour': color}
        skus = []
        for product_sku in product_detail['skus']:
            sku = common_sku.copy()
            sku['price'] = product_sku['price']
            sku['previous_price'] = product_sku['mrp']
            sku['size'] = product_sku['size']
            sku['outofstock'] = not product_sku['inStock']
            sku['sku_id'] = color + '_' + product_sku['size']
            skus.append(sku)
        return skus


class NnnowSpider(CrawlSpider):
    name = "nnnowSpider"
    allowed_domains = ['nnnow.com']
    start_urls = [
        'https://www.nnnow.com/men-fashion',
        'https://www.nnnow.com/women-fashion',
        'https://www.nnnow.com/kids-fashion',
    ]

    def parse(self, response):
        json_response = \
            json.loads(response.css('script').get().replace('<script>window.DATA= ', '').replace('</script>', ''))
        total_products_on_page = json_response['ProductStore']['ProductData']['totalPages']
        request_url = 'https://api.nnnow.com/d/apiV2/listing/products'
        category = response.url.split('/')[-1]
        request_headers = {'accept': 'application/json',
                           'Content-Type': 'application/json',
                           'module': 'odin'}
        for pg_no in range(1, total_products_on_page):
            payload = {'deeplinkurl': '/' + category + '?p=' + str(pg_no) + '&cid=tn_' + category.replace('-', '_')}
            yield response.follow(request_url, callback=self.parse_pages, method='POST', body=json.dumps(payload),
                                  headers=request_headers)

    def parse_pages(self, response):
        nnnow_details = NnnowParser()
        products_url_list = json.loads(response.body)['data']['styles']['styleList']
        for product_url in products_url_list:
            product_complete_url = 'https://www.nnnow.com' + product_url['url']
            yield response.follow(product_complete_url, callback=nnnow_details.parse_details)


class NnnowItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    img_urls = scrapy.Field()
    skus = scrapy.Field()
    request_queue = scrapy.Field()


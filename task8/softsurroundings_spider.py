from json import loads
from re import sub
from itertools import product
from six.moves.urllib.parse import urlencode, unquote_plus

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from scrapy.selector import Selector

from softsurroundings.items import Product


class SoftSurroundingsSpider(CrawlSpider):
    name = 'softsurroundings'
    allowed_domains = ['softsurroundings.com']

    start_urls = ['https://www.softsurroundings.com']

    categoy_css = '#menuNav'
    product_css = '.product'
    pagination_css = '.thumbscroll'

    rules = (
        Rule(LinkExtractor(restrict_css=categoy_css), callback='parse_category'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
    )

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {
        'atb': 'add to bag(empty)',
        'suggest': '',
        'wishlist': '',
        'outlier': '0',
        'cartId': '',
        'ajax': '1'
    }

    custom_settings = {
        'DOWNLOAD_DELAY': 6,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/68.0.3440.106 Safari/537.36'
    }

    def parse_category(self, response):
        next_page_css = '[name="page"]::attr(value)'
        prod_keys_css = '[name="docs"]::attr(value)'
        params = {'ajax': '1'}

        next_page_sels = response.css(self.pagination_css)

        for page_sel in next_page_sels:
            next_page = page_sel.css(next_page_css).extract_first()
            prod_keys = page_sel.css(prod_keys_css).extract_first()

            params['docKeys'] = prod_keys
            params['count'] = len(prod_keys.split(','))

            pagination_request_url = f'{response.url}/page-{next_page}/'

            return Request(pagination_request_url, headers=self.headers, method="POST",
                           body=urlencode(params), callback=self.parse_pagination)

    def parse_pagination(self, response):
        raw_prod_content = loads(response.text).get('content')
        product_css = f'{self.product_css} a::attr(href)'
        product_urls = Selector(text=raw_prod_content).css(product_css).extract()

        for url in product_urls:
            yield response.follow(url, callback=self.parse_product)

    def parse_product(self, response):
        product_item = Product()

        product_item['gender'] = self.extract_gender(response)
        product_item['name'] = self.extract_product_name(response)
        product_item['image_urls'] = self.extract_image_urls(response)
        product_item['retailer_sku'] = self.extract_retailer_sku(response)
        product_item['description'] = self.extract_description(response)
        product_item['category'] = self.extract_categories(response)
        product_item['url'] = self.extract_product_url(response)
        product_item['brand'] = self.extract_brand(response)
        product_item['care'] = self.extract_care(response)

        product_item['requests_queue'] = self.extract_skus_requests(response)

        return self.follow_or_extract_sku(product_item, response)

    def follow_or_extract_sku(self, product_item, response):
        sku_requests = product_item.get("requests_queue")

        product_item['skus'] = []

        if not sku_requests:
            return self.extract_single_sku(product_item, response)

        return self.requests_to_follow(product_item)

    def extract_skus_requests(self, response):
        raw_color_ids = response.css('#color .swatchlink img::attr(id)').extract()
        raw_size_ids = response.css('#size a::attr(id)').extract()

        if not raw_size_ids and not raw_color_ids:
            return []

        color_sels = response.css('#color .swatchlink')
        size_sels = response.css('#size a')

        parent_id_css = '[name="parentId"]::attr(value)'
        parent_id = response.css(parent_id_css).extract_first().lower()

        unique_id_css = '[name="uniqid"]::attr(value)'
        unique_id = response.css(unique_id_css).extract_first()

        if not color_sels:
            color_id_css = f'input[name="specOne-{unique_id}"]::attr(value)'
            color_sels = response.css(color_id_css).extract()

        if not size_sels:
            size_id_css = f'input[name="specTwo-{unique_id}"]::attr(value)'
            size_sels = response.css(size_id_css).extract()

        params = self.params.copy()
        params[f'sizecat-{unique_id}'] = parent_id
        params['sizecat_desc'] = parent_id
        params[f'quantity-{unique_id}'] = '1'
        params['uniqid'] = unique_id
        params['parentId'] = parent_id

        requests_to_follow = []
        for color_sel, size_sel in product(color_sels, size_sels):

            meta = {}

            color_id = color_sel
            if isinstance(color_sel, Selector):
                color_id = color_sel.css('img::attr(id)').extract_first()
                meta['color_id'] = color_id
                meta['color'] = color_sel.css(' ::text').extract_first()
                color_id = color_id.split("_")[1]

            size_id = size_sel
            if isinstance(size_sel, Selector):
                size_id = size_sel.css('::attr(id)').extract_first()
                size_id = size_id.split("_")[1]
                meta['size'] = size_sel.css(' ::text').extract_first()

            params = params.copy()
            params[f'specOne-{unique_id}'] = color_id
            params[f'specTwo-{unique_id}'] = size_id
            params[f'sku_{parent_id}'] = f'{parent_id}{color_id}{size_id}'

            sku_request_url = f'https://www.softsurroundings.com/p/{parent_id}/{color_id}{size_id}'
            request = Request(sku_request_url, meta=meta, headers=self.headers, body=urlencode(params),
                              method="POST", callback=self.parse_skus)

            requests_to_follow.append(request)

        return requests_to_follow

    def requests_to_follow(self, product_item):
        next_requests = product_item.get("requests_queue")

        if next_requests:
            request = next_requests.pop()
            request.meta['item'] = product_item
            return request

        del product_item["requests_queue"]

        return product_item

    def parse_skus(self, response):
        product_item = response.meta.get('item')
        product_item["skus"].append(self.extract_sku(response))
        return self.requests_to_follow(product_item)

    def extract_sku(self, response):
        raw_product = loads(response.text)
        raw_prod_header = Selector(text=unquote_plus(raw_product.get('productHeader')))
        raw_sku_sel = Selector(text=unquote_plus(raw_product.get('productBulk')))
        sku = dict()

        price_css = '[itemprop="price"]::text'
        sku['price'] = raw_prod_header.css(price_css).extract_first()

        currency_css = '[itemprop="priceCurrency"]::text'
        sku['currency'] = raw_prod_header.css(currency_css).extract_first()

        prod_color = response.meta.get('color', '')
        prod_size = response.meta.get('size', 'One Size')
        sku['color'] = prod_color
        sku['size'] = prod_size
        sku['sku_id'] = f'{prod_color}_{prod_size}'

        raw_prev_price = response.css('.ctntPrice::text').re('Was([^;]+)')

        if raw_prev_price:
            sku['previous_price'] = [raw_prev_price[0].strip()[1:]]

        stock_css = '#orderProcessError::text'
        prod_stock_status = raw_sku_sel.css(stock_css)
        if prod_stock_status:
            sku['out_of_stock'] = True

        return sku

    def extract_single_sku(self, product_item, response):
        size_css = '#size .basesize::text'
        prod_size = response.css(size_css).extract_first(default='One Size')

        color_css = '#color .basesize::text'
        prod_color = response.css(color_css).extract_first()

        sku = dict()
        price_css = '[itemprop="price"]::text'
        sku['price'] = response.css(price_css).extract_first()

        currency_css = '[itemprop="priceCurrency"]::text'
        sku['currency'] = response.css(currency_css).extract_first()

        sku['color'] = prod_color
        sku['size'] = prod_size
        sku['sku_id'] = f'{prod_color}_{prod_size}'

        raw_prev_price = response.css('.ctntPrice::text').re('Was([^;]+)')

        if raw_prev_price:
            sku['previous_price'] = [raw_prev_price[0].strip()[1:]]

        stock_css = '.stockStatus .basesize::text'
        raw_stock_status = response.css(stock_css).extract_first()

        if raw_stock_status != 'In Stock.':
            sku['out_of_stock'] = True

        product_item['skus'].append(sku)

        del product_item["requests_queue"]

        return product_item

    def extract_gender(self, response):
        if 'bedding' in ' '.join(self.extract_categories(response)).lower():
            return "Unisex"
        return "Women"

    def extract_image_urls(self, response):
        prod_images_css = '#detailAltImgs ::attr(src)'
        raw_images = response.css(prod_images_css).extract()
        return [sub('\/(\d*x\d*)\/', '/1200x1802/', raw_image) for raw_image in raw_images]

    def extract_product_name(self, response):
        prod_name_css = '[itemprop="name"]::text'
        return response.css(prod_name_css).extract_first()

    def extract_care(self, response):
        care_css = '#careAndContentInfo span::text, #directionsInfo ::text'
        return response.css(care_css).extract()

    def extract_description(self, response):
        desc_css = '.productInfo>:not(.productInfoDetails) ::text ,.productInfo ::text'
        raw_desc = response.css(desc_css).extract()
        return [desc for desc in raw_desc if desc.strip() != 'Description & Details']

    def extract_retailer_sku(self, response):
        prod_sku_css = '[itemprop="productID"]::text'
        return response.css(prod_sku_css).extract_first()

    def extract_brand(self, response):
        brand_css = '.productInfoDetails li:contains("Designed by")::text,' \
                    '#aboutbrandInfo img::attr(alt)'
        raw_brand = response.css(brand_css).extract_first(default='Soft Surroundings')
        return raw_brand.replace('Designed by', '').strip()

    def extract_product_url(self, response):
        return response.url

    def extract_categories(self, response):
        category_css = '.pagingBreadCrumb ::text'
        raw_categories = response.css(category_css).extract()
        return [raw_cat for raw_cat in raw_categories if '/' != raw_cat.strip()]

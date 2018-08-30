from json import loads
from re import sub
from itertools import product
from six.moves.urllib.parse import unquote_plus, urljoin

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest
from scrapy.selector import Selector

from softsurroundings.items import Product


class SoftSurroundingsSpider(CrawlSpider):
    name = 'softsurroundings'
    allowed_domains = ['softsurroundings.com']

    start_urls = ['https://www.softsurroundings.com/']

    categoy_css = '#menuNav'
    product_css = '.product'
    pagination_css = '.thumbscroll'

    rules = (
        Rule(LinkExtractor(restrict_css=categoy_css), callback='parse_category'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
    )

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

            pagination_request_url = urljoin(response.url, f'page-{next_page}/')
            yield FormRequest(pagination_request_url, formdata=params, callback=self.parse_pagination)

    def parse_pagination(self, response):
        raw_prod_content = loads(response.text)['content']
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

        return self.requests_to_follow(product_item)

    def requests_to_follow(self, product_item):
        next_requests = product_item.get("requests_queue")

        if next_requests:
            request = next_requests.pop()
            request.meta['item'] = product_item
            return request

        del product_item["requests_queue"]

        return product_item

    def extract_skus_requests(self, response):
        unique_id = response.css('[name="uniqid"]::attr(value)').extract_first()
        parent_id = response.css('[name="parentId"]::attr(value)').extract_first().lower()

        color_id_css = f'#color .swatchlink img::attr(data-value),' \
                       f'input[name="specOne-{unique_id}"]::attr(value)'
        color_ids = response.css(color_id_css).extract()
        color_ids = set(filter(None, color_ids))

        size_ids = response.css('#size a.size::attr(id)').extract() or ['size_000']
        size_ids = set(filter(None, size_ids))

        params = {'ajax': '1', f'sizecat-{unique_id}': parent_id, 'sizecat_desc': parent_id,
                  f'quantity-{unique_id}': '1', 'uniqid': unique_id, 'parentId': parent_id}

        requests_to_follow = []
        for color_id, size_id in product(color_ids, size_ids):

            color_css = f'img[data-value="{color_id}"]::attr(alt),#color .sizetbs .basesize::text'
            size_css = f'a[id="{size_id}"]::text,#size .sizetbs .basesize::text'

            meta = {'color': response.css(color_css).extract_first(default=''),
                    'size': response.css(size_css).extract_first(default='One Size')}

            size_id = size_id.split("_")[1]
            params = params.copy()
            params[f'specOne-{unique_id}'] = color_id
            params[f'specTwo-{unique_id}'] = size_id
            params[f'sku_{parent_id}'] = f'{parent_id}{color_id}{size_id}'

            sku_request_url = f'https://www.softsurroundings.com/p/{parent_id}/{color_id}{size_id}'
            request = FormRequest(sku_request_url, meta=meta, formdata=params,
                                  callback=self.parse_skus)

            requests_to_follow.append(request)

        return requests_to_follow

    def parse_skus(self, response):
        product_item = response.meta['item']
        product_item["skus"] = product_item.get('skus', []) + self.extract_sku(response)
        return self.requests_to_follow(product_item)

    def extract_sku(self, response):
        raw_product = loads(response.text)
        raw_prod_header = Selector(text=unquote_plus(raw_product['productHeader']))
        raw_sku_sel = Selector(text=unquote_plus(raw_product['productBulk']))

        sku = {'currency': raw_prod_header.css('[itemprop="priceCurrency"]::text').extract_first(),
               'price': raw_prod_header.css('[itemprop="price"]::text').extract_first()}

        prod_color = response.meta['color']
        prod_size = response.meta['size']
        sku['color'] = prod_color
        sku['size'] = prod_size
        sku['sku_id'] = f'{prod_color}_{prod_size}'

        raw_prev_price = response.css('.ctntPrice::text').re('Was([^;]+)')

        if raw_prev_price:
            sku['previous_price'] = [raw_prev_price[0].strip()[1:]]

        prod_stock_status = raw_sku_sel.css('.stockStatus .basesize::text').extract_first()
        if prod_stock_status != 'In Stock.':
            sku['out_of_stock'] = True

        return [sku]

    def extract_gender(self, response):
        if 'bedding' in ' '.join(self.extract_categories(response)).lower():
            return "Unisex"
        return "Women"

    def extract_image_urls(self, response):
        raw_images = response.css('#detailAltImgs ::attr(src)').extract()
        return [sub('\/(\d*x\d*)\/', '/1200x1802/', raw_image) for raw_image in raw_images]

    def extract_product_name(self, response):
        return response.css('[itemprop="name"]::text').extract_first()

    def extract_care(self, response):
        care_css = '#careAndContentInfo span::text, #directionsInfo ::text'
        return response.css(care_css).extract()

    def extract_description(self, response):
        desc_css = '.productInfo>:not(.productInfoDetails) ::text ,.productInfo ::text'
        raw_desc = response.css(desc_css).extract()
        return [desc for desc in raw_desc if desc.strip() != 'Description & Details']

    def extract_retailer_sku(self, response):
        return response.css('[itemprop="productID"]::text').extract_first()

    def extract_brand(self, response):
        brand_css = '.productInfoDetails li:contains("Designed by")::text,' \
                    '#aboutbrandInfo img::attr(alt)'
        raw_brand = response.css(brand_css).extract_first(default='Soft Surroundings')
        return raw_brand.replace('Designed by', '').strip()

    def extract_product_url(self, response):
        return response.url

    def extract_categories(self, response):
        raw_categories = response.css('.pagingBreadCrumb ::text').extract()
        return [raw_cat for raw_cat in raw_categories if '/' != raw_cat.strip()]

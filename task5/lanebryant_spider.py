from json import loads
from urllib.parse import parse_qsl
from itertools import product
from re import findall

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest
from scrapy.selector import Selector

from lanebryant.items import Product


class LanebryantSpider(CrawlSpider):
    name = 'lanebryant'

    gender = "Women"
    care_words = ['Clean', 'Wash', '%']

    listing_css = '.mar-subnav-links-column'
    product_css = '[tabindex]'
    pagination_css = '.mar-pagination'

    pagination_url = 'https://www.lanebryant.com/lanebryant/plp/includes/plp-filters.jsp'

    start_urls = ['https://www.lanebryant.com/']
    allowed_domains = ['lanebryant.com']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, allow='.*\/view-all\/.*', deny='#0'),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css, deny='#0'),
             callback='parse_product'),
        Rule(LinkExtractor(restrict_css=pagination_css, allow='N=.*'),
             process_request='pagination_request', callback='parse_pagination')
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 4,
    }

    def pagination_request(self, request):
        next_page = findall('N.*', request.url).pop()
        return FormRequest(LanebryantSpider.pagination_url, formdata=dict(parse_qsl(next_page)),
                           callback=self.parse_pagination)

    def validate_parameter(func):
        def validate(self, parameter):
            if parameter:
                return func(self, parameter)

        return validate

    def parse_pagination(self, response):
        product_grid = loads(response.text).get('product_grid', {})
        html_content = product_grid.get('html_content', "")

        product_css = '[tabindex]::attr(href)'
        product_urls = Selector(text=html_content).css(product_css).extract()

        for url in product_urls:
            yield response.follow(url, callback=self.parse_product)

    def parse_product(self, response):
        raw_product = self.get_raw_product(response)
        raw_sku = self.get_raw_skus(response)

        product_item = Product()

        product_item['brand'] = self.get_brand(raw_product)
        product_item['name'] = self.get_product_name(raw_product)
        product_item['image_urls'] = self.get_image_urls(raw_product)
        product_item['description'] = self.get_description(raw_product)

        product_item['category'] = self.get_categories(raw_sku)
        product_item['retailer_sku'] = self.get_retailer_sku(raw_sku)

        product_item['skus'] = self.get_skus(response)
        product_item['care'] = self.get_care(response)
        product_item['gender'] = self.get_gender(response)
        product_item['url'] = self.get_product_url(response)

        yield product_item

    def get_raw_product(self, response):
        product_css = 'script[type="application/ld+json"]::text'
        raw_product = response.css(product_css).extract_first()

        if raw_product:
            prev_name = findall('\s*\"name\"\s*:(.+?),', raw_product)
            updated_name = prev_name[0].replace('"', '')
            raw_product = raw_product.replace(prev_name[0], f'"{updated_name}"')
            return loads(raw_product, strict=False)

    def get_raw_skus(self, response):
        sku_css = 'script#pdpInitialData[type="application/json"]::text'
        raw_skus = response.css(sku_css).extract_first()

        if raw_skus:
            return loads(raw_skus, strict=False)

    @validate_parameter
    def get_brand(self, raw_product):
        return raw_product.get('offers', {}).get('seller', {}).get('name')

    @validate_parameter
    def get_product_name(self, raw_product):
        return raw_product.get('name')

    @validate_parameter
    def get_description(self, raw_product):
        raw_desc = raw_product.get('description', '')
        product_desc = Selector(text=raw_desc).css('::text').extract()
        return [line for line in product_desc if 'Item Number' not in line]

    @validate_parameter
    def get_image_urls(self, raw_product):
        return raw_product.get('image')

    @validate_parameter
    def get_retailer_sku(self, raw_sku):
        raw_product = raw_sku.get('pdpDetail', {}).get('product', {})[0]
        return raw_product.get("product_id")

    @validate_parameter
    def get_categories(self, raw_skus):
        raw_product = raw_skus.get('pdpDetail', {}).get('product', {})[0]
        product_specs = raw_product.get("ensightenData", {})[0]
        return product_specs.get("categoryPath", "").split(':')

    def get_care(self, response):
        css = '#tab1 ::text'
        product_desc = response.css(css).extract()

        if product_desc:
            return [line for line in product_desc
                    if any(word in line for word in LanebryantSpider.care_words)]

    def get_gender(self, response):
        return LanebryantSpider.gender

    def get_product_url(self, response):
        return response.url

    def get_skus(self, response):
        raw_product = self.get_raw_product(response)
        price_specs = raw_product.get('offers', {}).get('priceSpecification', {})
        price_currency = price_specs.get('priceCurrency')

        raw_skus = self.get_raw_skus(response)
        raw_skus = raw_skus.get('pdpDetail').get('product')[0]

        available_skus = raw_skus.get('skus')

        if not available_skus or not raw_skus:
            return []

        available_skus_map = {}
        for sku in available_skus:
            available_skus_map[f'{sku.get("color")}_{sku.get("size")}'] = sku
            available_skus_map[sku.get('color')] = sku

        raw_colors = raw_skus.get('all_available_colors')[0]
        raw_sizes = raw_skus.get('all_available_sizes')[0]

        product_skus = []
        for raw_color, raw_size in product(raw_colors.get('values'), raw_sizes.get('values')):
            sku = {}

            raw_sku = available_skus_map.get(f'{raw_color.get("id")}_{raw_size.get("id")}')

            if not raw_sku:
                raw_sku = available_skus_map.get(raw_color.get("id"))
                sku['out_of_stock'] = True

            sku['color'] = raw_color.get('name')
            sku['size'] = raw_size.get('value')
            sku['currency'] = price_currency

            sku['price'] = raw_sku.get('prices').get('sale_price')[1:]
            sku['previous_price'] = [raw_sku.get('prices').get('list_price')[1:]]

            sku['id'] = f'{raw_color.get("name")}_{raw_size.get("value")}'

            product_skus.append(sku)

        return product_skus

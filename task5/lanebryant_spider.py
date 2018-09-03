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
        Rule(LinkExtractor(restrict_css=product_css, deny='#0'), callback='parse_product'),
        Rule(LinkExtractor(restrict_css=pagination_css, allow='N=.*'),
             process_request='pagination_request', callback='parse_pagination')
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 4,
    }

    def pagination_request(self, request):
        next_page = findall('N.*', request.url).pop()
        return FormRequest(self.pagination_url, formdata=dict(parse_qsl(next_page)),
                           callback=self.parse_pagination)

    def parse_pagination(self, response):
        raw_page = loads(response.text)['product_grid']['html_content']

        product_urls = Selector(text=raw_page).css('[tabindex]::attr(href)').extract()

        for url in product_urls:
            yield response.follow(url, callback=self.parse_product)

    def parse_product(self, response):
        raw_product = self.get_raw_product(response)
        raw_sku = self.get_raw_skus(response)

        product_item = Product()

        product_item['brand'] = self.extract_brand(raw_product)
        product_item['name'] = self.extract_product_name(raw_product)
        product_item['image_urls'] = self.extract_image_urls(raw_product)
        product_item['description'] = self.extract_description(raw_product)

        product_item['category'] = self.extract_categories(raw_sku)
        product_item['retailer_sku'] = self.extract_retailer_sku(raw_sku)

        product_item['skus'] = self.extract_skus(response)
        product_item['care'] = self.extract_care(response)
        product_item['gender'] = self.extract_gender(response)
        product_item['url'] = self.extract_product_url(response)

        yield product_item

    def get_raw_product(self, response):
        product_css = 'script[type="application/ld+json"]::text'
        raw_product = response.css(product_css).extract_first()

        prev_name = findall('\s*\"name\"\s*:(.+?),', raw_product)
        updated_name = prev_name[0].replace('"', '')
        raw_product = raw_product.replace(prev_name[0], f'"{updated_name}"')
        return loads(raw_product, strict=False)

    def get_raw_skus(self, response):
        sku_css = 'script#pdpInitialData[type="application/json"]::text'
        raw_skus = response.css(sku_css).extract_first()
        return loads(raw_skus, strict=False)

    def extract_brand(self, raw_product):
        return raw_product['offers']['seller']['name']

    def extract_product_name(self, raw_product):
        return raw_product['name']

    def extract_description(self, raw_product):
        product_desc = Selector(text=raw_product['description']).css('::text').extract()
        return [line for line in product_desc if 'Item Number' not in line]

    def extract_image_urls(self, raw_product):
        return raw_product['image']

    def extract_retailer_sku(self, raw_sku):
        raw_product = raw_sku['pdpDetail']['product'][0]
        return raw_product["product_id"]

    def extract_categories(self, raw_skus):
        product_specs = raw_skus['pdpDetail']['product'][0]["ensightenData"][0]
        return product_specs["categoryPath"].split(':')

    def extract_care(self, response):
        css = '#tab1 ::text'
        product_desc = response.css(css).extract()
        return [line for line in product_desc if any(word in line for word in self.care_words)]

    def extract_gender(self, response):
        return self.gender

    def extract_product_url(self, response):
        return response.url

    def extract_skus(self, response):
        raw_product = self.get_raw_product(response)
        price_specs = raw_product['offers']['priceSpecification']
        price_currency = price_specs['priceCurrency']
        raw_skus = self.get_raw_skus(response)['pdpDetail']['product'][0]
        available_skus = raw_skus.get('skus')

        if not available_skus:
            sku = {'color': '', 'size': 'One Size', 'price': price_specs['price'],
                   'currency': price_currency, 'out_of_stock': True}
            return [sku]

        available_skus_map = {}
        for sku in available_skus:
            available_skus_map[f'{sku.get("color")}_{sku.get("size")}'] = sku
            available_skus_map[sku.get('color')] = sku

        raw_colors = raw_skus['all_available_colors'][0]
        raw_sizes = raw_skus.get['all_available_sizes'][0]

        product_skus = []
        for raw_color, raw_size in product(raw_colors['values'], raw_sizes['values']):
            sku = {}
            raw_sku = available_skus_map.get(f'{raw_color["id"]}_{raw_size["id"]}')

            if not raw_sku:
                raw_sku = available_skus_map.get(raw_color["id"])
                sku['out_of_stock'] = True

            sku['color'] = raw_color['name']
            sku['size'] = raw_size['value']
            sku['currency'] = price_currency
            sku['price'] = raw_sku['prices']['sale_price'][1:]
            sku['previous_price'] = [raw_sku['prices']['list_price'][1:]]
            sku['id'] = f'{raw_color["name"]}_{raw_size["value"]}'

            product_skus.append(sku)

        return product_skus

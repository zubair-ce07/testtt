import json
from urllib.parse import parse_qsl
from itertools import product
import re

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

    pagination_url = 'https://www.lanebryant.com/lanebryant/plp/includes/plp-filters.jsp'

    start_urls = ['https://www.lanebryant.com/']
    allowed_domains = ['lanebryant.com']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, allow='.*\/view-all\/.*', deny='#0'),
             callback='parse_category'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
    }

    def parse_category(self, response):
        product_urls = LinkExtractor(restrict_css='[tabindex]', deny='#0').extract_links(response)

        for link in product_urls:
            yield response.follow(link.url, callback=self.parse_product)

        pages_to_follow = response.css('.mar-pagination a::attr(href)').re('N.*')

        for next_page in set(pages_to_follow):
            yield FormRequest(LanebryantSpider.pagination_url, formdata=dict(parse_qsl(next_page)),
                              callback=self.parse_pagination)

    def parse_pagination(self, response):
        product_grid = json.loads(response.text).get('product_grid', {})
        html_content = product_grid.get('html_content', "")

        product_urls = Selector(text=html_content).css('[tabindex]::attr(href)').extract()

        for url in product_urls:
            yield response.follow(url, callback=self.parse_product)

    def parse_product(self, response):
        product_item = Product()

        product_item['retailer_sku'] = self.get_retailer_sku(response)
        product_item['image_urls'] = self.get_image_urls(response)
        product_item['description'] = self.get_description(response)
        product_item['name'] = self.get_product_name(response)
        product_item['gender'] = self.get_gender(response)
        product_item['category'] = self.get_categories(response)
        product_item['url'] = self.get_product_url(response)
        product_item['brand'] = self.get_brand(response)
        product_item['care'] = self.get_care(response)
        product_item['skus'] = self.get_skus(response)

        yield product_item

    def get_product_name(self, response):
        raw_product = self.get_raw_product(response)

        if raw_product:
            return raw_product.get('name')

    def get_care(self, response):
        product_desc = response.css('#tab1 ::text').extract()

        if product_desc:
            return [line for line in product_desc
                    if any(word in line for word in LanebryantSpider.care_words)]

    def get_description(self, response):
        raw_product = self.get_raw_product(response)

        if raw_product:
            product_desc = Selector(text=raw_product.get('description', '')).css('::text').extract()
            return [line for line in product_desc if 'Item Number' not in line]

    def get_retailer_sku(self, response):
        raw_product = self.get_raw_skus(response)

        if raw_product:
            return raw_product.get('pdpDetail', {}).get('product', {})[0].get("product_id")

    def get_image_urls(self, response):
        raw_product = self.get_raw_product(response)
        if raw_product:
            return raw_product.get('image')

    def get_gender(self, response):
        return LanebryantSpider.gender

    def get_brand(self, response):
        raw_product = self.get_raw_product(response)

        if raw_product:
            return raw_product.get('offers', {}).get('seller', {}).get('name')

    def get_product_url(self, response):
        return response.url

    def get_categories(self, response):
        raw_skus = self.get_raw_skus(response)

        if raw_skus:
            product_specs = raw_skus.get('pdpDetail', {}).get('product', {})[0]
            return product_specs.get("ensightenData", {})[0].get("categoryPath", "").split(':')

    def get_raw_skus(self, response):
        sku_css = 'script#pdpInitialData[type="application/json"]::text'
        raw_skus = response.css(sku_css).extract_first()

        if raw_skus:
            return json.loads(raw_skus, strict=False)

    def get_raw_product(self, response):
        product_css = 'script[type="application/ld+json"]::text'
        raw_product = response.css(product_css).extract_first()

        if raw_product:
            prev_name = re.findall('\s*\"name\"\s*:(.+?),', raw_product)
            updated_name = prev_name[0].replace('"', '')
            return json.loads(raw_product.replace(prev_name[0], '"' + updated_name + '"'), strict=False)

    def get_skus(self, response):
        raw_product = self.get_raw_product(response)
        raw_skus = self.get_raw_skus(response)

        available_skus = raw_skus.get('pdpDetail').get('product')[0].get('skus')

        if not available_skus:
            return []

        colors = raw_skus.get('pdpDetail').get('product')[0].get('all_available_colors')
        colors = dict(zip([i.get('id') for i in colors[0].get('values')],
                          [i.get('name') for i in colors[0].get('values')]))

        sizes = raw_skus.get('pdpDetail').get('product')[0].get('all_available_sizes')
        sizes = dict(zip([i.get('id') for i in sizes[0].get('values')],
                         [i.get('value') for i in sizes[0].get('values')]))

        product_skus = []
        for color, size in product(colors.keys(), sizes.keys()):
            sku = {}
            raw_sku = next((raw_sku for raw_sku in available_skus if raw_sku['color'] == color
                            and raw_sku['size'] == size), None)
            if not raw_sku:
                raw_sku = next((raw_sku for raw_sku in available_skus if raw_sku['color'] == color),
                               None)
                sku['out_of_stock'] = True

            sku['color'] = colors.get(color)
            sku['size'] = sizes.get(size)
            sku['id'] = '{}_{}'.format(colors.get(color), sizes.get(size))

            sku['price'] = raw_sku.get('prices').get('sale_price')[1:]
            sku['previous_price'] = [raw_sku.get('prices').get('list_price')[1:]]
            if raw_product:
                price_specs = raw_product.get('offers', {}).get('priceSpecification', {})
                sku['currency'] = price_specs.get('priceCurrency')

            product_skus.append(sku)

        return product_skus

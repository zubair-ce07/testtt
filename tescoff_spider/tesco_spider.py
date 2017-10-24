import json
import re

from scrapy import Selector, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TescoGarments(CrawlSpider):
    name = "tescoff-uk-crawl"

    start_urls = ['https://www.tesco.com/direct/clothing']

    listing_css = '.products'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        category_id = self.get_category_id(response)
        if not category_id:
            return super().parse(response)

        category_url_pattern = 'https://www.tesco.com/direct/blocks/catalog/productlisting/infiniteBrowse.jsp?' \
                               'catId={}&currentPageType=Category&imagePreset=imagePreset-portrait&' \
                               'lazyload=true&pageViewType=grid&segmentCount=3&sortBy=1&view=grid&offset={}'

        total_garments = self.get_garments_count(response)

        for offset in range(0, total_garments, 20):
            url = category_url_pattern.format(category_id, offset)
            yield Request(url=url, callback=self.parse_category)

    def get_category_id(self, response):
        category_id_css = '.products-wrapper::attr(data-endecaid)'
        return response.css(category_id_css).extract_first()

    def get_garments_count(self, response):
        garments_count_css = '.filter-productCount b::text'
        return int(response.css(garments_count_css).extract_first())

    def parse_category(self, response):
        raw_garments = json.loads(response.text).get('products')
        if not raw_garments:
            return

        garments_response = Selector(text=raw_garments)
        garment_links = self.get_garment_links(garments_response)

        for garment_link in garment_links:
            yield response.follow(url=garment_link, callback=self.parse_garment)

    def get_garment_links(self, response):
        garment_links_css = '.thumbnail::attr(href)'
        return response.css(garment_links_css).extract()

    def parse_garment(self, response):
        retailer_sku = self.get_retailer_sku(response)
        raw_garment = self.get_raw_garment(response)

        gender = raw_garment.get('dynamicAttributes', {'gender': 'unisex'})['gender']
        price = raw_garment['prices'].get('price')

        garment = dict()

        garment['name'] = raw_garment['displayName']
        garment['brand'] = raw_garment['brand']
        garment['retailer_sku'] = retailer_sku
        garment['url_original'] = response.url
        garment['gender'] = gender
        garment['market'] = 'UK'
        garment['currency'] = 'GBP'
        garment['retailer'] = 'tescoff-uk'
        garment['spider_name'] = 'tescoff-uk-crawl'
        garment['skus'] = self.parse_skus(raw_garment)
        garment['price'] = self.get_min_units(price)
        garment['category'] = self.get_garment_category(response)

        meta_data = {'garment': garment}
        sku_code = self.get_garment_sku(response)
        garment_sku_base_link = 'https://www.tesco.com//direct/rest/content/catalog/sku/{}'
        garment_sku_link = garment_sku_base_link.format(sku_code)

        return Request(url=garment_sku_link, callback=self.parse_garment_detail, meta=meta_data)

    def get_retailer_sku(self, response):
        retailer_sku_css = 'meta[property="og:upc"]::attr(content)'
        return response.css(retailer_sku_css).extract_first()

    def get_raw_garment(self, response):
        garment_css = '#ssb_block_10 script::text'
        raw_garment = response.css(garment_css).extract_first()
        garment = re.findall('product\s*=\s*{[.\s\S]*}\s*}\s*\]\s*}',
                             raw_garment)
        return json.loads(garment[0].replace('product =', ''))

    def parse_skus(self, raw_garment):
        price = raw_garment['prices'].get('price')
        previous_price = raw_garment['prices'].get('was', '')
        raw_skus = raw_garment['links']

        skus = {}
        sku_template = {
            'currency': 'GBP',
            'price': self.get_min_units(price)
        }
        if previous_price:
            converted_price = self.get_min_units(previous_price)
            sku_template['previous_price'] = [converted_price]

        for raw_sku in raw_skus:
            if raw_sku['type'] != 'sku':
                continue

            sku = sku_template.copy()
            sku['sku_id'] = raw_sku['id']
            sku['color'] = raw_sku['options'].get('primary')
            sku['size'] = raw_sku['options'].get('secondary')
            skus[raw_sku['id']] = sku

        return list(skus.values())

    def get_garment_category(self, response):
        category_css = '#breadcrumb-v2 a ::text'
        category = self.remove_empty_entries(response.css(category_css).extract())[1:-1]
        return category

    def get_garment_sku(self, response):
        sku_css = '#skuIdVal::attr(value)'
        return response.css(sku_css).extract_first()

    def parse_garment_detail(self, response):
        garment = response.meta['garment']
        raw_garment_details = json.loads(response.text)
        garment['care'] = self.parse_care(raw_garment_details)
        garment['image_urls'] = self.parse_images(raw_garment_details)
        garment['description'] = self.parse_description(raw_garment_details)
        if not garment['gender']:
            garment['gender'] = self.parse_gender(raw_garment_details)

        return garment

    def parse_images(self, raw_garment_details):
        product_gallery = raw_garment_details['mediaAssets']['skuMedia']
        image_url_attr = '{}&wid=1400&hei=2000'
        image_urls = [image_url_attr.format(image_url['src'].split('$')[0])
                      for image_url in product_gallery if image_url.get('mediaType') == 'Large']
        return image_urls

    def parse_care(self, raw_garment_details):
        care_details = raw_garment_details['specification'].get('Material', [])
        care = [care.get('description') for care in care_details if care.get('attr') == 'material']
        return care

    def parse_gender(self, raw_garment_details):
        garment_detail = raw_garment_details['specification'].get('Key Information', [])
        gender = [gender['description'] for gender in garment_detail if gender['attr'] == 'gender']
        return gender[0] if gender else 'unisex'

    def parse_description(self, raw_garment_details):
        raw_description = raw_garment_details['longDescription']
        description = Selector(text=raw_description)
        return self.remove_empty_entries(description.css('::text').extract())

    def get_min_units(self, price):
        return int(float(price)*100) if price else None

    def remove_empty_entries(self, content):
        return [entry.strip() for entry in content if entry.strip()]

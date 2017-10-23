import json
import re
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TescoGarments(CrawlSpider):
    name = "tescoff-uk-crawl"

    start_urls = ['https://www.tesco.com/direct/clothing']

    visited_garments = []

    listing_css = '.products'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        category_id = self.get_category_id(response)
        if not category_id:
            super().parse(response)
            return

        category_url_pattern = 'https://www.tesco.com/direct/blocks/catalog/productlisting/infiniteBrowse.jsp?' \
                               'catId={}&currentPageType=Category&imagePreset=imagePreset-portrait&' \
                               'lazyload=true&pageViewType=grid&segmentCount=3&sortBy=1&view=grid&offset={}'

        total_garments = self.get_garments_count(response)
        offset = 0
        while offset <= total_garments:
            url = category_url_pattern.format(category_id, offset)
            yield scrapy.Request(url=url, callback=self.parse_category)
            offset += 20

    def parse_category(self, response):
        raw_garments = json.loads(response.text).get('products')
        if not raw_garments:
            return
        garments_response = scrapy.Selector(text=raw_garments)
        garment_links = self.get_garment_links(garments_response)

        for garment_link in garment_links:
            yield response.follow(url=garment_link, callback=self.parse_garment)

    def parse_garment(self, response):
        raw_garment = self.get_raw_garment(response)

        retailer_sku = self.get_retailer_sku(response)
        if retailer_sku in self.visited_garments:
            return

        self.visited_garments.append(retailer_sku)

        gender = raw_garment.get('dynamicAttributes', {'gender': ''})['gender']
        price = raw_garment['prices'].get('price')

        garment = dict()

        garment['retailer_sku'] = retailer_sku
        garment['brand'] = raw_garment['brand']
        garment['name'] = raw_garment['displayName']
        garment['skus'] = self.parse_skus(raw_garment)
        garment['category'] = self.get_garment_category(response)
        garment['description'] = self.get_garment_description(response)
        garment['url_original'] = response.url
        garment['price'] = self.get_converted_price(price)
        garment['gender'] = gender
        garment['currency'] = 'GBP'
        garment['spider_name'] = 'tescoff-uk-crawl'
        garment['retailer'] = 'tescoff-uk'
        garment['market'] = 'UK'

        meta_data = {'garment': garment}
        sku_code = self.get_garment_sku(response)
        garment_sku_base_link = 'https://www.tesco.com//direct/rest/content/catalog/sku/{}'
        garment_sku_link = garment_sku_base_link.format(sku_code)

        return scrapy.Request(url=garment_sku_link, callback=self.parse_gender_care_images_desc, meta=meta_data)

    def parse_gender_care_images_desc(self, response):
        garment = response.meta['garment']
        garment['image_urls'] = self.parse_images(response)
        garment['care'] = self.parse_care(response)
        if not garment['gender']:
            garment['gender'] = self.parse_gender(response)[0]
        if not garment['description']:
            garment['description'] = self.parse_description(response)
        return garment

    def parse_images(self, response):
        raw_images = json.loads(response.text)
        product_gallery = raw_images['mediaAssets']['skuMedia']
        image_url_attr = '{}&wid=1400&hei=2000'
        return [image_url_attr.format(image_url['src'].split('$')[0])
                for image_url in product_gallery if image_url.get('mediaType') == 'Large']

    def parse_gender(self, response):
        raw_gender = json.loads(response.text)
        gender_detail = raw_gender['specification'].get('Key Information', [])
        return [gender['description'] for gender in gender_detail if gender['attr'] == 'gender']

    def parse_care(self, response):
        raw_care = json.loads(response.text)
        care_details = raw_care['specification'].get('Material', [])
        care = []
        for care_detail in care_details:
            if care_detail.get('attr', '') != 'material':
                continue
            care.append(care_detail.get('description'))
        return care

    def parse_description(self, response):
        raw_description = json.loads(response.text)
        description = raw_description['longDescription']
        return description.replace('<p>', '').replace('</p>', '').split('.')

    def parse_skus(self, raw_garment):
        price = raw_garment['prices'].get('price')
        previous_price = raw_garment['prices'].get('was', '')
        raw_skus = raw_garment['links']

        size_color_detail = []
        skus = {
            'currency': 'GBP',
            'price': self.get_converted_price(price),
            'previous_price': [previous_price] if previous_price else []
        }

        for raw_sku in raw_skus:
            if raw_sku['type'] != 'sku':
                continue
            skus['sku_id'] = raw_sku['id']
            skus['color'] = raw_sku['options']['primary']
            skus['size'] = raw_sku['options']['secondary']
            size_color_detail.append(skus.copy())

        return size_color_detail

    def get_raw_garment(self, response):
        garment_css = '#ssb_block_10 script::text'
        raw_garment = response.css(garment_css).extract_first()
        garment = re.findall('product\s*=\s*{[.\s\S]*}\s*}\s*\]\s*}',
                             raw_garment)
        return json.loads(garment[0].replace('product =', ''))

    def get_retailer_sku(self, response):
        retailer_sku_css = 'meta[property="og:upc"]::attr(content)'
        return response.css(retailer_sku_css).extract_first()

    def get_category_id(self, response):
        category_id_css = '.products-wrapper::attr(data-endecaid)'
        return response.css(category_id_css).extract_first()

    def get_garments_count(self, response):
        garments_count_css = '.filter-productCount b::text'
        return int(response.css(garments_count_css).extract_first())

    def get_garment_links(self, response):
        garment_links_css = '.thumbnail::attr(href)'
        return response.css(garment_links_css).extract()

    def get_garment_description(self, response):
        details_css = 'div[itemprop="description"]::text'
        garment_details = response.css(details_css).extract_first()
        description = garment_details.split('.') if garment_details else []
        return self.remove_empty_entries(description)

    def get_garment_category(self, response):
        category_css = '#breadcrumb-v2 a ::text'
        return self.remove_empty_entries(response.css(category_css).extract())[1:-1]

    def get_garment_sku(self, response):
        sku_css = '#skuIdVal::attr(value)'
        return response.css(sku_css).extract_first()

    def get_converted_price(self, price):
        if price:
            return int(float(price)*100)

    def remove_empty_entries(self, content):
        return [entry.strip() for entry in content if entry.strip()]

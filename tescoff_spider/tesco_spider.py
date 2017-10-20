import json
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TescoGarments(CrawlSpider):
    name = "tescoff-uk-crawl"

    start_urls = ['https://www.tesco.com/direct/clothing-accessories/mens-casual-shirts/cat38670012.cat?icid=ClothingDept_lhn_MensCasualShirts']

    product_css = '.image-container'
    listing_css = '.products'

    rules = (
        # Rule(LinkExtractor(restrict_css=listing_css), callback='parse_listing'),
        #Rule(LinkExtractor(restrict_css=product_css), callback='parse_garment'),
    )

    care_words = ['bleach', 'dry', 'iron', 'clean', 'cycle', '%']

    def parse(self, response):
        category_id = response.css('.products-wrapper::attr(data-endecaid)').extract_first()
        if not category_id:
            super().parse(response)
            return

        base_url = 'https://www.tesco.com/direct/blocks/catalog/productlisting/infiniteBrowse.jsp?' \
                   'catId={}&currentPageType=Category&imagePreset=imagePreset-portrait&' \
                   'lazyload=true&pageViewType=grid&segmentCount=3&sortBy=1&view=grid&offset={}'
        total_garments = int(response.css('.filter-productCount b::text').extract_first())
        offset = 0
        while offset < total_garments + 20:
            url = base_url.format(category_id, offset)
            yield scrapy.Request(url=url, callback=self.parse_category)
            offset += 20

    def parse_category(self, response):
        raw_garments = json.loads(response.text).get('products')
        if not raw_garments:
            return
        garments_response = scrapy.Selector(text=raw_garments)
        return {'links': garments_response.css('.thumbnail::attr(href)').extract()}

    def parse_garment(self, response):
        raw_garment = self.get_raw_garment(response)
        gender = raw_garment['dynamicAttributes']['gender']

        garment = dict()

        garment['retailer_sku'] = self.get_retailer_sku(response)
        garment['brand'] = raw_garment['brand']
        garment['name'] = raw_garment['displayName']
        garment['skus'] = self.parse_skus(raw_garment)
        garment['category'] = self.get_garment_category(response)
        garment['description'] = self.get_garment_description(response)
        garment['url_original'] = response.url
        garment['price'] = raw_garment['prices']['price']
        garment['gender'] = gender
        garment['currency'] = 'GBP'
        garment['spider_name'] = 'tescoff-uk-crawl'
        garment['retailer'] = 'tescoff-uk'
        garment['market'] = 'UK'

        meta = {'garment': garment}
        sku_code = self.get_garment_sku(response)
        garment_sku_base_link = 'https://www.tesco.com//direct/rest/content/catalog/sku/{}'
        garment_sku_link = garment_sku_base_link.format(sku_code)

        return scrapy.Request(url=garment_sku_link, callback=self.parse_care_images, meta=meta)
        # return garment

    def parse_care_images(self, response):
        garment = response.meta['garment']
        garment['image_urls'] = self.parse_images(response)
        garment['care'] = self.parse_care(response)
        return garment

    def parse_skus(self, raw_garment):
        price = raw_garment['prices'].get('price', 'N/A')
        previous_price = raw_garment['prices'].get('was', '')
        raw_skus = raw_garment['links']

        size_color_detail = []
        skus = {
            'currency': 'GBP',
            'price': price,
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

    def parse_images(self, response):
        raw_images = json.loads(response.text)
        product_gallery = raw_images['mediaAssets']['skuMedia']
        image_url_attr = '{}&wid=1400&hei=2000'
        return [image_url_attr.format(image_url['src'].split('$')[0])
                for image_url in product_gallery]

    def parse_care(self, response):
        raw_care = json.loads(response.text)
        care_details = raw_care['specification'].get('Material', {})
        care = []
        for care_detail in care_details:
            if care_detail.get('attr', '') != 'material':
                continue
            care.append(care_detail.get('description'))
        return care
    # 'product\s*=\s*{[.\s\S]*}\s*}\s*\]\s*}'

    def get_raw_garment(self, response):
        garment_css = '#ssb_block_10 script::text'
        raw_garment = response.css(garment_css).extract_first()
        cleaned_raw_garment = re.findall('product\s*=\s*{[.\s\S]*}\s*}\s*\]\s*}', raw_garment)
        return json.loads(cleaned_raw_garment[0].replace('product =', ''))

    def get_retailer_sku(self, response):
        retailer_sku_css = 'meta[property="og:upc"]::attr(content)'
        return response.css(retailer_sku_css).extract_first()

    def get_brand(self, response):
        brand_css = '.col-12 h2 span a::text'
        return response.css(brand_css).extract_first()

    def get_garment_name(self, response):
        name_css = '.col-12 h3::text'
        return response.css(name_css).extract_first()

    def get_garment_details(self, response):
        details_css = '.details li::text'
        details = response.css(details_css).extract()
        fabric_css = '#materials p ::text'
        garment_fabric = self.remove_empty_entries(response.css(fabric_css).extract())
        details += [garment_fabric[0]] if garment_fabric else []
        return details

    def get_garment_description(self, response):
        details_css = 'div[itemprop="description"]::text'
        garment_details = response.css(details_css).extract_first()
        description = garment_details.split('.') if garment_details else []
        return self.remove_empty_entries(description)

    def get_garment_care(self, response):
        garment_details = self.get_garment_details(response)
        return [garment_detail for garment_detail in garment_details
                if self.is_care(garment_detail)]

    def get_garment_category(self, response):
        category_css = '#breadcrumb-v2 a ::text'
        return self.remove_empty_entries(response.css(category_css).extract())[1:-1]

    def get_garment_sku(self, response):
        sku_css = '#skuIdVal::attr(value)'
        return response.css(sku_css).extract_first()

    def is_care(self, sentence):
        sentence_lower = sentence.lower()
        return any(care_word in sentence_lower for care_word in self.care_words)

    def remove_empty_entries(self, content):
        return [entry.strip() for entry in content if entry.strip()]
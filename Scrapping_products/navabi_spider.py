import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NavabiGarments(CrawlSpider):
    name = "navabi-uk-crawl"

    start_urls = ['https://www.navabi.co.uk/']

    product_css = '.ProductLink'
    listing_css = ['#mainnav', '.pagination--next']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_garment'),
    )

    care_words = ['bleach', 'dry', 'iron', 'clean', 'cycle', '%']

    def parse_garment(self, response):
        garment = dict()

        garment['retailer_sku'] = self.get_retailer_sku(response)
        garment['brand'] = self.get_brand(response)
        garment['name'] = self.get_garment_name(response)
        garment['category'] = self.get_garment_category(response)
        garment['description'] = self.get_garment_description(response)
        garment['care'] = self.get_garment_care(response)
        garment['url_original'] = response.url
        garment['currency'] = self.get_garment_currency(response)
        garment['price'] = self.get_garment_price(response)
        garment['spider_name'] = 'navabi-uk-crawl'
        garment['retailer'] = 'navabi-uk'
        garment['gender'] = 'women'
        garment['market'] = 'UK'

        meta = {'garment': garment}
        color_code = self.get_garment_color(response)
        garment_link_pattern = 'https://www.navabi.co.uk/product-information/?item-id={}-{}'
        garment_info_link = garment_link_pattern.format(garment['retailer_sku'], color_code)

        return scrapy.Request(url=garment_info_link, callback=self.parse_skus_images, meta=meta)

    def parse_skus_images(self, response):
        garment = response.meta['garment']
        garment['skus'] = self.parse_skus(response)
        garment['image_urls'] = self.parse_images(response)
        return garment

    def parse_skus(self, response):
        garment = response.meta['garment']

        raw_skus = json.loads(response.text)
        color = raw_skus['color']

        garment_sizes = raw_skus['measurementInfo'].keys()
        size_color_detail = list()

        sku_template = {
            'currency': garment['currency'],
            'price': garment['price'],
            'color': color
        }

        for size in garment_sizes:
            size_detail = sku_template.copy()
            size_detail['size'] = size
            size_detail['sku_id'] = color + '_' + size
            if float(raw_skus['saleprice']):
                size_detail['previous_prices'] = [raw_skus['price']]

            size_color_detail.append(size_detail)

        return size_color_detail

    def parse_images(self, response):
        raw_images = json.loads(response.text)
        product_gallery = raw_images['galleryImages']
        images_base_url = 'https://www.navabi.co.uk{}'
        return [images_base_url.format(image_url['big'])
                for image_url in product_gallery]

    def get_retailer_sku(self, response):
        retailer_sku_css = '.mainContent input::attr(value)'
        return response.css(retailer_sku_css).extract_first()

    def get_brand(self, response):
        brand_css = 'a[itemprop="brand"]::text'
        return response.css(brand_css).extract_first()

    def get_garment_name(self, response):
        name_css = 'h3[itemprop="name"]::text'
        return response.css(name_css).extract_first()

    def get_garment_details(self, response):
        details_css = '.details li::text'
        details = response.css(details_css).extract()
        fabric_css = '#materials p:first-of-type::text'
        garment_fabric = self.remove_empty_entries(response.css(fabric_css).extract())
        details += garment_fabric
        return details

    def get_garment_description(self, response):
        description_css = '.left-arrow p::text, #orig_description::text, #descr_more::text'
        description = self.remove_empty_entries(response.css(description_css).extract())
        garment_details = self.get_garment_details(response)
        detail_description = [garment_detail for garment_detail in garment_details
                              if not self.is_care(garment_detail)]

        return description + detail_description

    def get_garment_care(self, response):
        garment_details = self.get_garment_details(response)
        return [garment_detail for garment_detail in garment_details
                if self.is_care(garment_detail)]

    def get_garment_category(self, response):
        category_css = '.breadcrumb li:not(.back) a ::text'
        return response.css(category_css).extract()[1:]

    def get_garment_currency(self, response):
        currency_css = 'span[itemprop="priceCurrency"]::attr(content)'
        return response.css(currency_css).extract_first()

    def get_garment_price(self, response):
        price_css = 'span[itemprop="price"]::attr(content)'
        return response.css(price_css).extract_first()

    def get_garment_color(self, response):
        color_css = '#current_colorcode::attr(value)'
        return response.css(color_css).extract_first()

    def is_care(self, sentence):
        sentence_lower = sentence.lower()
        return any(care_word in sentence_lower for care_word in self.care_words)

    def remove_empty_entries(self, content):
        return [entry.strip() for entry in content if entry.strip()]

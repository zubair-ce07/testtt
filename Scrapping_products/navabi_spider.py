import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NavabiGarments(CrawlSpider):
    name = "navabi-uk-crawl"

    start_urls = ['https://www.navabi.co.uk/']

    visited_products = set()

    product_css = ['.ProductLink']
    listing_css = ['#mainnav', '.pagination--next']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_garment'),
    )

    care_words = ['bleach', 'dry', 'iron', 'remove_empty_entries', 'cycle', '%']

    def parse_garment(self, response):
        retailer_sku = self.get_retailer_sku(response)

        if retailer_sku in self.visited_products:
            return

        self.visited_products.add(retailer_sku)

        brand = self.get_brand(response)
        name = self.get_garment_name(response)
        description = self.get_garment_description(response)
        care = self.get_garment_care(response)
        category = self.get_garment_category(response)
        currency = self.get_product_currency(response)
        price = self.get_garment_price(response)

        garment = {
            'retailer_sku': retailer_sku,
            'brand': brand,
            'name': name,
            'category': category,
            'gender': 'women',
            'description': description,
            'care': care,
            'url_original': response.url,
            'currency': currency,
            'price': price,
            'market': 'UK',
            'retailer': 'navabi-uk',
            'spider_name': 'navabi-uk-crawl',
            'image_urls': [],
            'skus': []
        }

        meta = {'product': garment}
        color_code = self.get_garment_color(response)
        garment_link_pattern = 'https://www.navabi.co.uk/product-information/?item-id={}-{}'
        garment_info_link = garment_link_pattern.format(retailer_sku, color_code)

        yield scrapy.Request(url=garment_info_link, callback=self.parse_skus_images, meta=meta)

    def parse_skus_images(self, response):
        garment = response.meta['product']

        skus_images_info = json.loads(response.text)

        color_codes = skus_images_info['colors'].keys()
        color_names = [skus_images_info['colors'][colors_code]['name'] for colors_code in color_codes]

        garment_sizes = skus_images_info['measurementInfo'].keys()
        size_color_detail = list()

        for color in color_names:
            for size in garment_sizes:
                size_detail = {
                    'price': garment['price'],
                    'color': color,
                    'size': size,
                    'currency': garment['currency'],
                    'sku_id': color + '_' + size
                }
                if float(skus_images_info['saleprice']):
                    size_detail['previous_prices'] = [skus_images_info['price']]
                size_color_detail.append(size_detail)

        garment['skus'] = size_color_detail

        product_gallery = skus_images_info['galleryImages']
        images_base_url = 'https://www.navabi.co.uk{}'
        image_urls = [images_base_url.format(image_url['big']) for image_url in product_gallery]

        garment['image_urls'] = image_urls
        yield garment

    def get_retailer_sku(self, response):
        retailer_sku_css = '.mainContent input::attr(value)'
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
        product_fabric = self.remove_empty_entries(response.css('#materials p ::text').extract())
        details += [product_fabric[0] if product_fabric else '']
        return self.remove_empty_entries(details)

    def get_garment_description(self, response, ):
        description_css = '.more-details__accordion-content p::text'
        description = [response.css(description_css).extract_first()]
        garment_details = self.get_garment_details(response)
        description += [garment_detail for garment_detail in garment_details if not self.is_care(garment_detail)]
        return description

    def get_garment_care(self, response):
        garment_details = self.get_garment_details(response)
        return [garment_detail for garment_detail in garment_details if self.is_care(garment_detail)]

    def get_garment_category(self, response):
        category_css = '.breadcrumb a ::text'
        return response.css(category_css).extract()[2:]

    def get_product_currency(self, response):
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

    def remove_empty_entries(self, contents):
        return [content.strip() for content in contents if content.strip()]

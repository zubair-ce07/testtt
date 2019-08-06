from ..items import BeyondlimitItem

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BeyondLimitSpider(CrawlSpider):
    name = 'beyond_spider'
    start_urls = ['https://www.beyondlimits.com']
    allowed_domain = 'www.beyondlimits.com'

    brand = 'BeyondLimits'
    lang = 'en'
    market = 'UK'

    gender_category_terms = [
        'Men',
        'Women',
    ]

    category_css = '.bb_mega--subitem > .bb_mega--link'
    product_css = '.bb_product--link'
    rules = (
        Rule(LinkExtractor(restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_items')
    )

    def parse_items(self, response):
        garment = BeyondlimitItem()
        garment['retailer_sku'] = response.css('[itemprop=productID]::text').get()
        garment['lang'] = self.lang
        garment['trail'] = self.extract_trail(response)
        garment['gender'] = self.extract_gender(response)
        garment['category'] = self.extract_category(response)
        garment['brand'] = self.brand
        garment['url'] = response.url
        garment['market'] = BeyondLimitSpider.market
        garment['name'] = self.extract_name(response)
        garment['description'] = self.extract_description(response)
        garment['image_urls'] = self.extract_image_urls(response)
        garment['care'] = self.extract_care(response)
        garment['gender'] = self.extract_gender(response)
        garment['category'] = self.extract_category(response)
        garment['skus'] = self.extract_skus(response)

        return garment

    @staticmethod
    def extract_name(response):
        return response.css('[itemprop=name]::text').get()

    @staticmethod
    def extract_image_urls(response):
        return response.css('.bb_pic--navlink::attr(data-bbzoompicurl)').getall()

    @staticmethod
    def extract_care(response):
        return response.css('#description li::text, #description .MsoNormal span::text').getall()

    def extract_trail(self, response):
        category = self.extract_category(response)
        start_trail = " "
        first_trail = f'{self.allowed_domain}/{self.lang}/{category}'
        trail = f'{start_trail}, {first_trail}]'
        return trail

    def extract_gender(self, response):
        raw_genders = response.css('[itemprop=title]::text').getall()
        for gender in self.clean(raw_genders):
            if gender in self.gender_category_terms:
                return gender.lower()

    def extract_category(self, response):
        raw_category = response.css('[itemprop=title]::text').getall()
        for category in self.clean(raw_category):
            if category in self.gender_category_terms:
                return category

    def extract_description(self, response):
        description_css = '#description p::text, #description:not(li)::text'
        raw_description = response.css(description_css).getall()
        description = self.clean(raw_description)
        return description

    @staticmethod
    def extract_skus(response):
        skus = []
        colour = response.css('#description li:nth-child(1)::text').re_first(r'\s\w+')
        for item_size in response.css("select.bb_form--select option[value!=\"\"]::text").getall():
            sku = {
                "sku_id": f"{colour}_{item_size}",
                "colour": colour,
                "price": response.css('[itemprop=price]::text').get(),
                "currency": response.css('[itemprop=priceCurrency]::attr(content)').get(),
                "size": item_size
            }
            skus.append(sku)
        return skus

    @staticmethod
    def clean(uncleaned_data):
        return [item.strip() for item in uncleaned_data if item.strip()]

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
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css='.bb_mega--subitem > .bb_mega--link')),
        Rule(LinkExtractor(restrict_css='.bb_product--link'),follow=True, callback='parse_items')
    )

    def parse_items(self, response):
        item = BeyondlimitItem()
        item['retailer_sku'] = response.css('[itemprop=productID]::text').get()
        item['lang'] = BeyondLimitSpider.lang
        item['trail'] = self.extract_trail(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['brand'] = BeyondLimitSpider.brand
        item['market'] = BeyondLimitSpider.market
        item['url'] = response.url
        item['brand'] = BeyondLimitSpider.brand
        item['name'] = response.css('[itemprop=name]::text').get()
        item['description'] = self.extract_description(response)
        item['image_urls'] = response.css('.bb_pic--navlink::attr(data-bbzoompicurl)').getall()
        item['care'] = response.css('#description li::text, #description .MsoNormal span::text').getall()
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['skus'] = self.extract_skus(response)

        return item

    def extract_trail(self, response):
        category = self.extract_category(response)
        start_trail = " "
        first_trail = f'{self.allowed_domain}/{self.lang}/{category}'
        trail = f'{start_trail}, {first_trail}]'
        return trail

    def extract_gender(self, response):
        raw_genders = response.css('[itemprop=title]::text').getall()
        for gender in self.clean_data(raw_genders):
            if gender in self.gender_category_terms:
                return gender.lower()

    def extract_category(self, response):
        raw_category = response.css('[itemprop=title]::text').getall()
        for category in self.clean_data(raw_category):
            if category in self.gender_category_terms:
                return category

    def extract_description(self, response):
        raw_description = response.css('#description p::text, #description:not(li)::text').getall()
        description = self.clean_data(raw_description)
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
    def clean_data(uncleaned_data):
        return [item.strip() for item in uncleaned_data if item.strip()]

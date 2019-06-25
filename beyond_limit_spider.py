import scrapy
from scrapy.item import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Product(Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()


class BeyondLimitSpider(CrawlSpider):
    name = 'beyond_limit'
    allowed_domains = ['beyondlimits.com']
    start_urls = ['https://www.beyondlimits.com']
    default_brand = 'BeyondLimits'
    default_gender = 'unisex'
    gender_terms = [
        'women',
        'men',
    ]
    care_terms = [
        'Care tips',
        'Material',
    ]
    category_css = '.bb_mega--subitem > .bb_mega--link'
    product_css = '.bb_product--link'
    rules = (
        Rule(LinkExtractor(restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        item = Product()
        item['url'] = response.url
        item['brand'] = self.extract_brand_name(response)
        item['name'] = self.extract_item_name(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['description'] = self.extract_description(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['care'] = self.extract_care(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['skus'] = self.extract_skus(response)

        return item

    def extract_item_name(self, response):
        return response.css('[itemprop=name]::text').get()

    def extract_retailer_sku(self, response):
        return response.css('[itemprop=productID]::text').get()

    def extract_brand_name(self, response):
        return self.default_brand

    def extract_gender(self, response):
        raw_genders = response.css('[itemprop=title]::text').getall()

        for gender in clean(raw_genders):
            if gender.lower() in self.gender_terms:
                return gender

        return self.default_gender

    def extract_category(self, response):
        raw_category = response.css('[itemprop=title]::text').getall()
        return clean(raw_category)

    def extract_care(self, response):
        css = '#description li::text, #description .MsoNormal span::text'
        raw_cares = response.css(css).getall()
        return [care for care in raw_cares if any(care_t in care for care_t in self.care_terms)]

    def extract_image_urls(self, response):
        return response.css('.bb_pic--navlink::attr(data-bbzoompicurl)').getall()

    def extract_description(self, response):
        raw_description = response.css('#description p::text, #description:not(li)::text').getall()
        return [desc for sublist in clean(raw_description) for desc in sublist.split('.') if desc]

    def extract_colour(self, response):
        return response.css('#description li::text, .MsoNormal span::text').re_first(r'\s{1}\w+')

    def extract_currency(self, response):
        return response.css('[itemprop=priceCurrency]::attr(content)').get()

    def extract_current_price(self, response):
        return response.css('[itemprop=price]::text').get()

    def extract_previous_prices(self, response):
        return response.css('.oldPrice del::text').getall()

    def extract_skus(self, response):
        skus = []
        colour = self.extract_colour(response)
        common_sku = {
            'colour': colour,
            'price': self.extract_current_price(response),
            'currency': self.extract_currency(response),
            'previous_prices': self.extract_previous_prices(response)
        }

        for item_size in response.css('.bb_form--select [value!=""]::text').getall():
            sku = common_sku.copy()
            sku['size'] = item_size
            sku['sku_id'] = f'{colour}_{item_size}'
            skus.append(sku)

        return skus


def clean(raw_list):
    return [list_item.strip() for list_item in raw_list if list_item.strip()]

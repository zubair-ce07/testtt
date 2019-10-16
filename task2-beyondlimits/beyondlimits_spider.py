from scrapy.spiders import CrawlSpider

from ..items import BeyondLimitItem


class BeyondLimitsExtractor:
    def parse_details(self, response):
        product_details = BeyondLimitItem()
        product_details['retailer_sku'] = self.extract_retailor_sku(response)
        product_details['url'] = self.extract_url(response)
        product_details['gender'] = self.extract_gender(response)
        product_details['category'] = self.extract_category(response)
        product_details['brand'] = self.extract_brand(response)
        product_details['name'] = self.extract_name(response)
        product_details['description'] = self.extract_description(response)
        product_details['care'] = self.extract_care(response)
        product_details['img_urls'] = self.extract_img_urls(response)
        product_details['skus'] = self.extract_skus(response)
        return product_details

    def extract_retailor_sku(self, response):
        return response.css('[itemprop="productID"]::text').get()

    def extract_url(self, response):
        return response.url

    def extract_gender(self, response):
        return self.clean(response.css('[itemprop=title]::text').getall()[1].strip())

    def extract_category(self, response):
        return response.css('[itemprop=title]::text').getall()[1:]

    def extract_brand(self, response):
        return response.css('[property="og:site_name"]::attr(content)').get()

    def extract_name(self, response):
        return response.css(".bb_art--title::text").get()

    def extract_description(self, response):
        return self.clean(response.css('#description ::text').getall()[:2])

    def extract_care(self, response):
        return response.css('#description li::text')[1].getall()

    def extract_img_urls(self, response):
        return response.css(".bb_pic--nav ::attr(href)").getall()

    def extract_pricing_and_color(self, response):
        price = response.css('[itemprop="price"]::attr(content)').get()
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        previous_price = response.css('.oldPrice del::text').get(default='').split()[:-1]
        color = self.clean(response.css('#description li::text')[0].get().split(':')[1])
        return {'Price': price, 'Previous_Price': previous_price, 'Currency': currency, 'Colour': color}

    def make_sku(self, sku, size):
        final_sku = sku.copy()
        final_sku.update({'size': size, 'sku_id': sku['Colour']+'_'+size})
        return final_sku

    def extract_skus(self, response):
        pricing = self.extract_pricing_and_color(response)
        sizes_sel = response.css('#bb-variants--0 option::text').getall()
        skus = [self.make_sku(pricing, size_sel) for size_sel in sizes_sel]
        if not sizes_sel:
            skus = self.make_sku(pricing, '')
        return skus
    
    def clean(self, list_to_strip):
        if isinstance(list_to_strip, basestring):
            return list_to_strip.strip()
        return [str_to_strip.strip() for str_to_strip in list_to_strip if str_to_strip.strip()]


class BeyondLimitsSpider(CrawlSpider):
    name = "beyondlimits"
    allowed_domains = ['beyondlimits.com']
    start_urls = [
        'https://www.beyondlimits.com/Women/',
        'https://www.beyondlimits.com/Men/',
    ]

    def parse(self, response):
        next_page = response.css('.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        details_extractor = BeyondLimitsExtractor()
        for detail_url in response.css('.bb_product--link.bb_product--imgsizer::attr(href)'):
            yield response.follow(detail_url.get(), callback=details_extractor.parse_details)


class BeyondLimitItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    img_urls = scrapy.Field()
    skus = scrapy.Field()



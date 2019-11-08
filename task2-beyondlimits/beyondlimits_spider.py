from scrapy.spiders import CrawlSpider

from ..items import BeyondLimitItem


class BeyondLimitsParser:
    def parse_details(self, response):
        item = BeyondLimitItem()
        item['retailer_sku'] = self.extract_retailor_sku(response)
        item['url'] = self.extract_url(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['brand'] = self.extract_brand(response)
        item['name'] = self.extract_name(response)
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['img_urls'] = self.extract_img_urls(response)
        item['skus'] = self.extract_skus(response)
        return item

    def extract_retailor_sku(self, response):
        return response.css('[itemprop="productID"]::text').get()

    def extract_url(self, response):
        return response.url

    def extract_gender(self, response):
        return self.clean(response.css('[itemprop=title]::text').getall()[1])

    def extract_category(self, response):
        return response.css('[itemprop=title]::text').getall()[1:]

    def extract_brand(self, response):
        return response.css('[property="og:site_name"]::attr(content)').get()

    def extract_name(self, response):
        return response.css('.bb_art--title::text').get()

    def extract_description(self, response):
        return self.clean(response.css('#description ::text').getall()[:2])

    def extract_care(self, response):
        return response.css('#description li::text')[1].getall()

    def extract_img_urls(self, response):
        return response.css('.bb_pic--nav ::attr(href)').getall()

    def extract_common_sku(self, response):
        price = response.css('[itemprop="price"]::attr(content)').get()
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        previous_price = response.css('.oldPrice del::text').getall()
        color = self.clean(response.css('#description li::text')[0].get().split(':')[1])
        return {'price': price, 'previous_Price': previous_price, 'currency': currency, 'colour': color}

    def extract_skus(self, response):
        common_sku = self.extract_common_sku(response)
        sizes_sel = response.css('#bb-variants--0 option::text').getall()
        skus = []
        for size in sizes_sel:
            sku = common_sku.copy()
            sku['size'] = size
            sku['sku_id'] = f'{common_sku["colour"]}_{size}'
            skus.append(sku)

        return skus if skus else [common_sku.update({'sku_id': common_sku['colour']})]

    def clean(self, list_to_strip):
        if isinstance(list_to_strip, str):
            return list_to_strip.strip()
        return [str_to_strip.strip() for str_to_strip in list_to_strip if str_to_strip.strip()]


class BeyondLimitsSpider(CrawlSpider):
    name = 'beyondlimits'
    allowed_domains = ['beyondlimits.com']
    start_urls = [
        'https://www.beyondlimits.com/Women/',
        'https://www.beyondlimits.com/Men/',
    ]

    def parse(self, response):
        next_page = response.css('.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        details_extractor = BeyondLimitsParser()
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



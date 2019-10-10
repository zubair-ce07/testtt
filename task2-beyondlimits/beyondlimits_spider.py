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
        return response.css('[itemprop=title]::text').getall()[1].strip()

    def extract_category(self, response):
        return response.css('[itemprop=title]::text').getall()[1:]

    def extract_brand(self, response):
        return response.css('[property="og:site_name"]::attr(content)').get()

    def extract_name(self, response):
        return response.css(".bb_art--title::text").get()

    def extract_description(self, response):
        return [desc.strip() for desc in response.css('#description ::text').getall()[:2] if desc.strip()]

    def extract_care(self, response):
        return response.css('#description li::text')[1].getall()

    def extract_img_urls(self, response):
        return response.css(".bb_pic--nav ::attr(href)").getall()

    def extract_skus(self, response):
        color = response.css('#description li::text')[0].get().split(':')[1].strip()
        price = response.css('[itemprop="price"]::attr(content)').get()
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        previous_price = response.css('.oldPrice del::text').get(default='').split()[:-1]
        skus = []

        for size in response.css('#bb-variants--0 option'):
            if size.css("option::attr(value)").get():
                sku = {'colour': color,
                       'price': price,
                       'currency': currency,
                       'previous_prices': previous_price,
                       'size': size.css("option::text").get(),
                       'sku_id': color + "_" + size.css("option::text").get()}
                skus.append(sku)
        return skus


class BeyondLimitsSpider(CrawlSpider):
    name = "beyondlimits"
    allowed_domains = ['beyondlimits.com']
    start_urls = [
        'https://www.beyondlimits.com/',
    ]

    def parse(self, response):
        for category in response.css('.bb_catnav--link'):
            if category.css('::text').get().strip() in ['New In', 'Sale']:
                continue
            yield response.follow(category.attrib['href'], callback=self.parse_category)

    def parse_category(self, response):
        if response.css('.bb_pagination--item.current::text') == 1:
            for page in response.css('bb_pagination--item::attr(href)').getall():
                yield response.follow(page, callback=self.parse_category)
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



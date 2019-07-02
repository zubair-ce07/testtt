import re
import scrapy


class ProductDetails(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    stock = scrapy.Field()
    color = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()


class AsicsSpider(scrapy.Spider):
    name = "asics"
    allowed_domains = ['asics.com']
    start_urls = [
        'https://www.asics.com/us/en-us/',
    ]

    def parse(self, response):
        home_page = self.get_home_page_data(response)

        for major_category in home_page:
            category_url = response.urljoin(major_category)

            yield scrapy.Request(url=category_url, callback=self.extract_products)

    def extract_products(self, response):
        page_products = self.get_page_products(response)

        for product in page_products:
            product_url = response.urljoin(product)
            yield scrapy.Request(url=product_url, callback=self.extract_product_details)
        next_page = self.get_next_page_url(response)
        print(next_page)
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.extract_products)

    def extract_product_details(self, response):

        item = ProductDetails()
        item['retailer_sku'] = self.get_product_sku(response)
        item['name'] = self.get_name(response)
        item['gender'] = self.get_gender(response)
        item['category'] = self.get_category(response)
        item['url'] = self.get_product_url(response)
        item['description'] = self.get_description(response)
        item['image_urls'] = self.get_image_urls(response)
        currency = self.get_currency(response)
        price = self.get_price(response)
        color = self.get_color(response)

        item['care'] = []
        item['brand'] = "ASICS"

        skus = []
        sku_records = self.get_sku_record(response)

        for sku in sku_records:
            single_sku = {
                sku.css('::attr(data-value)').extract_first():
                    {
                        'color': color,
                        'currency': currency,
                        'price': price,
                        'size': self.get_size(sku)

                    }

            }
            skus.append(single_sku)

        item['skus'] = skus
        yield item

    def get_home_page_data(self,response):
        return response.css('div.childlink-wrapper > a ::attr(href)').extract()

    def get_next_page_url(self, response):
        return response.css('div.rightArrow ::attr(href)').extract_first()

    def get_page_products(self,response):
        return response.css('div.gridProduct > div > a ::attr(href)').extract()

    def get_size(self,response):
        return response.css('a.SizeOption::text').extract()

    def get_name(self,response):
        return response.css('title::text').extract_first().split('|')[0].strip()

    def get_gender(self,response):
        return response.css('title::text').extract_first().split('|')[1].strip()

    def get_category(self,response):
        return response.css('div.breadcrumb > a ::text ').extract()

    def get_product_url(self,response):
        return response.url

    def get_description(self,response):
        raw_descriptions = response.css('div.tabInfoChild > div.tabInfoChildContent::text').extract()
        for descption in raw_descriptions:
            if re.sub('\s+', '', descption):
                return re.sub('\s+', '', descption)

    def get_image_urls(self,response):
        return response.css('div.owl-carousel > img::attr(data-big)').extract()

    def get_currency(self,response):
        return response.css('div.clearfix > div.inStock > meta ::attr(content)')[2].extract()

    def get_price(self,response):
        return response.css('div.clearfix > div.inStock > meta ::attr(content)')[3].extract()

    def get_product_sku(self,response):
        print("AHMAD: ",response)
        return response.css('div.clearfix > div.inStock > meta ::attr(content)')[0].extract()

    def get_color(self,response):
        return response.css('title::text').extract_first().split('|')[2]

    def get_sku_record(self,response):
        return response.css('div.size-select-list')[2].css('div.inStock')


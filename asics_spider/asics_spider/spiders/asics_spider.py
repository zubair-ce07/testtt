import scrapy
from scrapy.spiders import CrawlSpider

from asics_spider.items import ProductItem


class AsicsSpider(CrawlSpider):
    name = 'asics_spider'

    def start_requests(self):
        urls = ['https://www.asics.com/us/en-us/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        categories_url = \
            response.xpath('//div[@class="navNodeImageContainer"]/following-sibling::div//a/@href').extract()
        for urls in categories_url:
            url = response.urljoin(urls)
            yield scrapy.Request(url=url, callback=self.parse_products)

    def parse_products(self, response):
        products_url = response.xpath('//a[@class="productMainLink"]/@href').extract()
        for urls in products_url:
            url = response.urljoin(urls)
            yield scrapy.Request(url=url, callback=self.parse_items)

    def parse_items(self, response):
        product_name = self.get_name(response)
        category = self.get_category(response)
        description = self.get_description(response)
        images = self.get_image_url(response)
        previous_price = self.get_previous_price(response)
        current_price = self.get_price(response)
        gender = self.get_gender(response)
        product_id = self.get_product_id(response)

        item = ProductItem()
        item["name"] = product_name
        item["category"] = category
        item["description"] = description
        item["image_urls"] = images
        item["previous_price"] = previous_price
        item["price"] = current_price
        item["gender"] = gender
        item["product_id"] = product_id
        yield item

    def get_name(self, response):
        return response.xpath('//h1[@class="single-prod-title"]/text()').extract_first()

    def get_category(self, response):
        return response.xpath('//div[@id="breadcrumb"]/a/text()').extract_first()

    def get_image_url(self, response):
        return response.xpath('//img[@class="product-img"]/@data-owl-thumb').extract()

    def get_previous_price(self, response):
        return response.xpath('//del/text()').extract_first()

    def get_price(self, response):
        return '$' + response.xpath('//meta[@content="PRICE"]/following-sibling::meta/@content').extract_first()

    def get_description(self, response):
        # This also works
        # return response.xpath('//meta[@name="description"]/@content').extract_first()
        return response.xpath('//h2[contains(text(), "Product Details")]/preceding-sibling::div/parent::div/text()').extract()

    def get_gender(self, response):
        return response.xpath('//div[@id="unisex-tab"]/@class').extract_first()

    def get_product_id(self, response):
        return response.xpath('//span[contains(@itemprop,"model")]//text()').extract_first()

    def skus(self, response):
        pass




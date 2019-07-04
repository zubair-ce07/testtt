import scrapy
from scrapy.spiders import CrawlSpider
from asics_spider.items import ProductItem


class AsicsSpider(CrawlSpider):
    name = 'asics_spider'
    item = ProductItem()

    def start_requests(self):
        self.item["skus"] = dict()
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
        product_sku = self.get_product_skus(response)

        self.item["name"] = product_name
        self.item["category"] = category
        self.item["description"] = description
        self.item["image_urls"] = images
        self.item["previous_price"] = previous_price
        self.item["price"] = current_price
        self.item["gender"] = gender
        self.item["product_id"] = product_id
        self.item["skus"] = product_sku
        yield self.item

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

    def get_product_skus(self, response):
        sku_dict = dict()
        self.item["request"] = list()
        products_urls = response.xpath('//div[@id="variant-choices"]//a/@href').getall()
        for urls in products_urls:
            url = response.urljoin(urls)
            self.item["request"].append(url)
        for url in self.item["request"]:
            scrapy.Request(url=url, callback=self.get_product_skus)
        size_list = self.get_available_sizes(response)
        if not size_list:
            sku_dict.update([(self.get_color(response) + "_" + response.url.split('/')[-1].split('.')[-1], "Not any size available ")])
        for size in size_list:
            sku_data = {
                "Color": self.get_color(response),
                "Price": self.get_price(response)
            }
            sku_dict.update([(self.get_color(response) + "_" + self.extract_size(size), sku_data)])
        return sku_dict

    def get_color(self, response):
        return response.xpath('//div[@id="colour-label"]//span[@class="color-label"]/text()').get()

    def get_available_sizes(self, response):
        form_selector = response.xpath('//form[@class="desktop-style"]')[0]
        return form_selector.css('div.SizeOption.inStock::attr(data-value)').getall()

    def extract_size(self, raw_string):
        token = raw_string.split('.')[3:]
        if len(token) > 1:
            product_size = '.'.join(token)
            return product_size
        elif 'H' in token[0]:
            return token[0].replace('H', '.5')
        return token[0]

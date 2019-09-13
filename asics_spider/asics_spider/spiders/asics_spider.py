import scrapy
from asics_spider.items import ProductItem
from scrapy.spiders import CrawlSpider


class AsicsSpider(scrapy.Spider):
    name = 'asics'
    item = ProductItem()
    allowed_domains = ["asics.com"]

    def start_requests(self):
        urls = ['https://www.asics.com/us/en-us']
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
        next_page = response.xpath('//div[@id="nextPageLink"]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_products)

    def parse_items(self, response):
        self.item["name"] = self.product_name(response)
        self.item["category"] = self.category(response)
        self.item["description"] = self.description(response)
        self.item["image_urls"] = self.image_url(response)
        self.item["previous_price"] = self.previous_price(response)
        self.item["price"] = self.price(response)
        self.item["gender"] = self.gender(response)
        self.item["product_id"] = self.product_id(response)
        self.item["request"] = self.requests(response)
        self.item["skus"] = self.product_skus(response)
        return self.parse_result(self.item)

    def product_name(self, response):
        return response.xpath('//h1[@class="single-prod-title"]/text()').extract_first()

    def category(self, response):
            return response.xpath('//div[@id="breadcrumb"]/a/text()').extract_first()

    def image_url(self, response):
        return response.xpath('//img[@class="product-img"]/@data-owl-thumb').extract()

    def previous_price(self, response):
        return response.xpath('//del/text()').extract_first()

    def price(self, response):
        return '$' + response.xpath('//meta[@content="PRICE"]/following-sibling::meta/@content').extract_first()

    def description(self, response):
        # This also works
        # return response.xpath('//meta[@name="description"]/@content').extract_first()
        return ' '.join(response.xpath(
            '//h2[contains(text(), "Product Details")]/preceding-sibling::div/parent::div/text()').extract()).strip()

    def gender(self, response):
        return response.xpath('//div[@id="unisex-tab"]/@class').extract_first()

    def product_id(self, response):
        return response.xpath('//span[contains(@itemprop,"model")]//text()').extract_first()

    def requests(self, response):
        products_urls = response.xpath(
            '//div[@id="variant-choices"]/div[not(contains(@class,"active"))]/a/@href').extract()
        return [response.follow(url=url, callback=self.update_skus) for url in products_urls]

    def update_skus(self, response):
        self.item['skus'].append(self.product_skus(response))
        return self.parse_result(self.item)

    def parse_result(self, item):
        if item['request']:
            return item['request'].pop()

        return item

    def product_skus(self, response):
        skus = []
        size_list = self.available_sizes(response)
        for size in size_list:
            color = self.color(response)
            size = self.size(size)
            sku = {
                f'{color}_{size}': {
                    'Color': color,
                    'Size': size,
                    'Price': self.price(response),
                    'Previous_prices': self. previous_price(response)
                }
            }
            skus.append(sku)
        return skus

    def color(self, response):
        return response.xpath('//div[@id="colour-label"]//span[@class="color-label"]/text()').extract_first()

    def available_sizes(self, response):
        form_selector = response.xpath('//form[@class="desktop-style"]')[0]
        return form_selector.css('div.SizeOption.inStock::attr(data-value)').extract()

    def size(self, raw_string):
        token = raw_string.split('.')[3:]
        if len(token) > 1:
            product_size = '.'.join(token)
            return product_size
        elif 'H' in token[0]:
            return token[0].replace('H', '.5')
        return token[0]

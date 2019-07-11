from brothers_spider.items import ProductItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BrothersSpider(CrawlSpider):
    name = 'brothers_spider'
    item = ProductItem()
    allowed_domains = ["brothers.se"]
    start_urls = ['https://www.brothers.se']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ol[@class="nav-primary"]')),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="next"]')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="product-image"]'),
             callback="parse_items", follow=True)
    )

    def parse_items(self, response):
        self.item["name"] = self.extract_name(response)
        self.item["category"] = self.extract_category(response)
        self.item["description"] = self.extract_description(response)
        self.item["image_urls"] = self.extract_image_url(response)
        self.item["previous_price"] = self.extract_previous_price(response)
        self.item["price"] = self.extract_price(response)
        self.item["gender"] = "Male"
        self.item["product_id"] = self.extract_product_id(response)
        self.item["request"] = self.extract_requests(response)
        self.item["skus"] = self.extract_product_skus(response)
        return self.parse_result(self.item)

    def extract_name(self, response):
        return response.xpath('//span[@class="name"]/text()').extract_first()

    def extract_category(self, response):
        return response.xpath('//span[@class="category"]//text()').extract_first()

    def extract_image_url(self, response):
        return response.xpath('//div[@class="more-views"]//img/@src').extract()

    def extract_previous_price(self, response):
        price = response.xpath('//p[@class="old-price"]/span[@class="price"]/text()').extract_first()
        if price:
            return price.strip().replace('\xa0', '')
        return None

    def extract_price(self, response):
        return response.xpath('//span[@class="price"]//text()').extract_first() + "Kr"

    def extract_description(self, response):
        return ' '.join(response.xpath('//div[@class="description"]//text()').extract()).strip()

    def extract_product_id(self, response):
        return response.xpath('//span[@class="product_id"]/text()').extract_first()

    def extract_requests(self, response):
        products_urls = response.xpath('//div[@class="other-products"]//a/@href').extract()
        return [response.follow(url=url, callback=self.update_skus, dont_filter=True) for url in products_urls]

    def extract_product_skus(self, response):
        skus = []
        sku = dict()
        size_list = self.extract_available_sizes(response)
        sku['price'] = self.extract_price(response),
        sku['previous_prices'] = self.extract_previous_price(response)
        sku['Available size'] = [self.extract_size(size) for size in size_list]
        sku['Color'] = self.extract_name(response).split(' ')[-1]
        skus.append(sku)

        return skus

    def update_skus(self, response):
        self.item['skus'].append(self.extract_product_skus(response))
        return self.parse_result(self.item)

    def parse_result(self, item):
        if item['request']:
            return item['request'].pop()
        return item

    def extract_available_sizes(self, response):
        return response.xpath('//div[@id="qty_table"]//p[not(text()="0")]/@class').extract()

    def extract_size(self, raw_size):
        return raw_size.split('_')[-1]

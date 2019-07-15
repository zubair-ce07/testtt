from brothers_spider.items import ProductItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ParseProducts:
    item = ProductItem()

    def parse_items(self, response):
        self.item["name"] = self.product_name(response)
        self.item["category"] = self.category(response)
        self.item["description"] = self.description(response)
        self.item["image_urls"] = self.image_url(response)
        self.item["previous_price"] = self.previous_price(response)
        self.item["price"] = self.price(response)
        self.item["gender"] = "Male"
        self.item["product_id"] = self.product_id(response)
        self.item["requests"] = self.requests(response)
        self.item["skus"] = self.product_skus(response)
        return self.parse_result(self.item)

    def product_name(self, response):
        return response.xpath('//span[@class="name"]/text()').extract_first()

    def category(self, response):
        return response.xpath('//span[@class="category"]//text()').extract_first()

    def image_url(self, response):
        return response.xpath('//div[@class="more-views"]//img/@src').extract()

    def previous_price(self, response):
        return ' '.join(response.xpath('//p[@class="old-price"]/span[@class="price"]//text()')
                        .extract()).strip().replace('\xa0', '')

    def price(self, response):
        return response.css(
            '.price-info p.special-price .price::text, .price-info span.regular-price .price::text').extract_first().strip().replace(
            '\xa0', '')

    def description(self, response):
        return ' '.join(response.xpath('//div[@class="description"]//text()').extract()).strip()

    def product_id(self, response):
        return response.xpath('//span[@class="product_id"]/text()').extract_first()

    def requests(self, response):
        sku_urls = response.xpath('//div[@class="other-products"]//a/@href').extract()
        return [response.follow(url=url, callback=self.update_skus, dont_filter=True) for url in sku_urls]

    def product_skus(self, response):
        skus = []
        size_list = self.available_sizes(response)
        for size in size_list:
            color = self.product_name(response).split()[-1]
            size = self.size(size)
            sku = {
                f'{color}_{size}': {
                    'Color': color,
                    'Size': size,
                    'Price': self.price(response),
                    'Previous_prices': self.previous_price(response) if self.previous_price(response) else None
                }
            }
            skus.append(sku)

        return skus

    def update_skus(self, response):
        self.item['skus'].append(self.product_skus(response))
        return self.parse_result(self.item)

    def parse_result(self, item):
        if item['requests']:
            return item['requests'].pop()
        return item

    def available_sizes(self, response):
        return response.xpath('//div[@id="qty_table"]//p[not(text()="0")]/@class').extract()

    def size(self, raw_size):
        return raw_size.split('_')[-1]


class BrothersSpider(CrawlSpider, ParseProducts):  # crawl
    name = 'brothers_spider'

    allowed_domains = ["brothers.se"]
    start_urls = ['https://www.brothers.se']
    listings_x = [
        '//ol[@class="nav-primary"]',
        '//a[@class="next"]',
    ]
    products_x = [
        '//div[@class="product-image"]',
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_x)),  # callback parse
        Rule(LinkExtractor(restrict_xpaths=products_x),
             callback='parse_items', follow=True)
    )

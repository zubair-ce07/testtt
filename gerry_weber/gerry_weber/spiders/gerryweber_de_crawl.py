from gerry_weber.items import GerryweberItem
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class GerryweberDeCrawlSpider(CrawlSpider):
    name = "gerryweber-de-crawl"
    allowed_domains = ["house-of-gerryweber.de"]
    start_urls = [
        'http://www.house-of-gerryweber.de/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="nav_bg_head_tab"]',
                                            '//ul[@id="nav_catmenu"]//li',
                                            '//a[@class="scrollforward"]'])),
        Rule(LinkExtractor(restrict_xpaths=['//ul[@class="cat_products"]/li']),
             callback='parse_product_contents'),
    )

    def parse_product_contents(self, response):
        item = GerryweberItem()
        item['spider_name'] = self.name
        item['retailer'] = 'gerryweber-de'
        item['currency'] = self.product_currency(response)
        item['market'] = 'DE'
        item['category'] = self.product_category(response)
        item['retailer_sku'] = self.product_retailer_sku(response)
        item['price'] = self.product_price(response)
        item['description'] = self.product_description(response)
        item['url_original'] = response.url
        item['brand'] = self.product_brand(response)
        item['image_urls'] = self.product_image_urls(response)
        item['crawl_id'] = None
        item['date'] = None
        item['skus'] = self.product_sku(response)
        item['care'] = []
        item['lang'] = 'de'
        item['name'] = self.product_name(response)
        item['url'] = response.url
        item['gender'] = 'women'
        item['industry'] = None
        yield item

    def product_category(self, response):
        return response.xpath('//li[contains(@class,"active")]/a//text()').extract()

    def product_retailer_sku(self, response):
        retailer_sku = response.xpath('//div[contains(@class, "itemNo")]//text()').extract()
        return retailer_sku[0].split(' ', 1)[-1]

    def product_price(self, response):
        return response.xpath('//div[contains(@class,"salesprice")]/span/text()').extract()[0]

    def product_description(self, response):
        return response.xpath('//span[@itemprop="description"]/text()').extract()

    def product_brand(self, response):
        return response.xpath('//span[@itemprop="brand"]/text()').extract()[0]

    def product_image_urls(self, response):
        return response.xpath('//div[@id="wrap"]//a/@href | //div[@id="wrap"]/img/@src').extract()

    def product_name(self, response):
        return response.xpath('//h1[@class="productname"]//text()').extract()[0]

    def product_currency(self, response):
        return 'EUR'

    def product_sku(self, response):
        skus = {}
        sku_common = {}
        colours = response.xpath('//div[contains(@class,"color")]/ul/li/div/a/@title').extract()
        sizes = response.xpath('//div[contains(@class,"swatches size")]/ul/li/div/a/@data-value').extract()
        sku_common['currency'] = self.product_currency(response)
        sku_common['price'] = self.product_price(response)
        index = 0

        for color in colours:
            if sizes:
                for size in sizes:
                    sku = {'size': size, 'colour': color}
                    sku.update(sku_common)
                    skus[index] = sku
                    index += 1
            else:
                sku = {'size': 'One Size', 'colour': color}
                sku.update(sku_common)
                key = self.product_retailer_sku(response)
                skus[key] = sku
        return skus

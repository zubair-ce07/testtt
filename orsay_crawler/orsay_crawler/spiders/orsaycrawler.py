import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from orsay_crawler.items import OrsayCrawlerItem

import json


class OrsaySpider(CrawlSpider):
    name = 'orsaycrawler'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']

    rules = (Rule(LinkExtractor(allow=r'^http://www.orsay.com/de-de/produkte/$'), callback='parse_products'),
             Rule(LinkExtractor(allow=r'^http://www.orsay.com/de-de/.*\.html$'), callback='parse_product_detail'))

    def parse_products(self, response):
        products = response.css(".js-product-grid-portion li")
        for product in products:
            url = product.css(".product-image a::attr(href)").extract_first()
            if url:
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse_product_detail)

    def parse_product_detail(self, response):
        item = OrsayCrawlerItem()
        json_data = self.get_json(response)

        item["brand"] = json_data["brand"]
        item["care"] = self.get_care(response)
        item["category"] = json_data["categoryName"]
        item["description"] = self.get_description(response)
        item["gender"] = 'women'
        item["image_urls"] = self.get_images_url(response)
        item["lang"] = 'de'
        item["market"] = 'DE'
        item["name"] = json_data["name"]
        item["retailer_sku"] = json_data["idListRef6"]
        item["url"] = response.url
        item["skus"] = {}
        item["req_list"] = self.get_colours_requests(response, item)
        return self.generate_request(item)

    def parse_skus(self, response):
        item = response.meta['item']
        item["skus"].update(self.skus(response))
        return self.generate_request(item)

    def skus(self, response):
        sku = {}
        json_data = self.get_json(response)
        sizes = self.get_sizes(response)
        for size in sizes:
            sku.update({
                f"{json_data['productId']}_{size}": {
                    "color": json_data['color'],
                    "currency": json_data['currency_code'],
                    "out_of_stock": 'False' if json_data['quantity'] else 'True',
                    "price": json_data['grossPrice'],
                    "size": json_data['size']}
            })
        return sku

    @staticmethod
    def get_images_url(response):
        return response.css(".thumb.js-thumb img::attr(src)").extract()

    @staticmethod
    def get_care(response):
        return response.css(".product-material.product-info-block.js-material-container p::text").extract()

    @staticmethod
    def get_description(response):
        return response.css(".product-info-block.product-details div.with-gutter::text").extract()

    @staticmethod
    def get_json(response):
        return json.loads(response.css(".js-product-content-gtm::attr(data-product-details)").extract_first())

    @staticmethod
    def get_sizes(response):
        sizes = response.css("ul.swatches.size li.selectable a::text").extract()
        return [size.strip('\n') for size in sizes if size != '']

    @staticmethod
    def generate_request(item):
        if item['req_list']:
            return item['req_list'].pop(0)
        else:
            return item

    def get_colours_requests(self, response, item):
        all_requests = []
        colours = response.css("ul.swatches.color li a::attr(href)").extract()
        for color in colours:
            all_requests.append(
                scrapy.Request(url=response.urljoin(color), callback=self.parse_skus,
                               meta={"item": item}, dont_filter=True))
        return all_requests

import scrapy
import json
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from orsay_crawler.items import OrsayCrawlerItem


class OrsaySpider(CrawlSpider):
    name = 'orsaycrawler'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']

    rules = (Rule(LinkExtractor(allow=r'^http://www.orsay.com/de-de/produkte/$'), callback='fetch_products'),
             Rule(LinkExtractor(allow=r'^http://www.orsay.com/de-de/.*\.html$'), callback='fetch_product_details'))

    def fetch_products(self, response):
        products = response.css("div.js-product-grid-portion li")
        for product in products:
            url = product.css("div.product-image a::attr(href)").extract_first()
            if url:
                yield scrapy.Request(url=response.urljoin(url), callback=self.fetch_product_detail)

    def fetch_product_detail(self, response):
        item = OrsayCrawlerItem()
        json_data = json.loads(response.css("div.js-product-content-gtm::attr(data-product-details)").extract_first())

        item["brand"] = json_data["brand"]
        item["care"] = response.css("div.product-material.product-info-block.js-material-container p::text").extract()
        item["category"] = json_data["categoryName"]
        item["description"] = response.css("div.product-info-block.product-details div.with-gutter::text").extract()
        item["gender"] = 'women'
        item["lang"] = 'de'
        item["market"] = 'DE'
        item["name"] = json_data["name"]
        item["image_urls"] = self.fetch_images_links(response)
        item["retailer_sku"] = json_data["idListRef6"]
        item["skus"] = []
        item["url"] = []

        colors = response.css("ul.swatches.color li a::attr(href)").extract()
        if colors:
            yield scrapy.Request(
                url=colors[0],
                callback=self.fetch_product_skus,
                meta={"colors": colors, "item": item},
                dont_filter=True)
        else:
            yield item

    def fetch_product_skus(self, response):
        skus_data = []
        item = response.meta['item']
        colors = response.meta['colors']
        sizes = self.fetch_sizes(response)
        json_data = json.loads(response.css("div.js-product-content-gtm::attr(data-product-details)").extract_first())

        for size in sizes:
            skus_data.append(
                {f"{json_data['idListRef6']}_{size}":
                    {"color": json_data['color'],
                     "currency": json_data['currency_code'],
                     "out_of_stock": 'False' if json_data['quantity'] else 'True',
                     "price": json_data['grossPrice'],
                     "size": size}})

        item['skus'] = skus_data
        item["url"].append(response.url)
        colors.remove(response.url)

        if colors:
            yield scrapy.Request(
                url=colors[0],
                callback=self.fetch_product_skus,
                meta={"colors": colors, "item": item},
                dont_filter=True)
        else:
            yield item

    @staticmethod
    def fetch_images_links(response):
        return response.css("div.thumb.js-thumb img::attr(src)")

    @staticmethod
    def fetch_sizes(response):
        sizes = response.css("div.value ul.swatches.size li.selectable a::text").extract()
        return [size.strip('\n') for size in sizes if size != '']

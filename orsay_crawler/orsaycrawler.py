import json

from scrapy.spiders import Rule, CrawlSpider, Request
from scrapy.linkextractors import LinkExtractor
from orsay_crawler.items import OrsayCrawlerItem
MAX_PRODUCT_DISPLAY = 72


class OrsaySpider(CrawlSpider):
    name = "orsaycrawler"
    allowed_domains = ["orsay.com"]
    start_urls = ["http://www.orsay.com/de-de/"]

    listing_css = [".navigation .level-1"]
    product_css = [".js-product-grid-portion"]
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback="parse_pagination"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_product_detail")
    )

    def parse_pagination(self, response):
        total_products = self.parse_products_count(response)

        for items_count in range(0, total_products+1, MAX_PRODUCT_DISPLAY):
            next_url = response.url + "?sz=" + str(items_count)
            yield Request(url=next_url, callback=self.parse)

    def parse_products_count(self, response):
        total_product_css = ".load-more-progress::attr(data-max)"
        pages = response.css(total_product_css).extract_first()
        return int(pages) if pages else 0

    def parse_product_detail(self, response):
        item = OrsayCrawlerItem()
        json_data = self.raw_data(response)
        item["brand"] = json_data["brand"]
        item["care"] = self.parse_care(response)
        item["category"] = json_data["categoryName"]
        item["description"] = self.pasre_description(response)
        item["gender"] = "women"
        item["image_urls"] = self.parse_images_urls(response)
        item["lang"] = "de"
        item["market"] = "DE"
        item["name"] = json_data["name"]
        item["retailer_sku"] = json_data["idListRef6"]
        item["url"] = response.url
        item["skus"] = {}

        requests = self.parse_colours_requests(response)
        return self.next_request(requests, item)

    def parse_colours(self, response):
        item = response.meta["item"]
        requests = response.meta["requests"]
        item["skus"].update(self.skus(response))
        return self.next_request(requests, item)

    def skus(self, response):
        json_data = self.raw_data(response)
        sizes_css = "ul.swatches.size li.selectable a::text"
        sizes = response.css(sizes_css).extract()
        sizes = [size.strip("\n") for size in sizes if size]

        skus = {}
        for size in sizes:
            sku = {"colour": json_data["color"]}
            sku["currency"] = json_data["currency_code"]
            sku["currency"] = json_data["currency_code"]
            sku["out_of_stock"] = "False" if json_data["quantity"] else "True"
            sku["price"] = json_data["grossPrice"]
            sku["size"] = json_data["size"]
            skus[f"{json_data['productId']}_{size}"] = sku
        return skus

    def parse_images_urls(self, response):
        return response.css(".thumb.js-thumb img::attr(src)").extract()

    def parse_care(self, response):
        care_css = ".product-material.product-info-block.js-material-container p::text"
        return response.css(care_css).extract()

    def pasre_description(self, response):
        desc_css = ".product-info-block.product-details div.with-gutter::text"
        return response.css(desc_css).extract()

    def raw_data(self, response):
        raw_css = ".js-product-content-gtm::attr(data-product-details)"
        return json.loads(response.css(raw_css).extract_first())

    def next_request(self, requests, item):
        if requests:
            request = requests.pop()
            request.meta["item"] = item
            request.meta["requests"] = requests
            return request
        else:
            return item

    def parse_colours_requests(self, response):
        colour_requests = []
        colours_css = "ul.swatches.color li a::attr(href)"
        colours = response.css(colours_css).extract()
        for colour in colours:
            colour_requests.append(Request(
                url=response.urljoin(colour),
                callback=self.parse_colours,
                dont_filter=True))
        return colour_requests

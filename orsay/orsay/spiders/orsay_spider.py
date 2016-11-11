import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from orsay.items import OrsayItem


class OrsaySpider(CrawlSpider):
    name = "orsay"
    allowed_domains = ["orsay.com"]
    start_urls = [
        "http://www.orsay.com/de-de/"
    ]

    rules = (
        Rule(LinkExtractor(restrict_css="#nav")),
        Rule(LinkExtractor(restrict_css=".product-image"), callback="parse_item")
    )

    def parse(self, response):
        item = OrsayItem()

        care = response.css(".product-care img::attr(src)").extract()
        care.append(response.css(".material::text").extract_first())

        currency = "EUR"
        price = response.css(".price::text").extract_first().split()[0]
        color = response.css(".product-colors li.active a img::attr(title)").extract_first()

        item["spider_name"] = "orsay-de-crawl"
        item["url"] = response.url
        item["retailer"] = "orsay-de"
        item["brand"] = "Orsay"
        item["currency"] = currency
        item["market"] = "DE"
        item["lang"] = "de"
        item["category"] = response.css("#nav span::text").extract()
        item["name"] = response.css("h1.product-name::text").extract_first()
        item["description"] = response.css(".description::text").extract()
        item["product_hash"] = response.css(".sku::text").extract_first().split(":")[1].strip()
        item["price"] = price
        item["color"] = color
        item["image_urls"] = response.css(".product-image-gallery-thumbs img::attr(src)").extract()
        item["care"] = care
        item["skus"] = self.get_skus(response, currency, price, color)

        colors_urls = response.css(".product-colors li:not(.active) a::attr(href)").extract()

        return self.request_colors(item, colors_urls)

    def request_colors(self, item, colors_urls):
        if colors_urls:
            single_url = colors_urls.pop()
            request = scrapy.Request(single_url, callback=self.parse_colors,
                                     meta={"item": item, "colors_urls": colors_urls})
            return request
        return item

    def parse_colors(self, response):
        item = response.meta["item"]
        colors_urls = response.meta["colors_urls"]

        item["skus"].update(
            self.get_skus(response, item._values["currency"], item._values["price"], item._values["color"]))

        return self.request_colors(item, colors_urls)

    @staticmethod
    def get_skus(response, currency, price, color):
        skus = {}

        for size in response.css(".sizebox-wrapper ul li"):
            item_size = size.css("::text").extract_first().strip()
            skus[response.css("input#sku::attr(value)").extract_first() + "_" + item_size] = {
                "currency": currency,
                "price": price,
                "size": item_size,
                "out_of_stock": True if size.css(".mz-tooltip::text").extract_first() == "nicht verfügbar" else False,
                "color": color
            }
        return skus

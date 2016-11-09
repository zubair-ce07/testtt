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

    def parse_item(self, response):
        item = OrsayItem()

        care = response.css(".product-care img::attr(src)").extract()
        care.append(response.css(".material::text").extract_first())

        currency = "EUR"
        price = response.css(".price::text").extract_first().split()[0]
        color = response.css(".product-colors li.active a img::attr(title)").extract_first()

        skus = {}
        for size in response.css(".sizebox-wrapper ul li"):
            skus[size.css("::attr(data-optionid)").extract_first()] = {
                "currency": currency,
                "price": price,
                "size": size.css("::text").extract_first().strip(),
                "out_of_stock": True if size.css(".mz-tooltip::text").extract_first() == "nicht verfügbar" else False,
                "color": color
            }

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
        item["skus"] = skus

        request =

        yield item

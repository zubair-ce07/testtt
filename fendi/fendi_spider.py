from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from fendi.items import FendiItem


class FendiSpider(CrawlSpider):
    name = "fendi"
    allowed_domains = ["fendi.com"]
    start_urls = [
        "http://www.fendi.com/gb/"
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=[".first-level-container ul li", ".showRelatedMenu ul li"])),
        Rule(LinkExtractor(restrict_css=".goToProduct"), callback="parse_item")
    )

    def parse_item(self, response):
        item = FendiItem()

        sks = {}
        for o in response.css("#js_prod_size option.soldout"):
            sks[o.css("::attr(value)").extract_first()] = {
                "currency": "GBP",
                "price": response.css(".fd-pp-info-wrp .upgradable::text").extract_first()[1:],
                "color": "Black",
                "size": o.css("::text").extract_first()
            }

        item["original_url"] = response.url,
        item["spider_name"] = "fendi-k-crawl",
        item["retailer"] = "fendi-k",
        item["category"] = response.css(".first-level-container ul li a::text").extract(),
        item["product_hash"] = \
            response.css(".fd-pp-info-wrp .js_slidingInfo-right li p::text").extract_first().split(":")[1].strip(),
        item["brand"] = "Fendi",
        item["name"] = response.css(".fd-pp-info-wrp h1::text").extract_first(),
        item["description"] = response.css(".fd-pp-info-wrp p.fd-pp-intro::text").extract_first(),
        item["price"] = response.css(".fd-pp-info-wrp .upgradable::text").extract_first()[1:],
        item["image_urls"] = response.css(".fd-pp-thumbnails ul li a::attr(href)").extract(),
        item["currency"] = "GBP",
        item["market"] = "K",
        item["sks"] = sks

        yield item

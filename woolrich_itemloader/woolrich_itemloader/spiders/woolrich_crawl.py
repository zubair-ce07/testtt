from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from woolrich_itemloader.spiders.woolrich_itemloader_parser import WoolrichItemloaderParserSpider


class WoolrichCrawlSpider(CrawlSpider):
    name = "woolrich-crawl"
    allowed_domains = ["www.woolrich.com"]
    start_urls = ["http://www.woolrich.com/"]
    listing_css = ["#primary ul:not([class])", ".pagination-item--next"]
    product_css = ".card-title"
    product_parser = WoolrichItemloaderParserSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback=product_parser.parse)
    )

    def parse(self, response):
        requests = super().parse(response)
        trail = response.meta.get("trail", [])
        trail.append(response.url)

        for request in requests:
            request.meta["trail"] = trail.copy()
            yield request

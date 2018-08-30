from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner

from forevernew_xpath.spiders.product_parser import ProductParser


class ForeverNewAuCrawlSpider(CrawlSpider):
    name = "forever-new-au-crawl"
    allowed_domains = ["forevernew.com.au"]
    start_urls = ["https://www.forevernew.com.au/"]
    product_parser = ProductParser()
    listing_xpath = ["//*[@id='menu']", "//*[@class='next']"]
    product_xpath = "//*[@class='product-name']"

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listing_xpath), callback="parse"),
        Rule(LinkExtractor(restrict_xpaths=product_xpath,
                           process_value=url_query_cleaner), callback=product_parser.parse)
    )

    def parse(self, response):
        requests = super().parse(response)
        trail = response.meta.get("trail", [])
        trail.append(response.url)

        for request in requests:
            request.meta["trail"] = trail.copy()
            yield request

from forever_new.spiders.product_parser import ProductParser
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner


class ForeverNewAuCrawlSpider(CrawlSpider):
    name = "forever-new-au-crawl"
    allowed_domains = ["forevernew.com.au"]
    start_urls = ["https://www.forevernew.com.au/"]
    product_parser = ProductParser()
    category_css = "#menu, .next"
    product_css = ".product-name"

    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css, process_value="process_link"), callback=product_parser.parse)
    )

    def parse(self, response):
        requests = super().parse(response)
        trail = response.meta.get("trail", [])
        trail.append(response.url)

        for request in requests:
            request.meta["trail"] = trail.copy()
            yield request

    def process_link(self, value):
        return url_query_cleaner(value, [])

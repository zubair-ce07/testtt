from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner

from forevernew_itemloader.spiders.forever_new_itemloader_parse import ForeverNewItemloaderParseSpider


class ForeverNewAuCrawlSpider(CrawlSpider):
    name = "forever-new-au-crawl"
    allowed_domains = ["forevernew.com.au"]
    start_urls = ["https://www.forevernew.com.au/"]
    product_parser = ForeverNewItemloaderParseSpider()
    listing_css = ["#menu", ".next"]
    product_css = ".product-name"

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css, process_value=url_query_cleaner), callback=product_parser.parse)
    )

    def parse(self, response):
        requests = super().parse(response)
        trail = response.meta.get("trail", [])
        trail.append(response.url)

        for request in requests:
            request.meta["trail"] = trail.copy()
            yield request

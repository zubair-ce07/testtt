from forever_new.spiders.product_parser import ProductParser
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner


class ForeverNewAuCrawlSpider(CrawlSpider):
    name = "forever-new-au-crawl"
    allowed_domains = ["forevernew.com.au"]
    start_urls = ["https://www.forevernew.com.au/"]
    product_parser = ProductParser()

    rules = (
        Rule(LinkExtractor(restrict_css="#menu, .next"), callback="parse"),
        Rule(LinkExtractor(restrict_css=".product-name"), callback=product_parser.parse
             , process_links="clean_links")
    )

    def parse(self, response):
        requests = super().parse(response)
        trail = response.meta.get("trail", [])
        trail.append(response.url)

        for request in requests:
            request.meta["trail"] = trail.copy()
            yield request

    def clean_links(self, links):
        for link in links:
            link.url = url_query_cleaner(link.url, [])

        return links

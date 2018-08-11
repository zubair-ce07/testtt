from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import add_or_replace_parameter

from levis.spiders.product_parser import ProductParser


class LevisBrCrawlSpider(CrawlSpider):
    name = "levis-br-crawl"
    allowed_domains = ["www.levi.com.br"]
    start_urls = ["https://www.levi.com.br/"]

    product_parser = ProductParser()

    rules = (Rule(LinkExtractor(restrict_css=".menu-departamento"), callback="parse_category"),
             Rule(LinkExtractor(restrict_css=".product-name a"), callback=product_parser.parse))

    def parse(self, response):
        requests = super().parse(response)
        trail = response.meta.get("trail", [])
        trail.append(response.url)

        for request in requests:
            request.meta["trail"] = trail.copy()
            yield request

    def parse_category(self, response):
        total_pages = response.css(".main script").re_first(".*pagecount_.*=\s(\d+)")

        if not total_pages:
            return

        total_pages = int(total_pages)
        request_url = response.css(".main script").re_first(".*(/buscapagina?.*=)'")
        trail = response.meta["trail"]
        trail.append(response.url)

        for page_no in range(1, total_pages + 1):
            request_url = add_or_replace_parameter(request_url, "PageNumber", page_no)
            request = Request(response.urljoin(request_url), callback=self.parse)
            request.meta["trail"] = trail.copy()
            yield request

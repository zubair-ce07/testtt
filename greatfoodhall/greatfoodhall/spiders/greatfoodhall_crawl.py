from scrapy import Spider, Request
from w3lib.url import add_or_replace_parameter
from scrapy.linkextractors import LinkExtractor

from greatfoodhall.spiders.greatfoodhall_product_parser import GreatfoodhallProductParserSpider


class GreatfoodhallCrawlSpider(Spider):

    name = 'greatfoodhall-crawl'
    allowed_domains = ['www.greatfoodhall.com']
    start_urls = ['http://www.greatfoodhall.com/']
    pagination_base_url = "http://www.greatfoodhall.com/eshop/ShowProductPage.do"

    lisiting_le = LinkExtractor(restrict_css=".mainNav")
    product_le = LinkExtractor(restrict_css=".productTmb")

    product_parser = GreatfoodhallProductParserSpider()

    def parse(self, response):
        listing_urls = self.lisiting_le.extract_links(response)

        for cookie_id, listing_url in enumerate(listing_urls):
            yield response.follow(url=listing_url.url, callback=self.parse_sessions, meta={"cookiejar": cookie_id})

    def parse_sessions(self, response):
        yield Request(url=response.url, callback=self.parse_listing_pages,
                      meta={"cookiejar": response.meta["cookiejar"]}, dont_filter=True)

    def parse_listing_pages(self, response):
        total_pages = response.xpath("//script[contains(text(), 'totalpage')]").re_first("totalpage = (\d+)")
        if not total_pages:
            return
        total_pages = int(total_pages)
        for page_no in range(1, total_pages+1):
            url = add_or_replace_parameter(self.pagination_base_url, "curPage_1", page_no)
            yield Request(url=url, meta={"cookiejar": response.meta["cookiejar"]},
                          dont_filter=True, callback=self.parse_listing)

    def parse_listing(self, response):
        product_urls = self.product_le.extract_links(response)

        for product_url in product_urls:
            yield Request(url=product_url.url, callback=self.product_parser.parse,
                          meta={"cookiejar": response.meta["cookiejar"]})

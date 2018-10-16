import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from isetan.items import IsetanItem, IsetanItemLoader


class IsetanSpider(CrawlSpider):
    name = "isetan"
    allowed_domains = ["isetan.com.sg"]
    start_urls = ["http://isetan.com.sg/"]
    listings_css = [
        ".navPages-list .navPages-item",
        ".pagination-item--next"
        ]
    products_css = [".custm-tags"]
    deny_re = ["/workshops/"]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re),
            callback="parse"),
        Rule(LinkExtractor(restrict_css=products_css),
            callback="parse_product")
    )

    def parse_product(self, response):
        loader = IsetanItemLoader(item=IsetanItem(), response=response)
        loader.add_css("name", ".productView-title::text")
        loader.add_css("brand", ".product-brand::text")
        loader.add_css("price", ".productView-price .price::text")
        loader.add_css("quantity", ".productView-info-value::text")
        loader.add_css("categories", ".breadcrumb-label::text")
        loader.add_css("description", "#tab-description p::text")
        loader.add_css("image_urls", ".productView-thumbnail a::attr(href)")
        loader.add_css("currency", "meta[property='product:price:currency']::attr(content)")
        loader.add_css("product_type", ".breadcrumb:nth-child(2) a::text")
        loader.add_value("url", response.url)
        loader.add_value("website", self.start_urls[0])
        return loader.load_item()

import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from isetan.items import IsetanItem, IsetanItemLoader


class IsetanSpider(CrawlSpider):
    name = 'isetan'
    allowed_domains = ['isetan.com.sg']
    start_urls = ['http://isetan.com.sg/']
    urls_css = [
        ".navPages-list .navPages-item",
        ".pagination-item--next"]

    rules = (
        Rule(LinkExtractor(
            restrict_css=url_css,
            deny=("/workshops/")), callback="parse"),
        Rule(LinkExtractor(restrict_css=(".custm-tags")),
            callback="parse_product")
    )

    def parse_product(self, response):
        loader = IsetanItemLoader(item=IsetanItem(), response=response)
        loader.add_css("name", ".productView-title::text")
        loader.add_css("brand", ".product-brand::text")
        loader.add_css("price", ".productView-price div .price::text")
        loader.add_css("quantity", ".productView-info-value::text")
        loader.add_css("categories", ".breadcrumb-label::text")
        loader.add_css("description", "#tab-description p::text")
        loader.add_css("image_urls", ".productView-thumbnail a::attr(href)")
        loader.add_css("currency", "meta[property='product:price:currency']::attr(content)")
        loader.add_css("product_type", "ul.breadcrumbs > li:nth-child(2) a::text")
        loader.add_value("url", response.url)
        loader.add_value("website", "https://www.isetan.com.sg/")
        return loader.load_item()

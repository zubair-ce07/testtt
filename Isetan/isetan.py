import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from isetan.items import IsetanItem, IsetanItemLoader


class IsetanSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['isetan.com.sg']
    start_urls = ['http://isetan.com.sg/']

    rules = (
        Rule(LinkExtractor(restrict_css=(".navPages-list > .navPages-item > a"),
                deny=("/workshops/")), callback="parse_product_list", follow=True),
        Rule(LinkExtractor(
            restrict_css=(".pagination-item--next > a"), allow=("page=")),
            callback="parse_product_list", follow=True),
    )

    def parse_product_urls(self, response):
        return response.css(".custm-tags a::attr(href)").extract()

    def parse_product_list(self, response):
        product_urls = self.parse_product_urls(response)

        for url in product_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_product
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
        loader.add_css("currency", ".productView-price div .price::text")
        loader.add_css("product_type", "ul.breadcrumbs > li:nth-child(2) a::text")
        loader.add_value("url", response.url)
        loader.add_value("website", "https://www.isetan.com.sg/")
        return loader.load_item()

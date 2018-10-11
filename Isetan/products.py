import scrapy
from isetan.items import IsetanItem, IsetanItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ProductsSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['isetan.com.sg']
    start_urls = ['http://isetan.com.sg//']

    rules = (Rule(LinkExtractor(
            deny=('/workshops/'),
            restrict_css=(".navPages-list > .navPages-item > a")),
            callback='parse_product_list'),
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
        l = IsetanItemLoader(item=IsetanItem(), response=response)
        l.add_css("name", ".productView-title::text")
        l.add_css("brand", ".product-brand::text")
        l.add_css("price", ".productView-price div .price::text")
        l.add_css("quantity", ".productView-info-value::text")
        l.add_css("categories", ".breadcrumb-label::text")
        l.add_css("description", "#tab-description p span::text")
        l.add_css("image_urls", ".productView-thumbnail a::attr(href)")
        l.add_value("currency", "SGD")
        l.add_css("product_type", "ul.breadcrumbs > li:nth-child(2) a::text")
        l.add_value("url", response.url)
        l.add_value("website", "https://www.isetan.com.sg/")
        return l.load_item()

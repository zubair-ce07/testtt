from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Task3.items import ProductItem


class ColcciProductDetails(CrawlSpider):
    name = "Colcci"
    start_urls = ['https://www.colcci.com.br/']

    allowed_links = ('masculino-novo1', 'feminino-novo1', 'fitness', 'acessorios')
    rules = (Rule(LinkExtractor(allow=allowed_links, restrict_css="div#main-menu ul#menus")),
             Rule(LinkExtractor(restrict_css="div.products-list"), callback='parse_page'),)

    def parse_page(self, response):
        product_css_selector = response.css("div.descriptioncolContent")
        product_loader = ItemLoader(item=ProductItem(), selector=product_css_selector)

        product_loader.default_output_processor = TakeFirst()

        product_loader.add_css('retailer_sku', 'form input::attr(value)')
        product_loader.add_css('name', " div.title h1::text")
        product_loader.add_css('category', " div.title h1::text")
        product_loader.add_css('price', "div.price-holder span.price::text")
        product_loader.add_css('description', self.get_product_description_selector(response))
        product_loader.add_value('brand', 'Colcci')
        product_loader.add_value('url', response.url)
        product_loader.add_value('gender', response.url
                                 + response.css(" div.title h1::text").extract_first())
        product_loader.add_value('image_urls',
                                 response.css("div.jTscroller a::attr(href)").extract())

        raw_skus = response.css("head script::text").re_first(r'.+LS.variants = \[(.+)\];')
        product_loader.add_value('skus', self.format_rawskus_to_jsonstrings(raw_skus))

        yield product_loader.load_item()

    def format_rawskus_to_jsonstrings(self, raw_skus):
        if raw_skus:
            raw_skus = raw_skus.split("}}}\"},")
            total_skus = len(raw_skus)
            skus_in_json_format = []
            for sku in raw_skus[:total_skus - 1]:
                skus_in_json_format.append(sku + "}}}\"}")

            skus_in_json_format.append(raw_skus[total_skus - 1])

            return skus_in_json_format

    def get_product_description_selector(self, response):
        if response.css("div#whatItIs p::text").extract():
            description_selector = "div#whatItIs p::text"
        elif response.css("div#whatItIs p + div::text").extract():
            description_selector = "div#whatItIs p + div::text"
        else:
            description_selector = "div#whatItIs p + div div::text"

        return description_selector

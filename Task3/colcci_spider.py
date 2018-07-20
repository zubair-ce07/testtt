import json

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
             Rule(LinkExtractor(deny='page', restrict_css="div.products-list"), callback='parse_page'),)

    def parse_page(self, response):
        product_css_selector = response.css("div.descriptioncolContent")
        product_loader = ItemLoader(item=ProductItem(), selector=product_css_selector)
        product_loader.default_output_processor = TakeFirst()

        product_loader.add_css('retailer_sku', 'form input::attr(value)')
        product_loader.add_css('name', " div.title h1::text")
        product_loader.add_css('category', " div.title h1::text")
        product_loader.add_css('price', "div.price-holder span.price::text")
        product_loader.add_css('description', ColcciProductDetails.get_product_description_css(response))
        product_loader.add_value('brand', 'Colcci')
        product_loader.add_value('url', response.url)
        product_loader.add_value('gender', response.url+response.css(" div.title h1::text").extract_first())
        product_loader.add_value('image_urls', response.css("div.jTscroller a::attr(href)").extract())
        product_loader.add_value('skus', json.loads(
            response.css("head script::text").re_first(r'.+LS.variants = (.+);')))

        yield product_loader.load_item()

    @staticmethod
    def get_product_description_css(response):
        if response.css("div#whatItIs p::text").extract():
            description_css = "div#whatItIs p::text"
        elif response.css("div#whatItIs p + div::text").extract():
            description_css = "div#whatItIs p + div::text"
        else:
            description_css = "div#whatItIs p + div div::text"

        return description_css

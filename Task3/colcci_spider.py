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
    rules = (Rule(LinkExtractor(allow=allowed_links, restrict_css=".with-subitems")),
             Rule(LinkExtractor(deny='page', restrict_css=".products-list"), callback='parse_page'),)

    def parse_page(self, response):
        product_css_selector = response.css(".descriptioncolContent")
        product_loader = ItemLoader(item=ProductItem(), selector=product_css_selector)
        product_loader.default_output_processor = TakeFirst()

        product_loader.add_css('retailer_sku', '[name="add_to_cart"]::attr(value)')
        product_loader.add_css('name', '[itemprop="name"]::text')
        product_loader.add_css('category', '[itemprop="name"]::text')
        product_loader.add_css('price', '[itemprop="price"]::text')
        product_loader.add_xpath('description', '//*[@id="whatItIs"]//text()')
        product_loader.add_value('brand', 'Colcci')
        product_loader.add_value('url', response.url)
        product_loader.add_value('gender', response.url+response.css('[itemprop="name"]::text').extract_first())
        product_loader.add_value('image_urls', response.css(".cloud-zoom-gallery::attr(href)").extract())

        sku_jsondata = json.loads(response.css("head script::text").re_first(r'.+LS.variants = (.+);'))
        product_loader.add_value('skus', sku_jsondata)

        yield product_loader.load_item()

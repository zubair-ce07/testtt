from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import StartItem


class LemkusSpider(CrawlSpider):

    name = "Lemkus"
    start_urls = ['https://www.jacklemkus.com/']
    rules = (
        Rule(LinkExtractor(restrict_css= ".clearfix.menu-simple-dropdown.menu-columns")),
        Rule(LinkExtractor(restrict_css= [".row.products-grid",".next.i-next"]),callback= 'product_items'),
    )

    def product_items(self, response):

        items = StartItem()

        items['retailer_sku'] = self.extract_retailer_sku(response)
        items['gender'] = self.extract_gender(response)
        items['brand'] = self.extract_brand(response)
        items['url'] = self.extract_url(response)
        items['name'] = self.extract_name(response)
        items['description'] = self.extract_description(response)
        items['image_urls'] = self.extract_image_url(response)
        items['skus'] = self.extract_skus(response)

        yield items

    def extract_retailer_sku(self,response):        
        return response.css(".sku::text").extract_first()
        
    def extract_gender(self,response):
        return response.xpath('//th[contains(text(),"Gender")]/following-sibling::td/text()').extract_first()

    def extract_brand(self,response):
        return response.xpath('//th[contains(text(),"Item Brand")]/following-sibling::td/text()').extract_first()

    def extract_url(self, response):
        return response.url

    def extract_name(self, response):
        return response.css(".product-name h1::text").extract_first()

    def extract_description(self, response):
        return response.css(".std::text").extract_first("").strip()

    def extract_image_url(self, response):
        return  response.css(".hidden-xs img::attr(src)").extract()

    def extract_skus(self, response):

        price = response.css(".price::text").extract_first()
        currency = 'R'
        size_label =  response.xpath('//th[contains(text(),"Whats My Size (ALL UK)")]/following-sibling::td/text()').extract_first()
        product_id = response.css(".product-data-mine::attr(data-confproductid)").extract()

        sku = {
            "price": price,
            "currency": currency,
            "size": size_label,
            "sku-id": product_id
        }

        return sku



import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import StartItem


class QuotesSpider(CrawlSpider):

    name = "Lemkus"
    start_urls = [ 'https://www.jacklemkus.com/']
    rules = (
        Rule(LinkExtractor(restrict_css= ".menu-link")),
        Rule(LinkExtractor(restrict_css=(".products-grid")),callback='product'),
        Rule(LinkExtractor(restrict_css=(".next.i-next")),callback='product'),
   )

    def product(self, response):

        items = StartItem()

        items['retailer_sku'] = self.get_retailer_sku(response)
        items['gender'] = self.extract_gender(response)
        items['brand'] = self.get_brand(response)
        items['url'] = self.get_url(response)
        items['name'] = self.get_name(response)
        items['description'] = self.get_description(response)
        items['image_urls'] = self.get_image_url(response)
        items['skus'] = self.get_skus(response)

        yield items

    def get_retailer_sku(self,response):
    
        return response.css(".sku::text").extract_first()
        
    def extract_gender(self,response):

        return response.xpath('//th[contains(text(),"Gender")]/following-sibling::td/text()').extract_first()

    def get_brand(self,response):

        return response.xpath('//th[contains(text(),"Item Brand")]/following-sibling::td/text()').extract_first()

    def get_url(self, response):

        return response.url

    def get_name(self, response):

        return response.css(".product-name h1::text").extract_first()

    def get_description(self, response):

        return response.css(".std::text").extract_first("").strip()

    def get_image_url(self, response):

        return  response.css(".hidden-xs img::attr(src)").extract()

    def get_skus(self, response):

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

        
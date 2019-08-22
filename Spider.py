from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import StartItem

class LemkusSpider(CrawlSpider):

    name = "Lemkus"
    currency = 'R'
    start_urls = ['https://www.jacklemkus.com/']
    listings_css = [".clearfix.menu-simple-dropdown.menu-columns", ".next.i-next"]
    products_css = [".row.products-grid"]
    
    rules = (
        Rule(LinkExtractor(restrict_css = listings_css)),
        Rule(LinkExtractor(restrict_css = products_css), callback = 'product_items'),
    )

    def product_items(self, response):

        product = StartItem()

        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['gender'] = self.extract_gender(response)
        product['brand'] = self.extract_brand(response)
        product['url'] = response.url
        product['name'] = self.extract_name(response)
        product['description'] = self.extract_description(response)
        product['image_urls'] = self.extract_image_url(response)
        product['skus'] = self.extract_skus(response)

        yield product

    def extract_retailer_sku(self,response):        
        return response.css(".sku::text").extract_first()
        
    def extract_gender(self,response):
        return response.xpath('//th[contains(text(),"Gender")]/following-sibling::td/text()').extract_first()

    def extract_brand(self,response):
        return response.xpath('//th[contains(text(),"Item Brand")]/following-sibling::td/text()').extract_first()

    def extract_name(self, response):
        return response.css(".product-name h1::text").extract_first()

    def extract_description(self, response):
        return response.css(".std::text").extract_first("").strip()

    def extract_image_url(self, response):
        return  response.css(".hidden-xs img::attr(src)").extract()

    def extract_skus(self, response):

        skus = []

        price = response.css(".price::text").extract_first()
        currency = self.currency
        size_label = response.css(".product-data-mine::attr(data-lookup)").extract()

        common_sku = {
            "price": price,
            "currency": currency,
            "sku_id": "onesize"
        }
    
        if size_label is None:
            return common_sku

        size_label =  eval(size_label[0])

        for _, raw_sku in size_label.items():

            if raw_sku["stock_status"]:

                if raw_sku["id"] is not None:
                    common_sku["sku_id"] = raw_sku["id"]

                sku = {
                    "size": raw_sku["size"],
                    "quantity": raw_sku["qty"],
                }      
                sku.update(common_sku)              
                skus.append(sku)

        if skus is not None:
            return skus
        else:
            return common_sku


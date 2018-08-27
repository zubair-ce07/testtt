import json

from scrapy import Spider, Request

from lanebryant.item import LanebryantItem

retailer_sku = Field()
trail = Field()
gender = Field()
category = Field()
brand = Field()
url = Field()
name = Field()
description = Field()
care = Field()
image_urls = Field()
skus = Field()
price = Field()
currency = Field()


# 'https://www.lanebryant.com/lanebryant/baseAjaxServlet?pageId=UserState&Action=Header.userState&userState_id=pId%3D351394&fetchFavorites=true&_=1534750185924'

class ProductParser(Spider):
    name = 'lanebryant-parser'
    brand = 'LB'
    gender = 'female'

    def extract_retailer_sku(self, response):
        return response.css('::attr(data-bv-product-id)').extract_first()

    def extract_product_name(self, response):
        return response.css('mar-product-title::text').extract_first()

    def extract_product_description(self, response):
        description = response.css('div#tab1 p::text').extract()
        description += response.css('div#tab1 ul:nth-child(2) ::text').extract()
        return description

    def extract_product_care(self, response):
        return response.css('div#tab1 ul:nth-child(3) ::text').extract()

    def extract_raw_product(self, response):
        return json.loads(response.css('#pdpInitialData::text').extract_first())

    def extract_price_specification(self, response):
        price_spec_css = "[type='application/ld+json']::text"
        return json.loads(response.css(price_spec_css).extract_first())

    def extract_price(self, response):
        raw_speci = self.extract_price_specification(response)
        return raw_price['offers']['priceSpecification']['price']

        # raw_product = self.extract_raw_product(response)['pdpDetail']['product'][0]
        # return raw_product['price_range']['list_price']

    # '//lanebryant.scene7.com/is/image/lanebryantProdATG/351368_0000008003_swatch?$swatch$'

    def extract_currency(self, response):
        raw_currency = self.extract_price_specification(response)
        return raw_currency['offers']['priceSpecification']['priceCurrency']

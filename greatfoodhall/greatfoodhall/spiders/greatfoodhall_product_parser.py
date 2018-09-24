from scrapy import Spider

from ..items import GreatfoodhallItemLoader


class GreatfoodhallProductParserSpider(Spider):
    name = 'greatfoodhall-product-parser'
    allowed_domains = ['www.greatfoodhall.com']

    product_xpaths_map = {
        "brand": "//*[@class='pL6']/text()",
        "name": "//*[contains(@class, 'description')]/text()",
        "price": "//*[@class='itemOrgPrice2']/text() | //*[contains(@class, 'newPrice')]/text()",
        "previous_price":  "//*[contains(@class, 'oldPrice')]/text()",
        "categories": "//*[contains(@class, 'breadCrumbArea')]/ul/text()",
        "packaging": "//*[contains(@class, 'ml')]/text() |"
                     " //*[contains(@class, 'priceBox')]//*[contains(@class, 'pB5')]/text()",
        "image_urls": "//*[@class='productPhoto']/img/@src",
        "availability": "//*[contains(@class, 'btnAddToCart')]/img"
    }

    def parse(self, response):
        product_loader = GreatfoodhallItemLoader(response=response)

        for field, field_xpath in self.product_xpaths_map.items():
            product_loader.add_xpath(field, field_xpath)

        product_loader.add_value("url", response.url)
        product_loader.add_value("currency", "HKD")
        product_loader.add_value("website_name", "Greatfoodhall")

        yield product_loader.load_item()

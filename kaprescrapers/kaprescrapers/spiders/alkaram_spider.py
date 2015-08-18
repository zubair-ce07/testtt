__author__ = 'mateenahmeed'
from scrapy.spiders import Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from kaprescrapers.items import Garment
from kaprescrapers.spiders.KapreBaseSpider import KapreBaseSpider
import re


class AlkaramSpider(KapreBaseSpider):
    name = "alkaram"
    allowed_domains = ["alkaramstudio.com"]
    start_urls = ['http://www.alkaramstudio.com/']
    brand_id = 12

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=("//a[contains(., 'View All')]",
                                                "//a[@title='Next']"
                                                ))),
        Rule(SgmlLinkExtractor(restrict_xpaths=("//*[@class='product-name']",
                                                )),
             callback="parse_product")
    )

    # for each product
    def parse_product(self, response):
        sel = response.xpath("//*[@class='product-essential']")

        item = Garment()
        item['item_is_available'] = True
        item['source_url'] = response.url
        item['item_category_name'] = self.get_category(sel)
        item['item_brand_id'] = self.brand_id
        item['item_code'] = self.get_item_code(sel)
        item['item_image_url'] = self.get_image_url(response)
        item['item_description'] = self.get_description(sel)
        item['item_price'] = self.get_price(sel)
        item['item_is_on_sale'] = self.is_on_sale(sel)
        yield item

    # for item code
    def get_item_code(self, sel):
        return sel.xpath(".//*[@class='product-name']/h1/text()").extract()[0].strip()

    # for product description
    def get_description(self, sel):
        des = sel.xpath(".//tbody/tr[contains(.,'Description')]//td//text()").extract()
        return " ".join(des)

    # category
    def get_category(self, sel):
        category = sel.xpath(".//tr[contains(.,'Category')]//td/text()").extract()
        return category[0].strip() if category else "uncategorized"

    # image url
    def get_image_url(self, response):
        src = response.xpath(".//*[@id='image-zoom']/@href")
        return response.urljoin(src[0].extract())

    # price for product
    def get_price(self, sel):
        price = sel.xpath(".//*[@class='regular-price' or @class='special-price']"
                          "//*[@class='price']/text()").extract()[0].strip()
        return re.sub("PKR ", '', price)

    def is_on_sale(self, sel):
        on_sale = sel.xpath(".//*[@class='special-price']//*[@class='price']/text()").extract()
        return True if on_sale else False

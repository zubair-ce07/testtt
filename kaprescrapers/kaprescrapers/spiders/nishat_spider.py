__author__ = 'mateenahmeed'
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from kaprescrapers.items import KaprePkItem
import re


class NishatSpider(CrawlSpider):
    name = "nishat"
    allowed_domains = ["nishatlinen.com"]
    start_urls = ['http://nishatlinen.com/']
    brand_id = 2

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=("//*[@id='header']//ul[contains(@class,'nav')]/li[position()<5]",
                                                "//div[@class= 'links']//a"
                                                ))),
        Rule(SgmlLinkExtractor(restrict_xpaths=("//div[@class='product']//a",
                                                )),
             callback="parse_product")
    )

    # for each product
    def parse_product(self, response):
        sel = response.xpath("/html")

        item = KaprePkItem()
        item['source_url'] = response.url
        item['item_category_name'] = self.get_category(sel)
        item['item_brand_id'] = self.brand_id
        item['item_code'] = self.get_item_code(sel)
        item['item_image_url'] = self.get_image_url(response)
        item['item_description'] = self.get_description(sel)
        item['item_price'] = self.get_price(sel)
        item['item_is_available'] = self.is_available(sel)
        item['item_is_on_sale'] = self.is_on_sale(sel)
        yield item

    # for item code
    def get_item_code(self, sel):
        return sel.xpath(".//*[@id='product']/h1/text()").extract()[0].strip()

    # for product description
    def get_description(self, sel):
        des = sel.xpath(".//*[@id='tab-description']//p/text()").extract()
        if not des:
            des = sel.xpath(".//*[@id='tab-description']//tr/*/text()").extract()
        return " ".join(des)

    # category
    def get_category(self, sel):
        category = sel.xpath(".//*[@id='product']/ul/li/text()").extract()
        if category:
            return re.sub("Product Code: ", '', category[0].strip())
        return "uncategorized"

    # image url
    def get_image_url(self, response):
        src = response.xpath(".//*[@id='zoom1']/@href")
        return response.urljoin(src[0].extract())

    # price for product
    def get_price(self, sel):
        price = sel.xpath("//*[@id='product']//div[@class= 'price']//p/text() |"
                          "//*[@id='product']//*[@class= 'special_price']/text()").extract()
        if price:
            return (price[0].strip()).split(" ")[-1]
        return "TBA"

    def is_on_sale(self, sel):
        on_sale = sel.xpath("//*[@id='product']//*[@class= 'special_price']/text()").extract()
        return True if on_sale else False

    def is_available(self, sel):
        # if comming soon
        tba_check = self.get_price(sel)
        if "TBA" in tba_check:
            return False
        sold = sel.xpath("//*[@id='product']//span[contains(.,'sold')]/text()").extract()
        return False if sold else True

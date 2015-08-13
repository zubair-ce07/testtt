__author__ = 'mateenahmeed'
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from kaprescrapers.items import KaprePkItem


class SafinazSpider(CrawlSpider):
    name = "safinaz"
    allowed_domains = ["sanasafinaz.com"]
    start_urls = ['http://www.sanasafinaz.com/']
    brand_id = 8

    rules = (
        Rule(SgmlLinkExtractor(deny=("accessories", "Acoustics"),
                               restrict_xpaths=("//*[@class= 'top-menu']/li/a",
                                                )),
             callback="parse_items"),
    )

    # this will parse all the products on current page
    def parse_items(self, response):
        product_links = response.xpath("//*[@class= 'product-item']")
        for href in product_links:
            plink = href.xpath(".//*[@class='product-title']/a/@href").extract()
            full_url = response.urljoin(plink[0])
            on_sale = self.is_on_sale(href)
            # manual requests were made because on_sale is not mentioned on item page
            yield scrapy.Request(full_url, callback=self.parse_product, meta={'on_sale': on_sale})

    # for each product
    def parse_product(self, response):
        sel = response.xpath("//*[@class='detail-box']")

        item = KaprePkItem()
        item['item_is_on_sale'] = response.meta["on_sale"]
        item['source_url'] = response.url
        item['item_category_name'] = self.get_category(sel)
        item['item_brand_id'] = self.brand_id
        item['item_code'] = self.get_item_code(sel)
        item['item_image_url'] = self.get_image_url(response)
        item['item_description'] = self.get_description(sel)
        item['item_is_available'] = True
        item['item_price'] = self.get_price(sel)
        yield item

    # for item code
    def get_item_code(self, sel):
        return sel.xpath(".//*[@itemprop='name']/text()").extract()[0].strip()

    # for product description
    def get_description(self, sel):
        des = sel.xpath(".//*[@class='short-description']/text()").extract()
        return des[0].strip() if des else ""

    # category
    def get_category(self, sel):
        return sel.xpath(".//*[@class='cat-neme']/text()").extract()[0].strip()

    # image url
    def get_image_url(self, response):
        src = response.xpath("//*[@id='zoom1']/@href")
        return response.urljoin(src[0].extract())

    # price for product
    def get_price(self, sel):
        price = sel.xpath(".//*[@class='product-price']/span/text()").extract()[0].strip()
        return price.split(" ")[-1]

    def is_on_sale(self, sel):
        on_sale = sel.xpath(".//*[@class='price old-price']").extract()
        return True if on_sale else False

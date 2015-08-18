__author__ = 'mateenahmeed'
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from kaprescrapers.items import Garment
from kaprescrapers.spiders.KapreBaseSpider import KapreBaseSpider
import re
from urlparse import urlparse


class BareezeSpider(KapreBaseSpider):
    name = "bareeze"
    allowed_domains = ["www.bareeze.com"]
    start_urls = ['http://www.bareeze.com/pk/shop/']
    brand_id = 6

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=("//*[@id='nav']//li/ul",
                                                "//a[@title='Next']"
                                                )),
             follow=True,
             callback="parse_items"),
    )

    # this will parse all the products on current page
    def parse_items(self, response):
        product_links = response.xpath("//*[@class='product_detail']")
        for href in product_links:
            plink = href.xpath(".//*[@class='product-name']//a/@href").extract()
            full_url = response.urljoin(plink[0])
            price = self.get_price(href)
            # price demanded is on products pages so we are taking price from here
            # its not in Rules as price on item page is calculated from JS for multiple skus with multiple option
            # that will be performance overhead to extract and calculate prices from JS using regex
            yield scrapy.Request(full_url, callback=self.parse_product, meta={'price': price})

    # for each product
    def parse_product(self, response):
        sel = response.xpath("/html")

        item = Garment()
        item['item_price'] = response.meta["price"]
        item['source_url'] = response.url
        item['item_category_name'] = self.get_category(response.url)
        item['item_brand_id'] = self.brand_id
        item['item_code'] = self.get_item_code(sel)
        item['item_image_url'] = self.get_image_url(response)
        item['item_description'] = self.get_description(sel)
        item['item_is_available'] = True
        item['item_is_on_sale'] = self.is_on_sale(sel)
        yield item

    # for item code
    def get_item_code(self, sel):
        code = sel.xpath("//div[@class='sku']/text()").extract()[0].strip()
        return re.sub("SKU: ", '', code)

    # for product description
    def get_description(self, sel):
        des = sel.xpath("//div[@class='std']/text()").extract()
        return des[0] if des else ""

    # category
    def get_category(self, url):
        path = urlparse(url).path
        return path.split("/")[2]

    # image url
    def get_image_url(self, response):
        src = response.xpath("//*[@id='cloudZoom']/@href")
        return response.urljoin(src[0].extract())

    # price for product
    def get_price(self, sel):
        price = sel.xpath(".//*[@class='price']/text()").extract()[-1].strip()
        return re.sub("PKR ", '', price)

    def is_on_sale(self, sel):
        on_sale = sel.xpath("//*[@class='full-product-price']//*[@class='old-price']/text()").extract()
        return True if on_sale else False

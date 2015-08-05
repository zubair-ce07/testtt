__author__ = 'mateenahmeed'
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from gulahmed.items import gulItem


class MySpider(CrawlSpider):
    name = "gulahmed"
    allowed_domains = ["gulahmedshop.com"]
    start_urls = ['http://www.gulahmedshop.com/']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=("//*[@id='site-menu']/ul/li//li",
                                                ))),
        Rule(SgmlLinkExtractor(restrict_xpaths=("//*[@id='main-content']//section/section[1]//*[@id='brands-list']",
                                               )),
            callback="parse_items")
    )

    # this will parse all the products on current page
    def parse_items(self, response):

        sel = response.xpath("/html")
        nextpage = sel.xpath("//*[@id='frm']//a[@data-title='Next Page']/@href")
        if nextpage:
            next_page_url = response.urljoin(nextpage[0].extract())
            yield scrapy.Request(next_page_url, callback=self.parse_items)

        # getting all products on current page
        product_links = response.xpath("//*[@id='main-content']//div[@class ='product']")
        for href in product_links:
            plink = href.xpath(".//div[@class='entry-media']/a/@href").extract()
            full_url = response.urljoin(plink[0])
            #availability of item
            availabity = self.get_availability(href)
            yield scrapy.Request(full_url, callback=self.parse_product, meta={'availabilty': availabity})

     # for each product
    def parse_product(self, response):
        sel = response.xpath("/html")
        # item = response.meta["item"]
        item = gulItem()
        item['item_is_avaiable'] = response.meta["availabilty"]

        item['item_url'] = response.url
        item['item_category_name'] = self.get_category(sel)
        item['item_brand_id'] = self.get_brand_id(sel)
        item['item_code'] = self.get_item_code(sel)
        item['item_image_url'] = self.get_image_url(response)
        item['item_description'] = self.get_description(sel)
        item['item_price'] = self.get_price(sel)
        yield item

    # for brand id
    def get_brand_id(self, sel):
        # demanded as int  '3'
        return 3

    # for item code
    def get_item_code(self, sel):
        return sel.xpath("//*[@id='main-content']//header//h3/text()").extract()[0].strip()

    # for product description
    def get_description(self, sel):
        des = sel.xpath("//*[@id='product-description']/p[2]/text()").extract()
        if des:
            return des[0]
        return ""

    # category
    def get_category(self, sel):
        return sel.xpath("//*[@id='main-content']//header//h2/text()").extract()[0].strip()

    # image url
    def get_image_url(self, response):
        src = response.xpath("//img[@id='zoom1']/@src")
        return response.urljoin(src[0].extract())

    # price for product
    def get_price(self, sel):
        price = sel.xpath("//article [@class='entry-content']//li[3]/span[@class= 'value']/text()").extract()[0].strip()
        return price.split(" ")[-1]

    def get_availability(self, sel):
        availblilty = sel.xpath(".//div[@class='entry-main']/div/a/span/text()").extract()[0]
        if "Not" in availblilty:
            return False
        return True


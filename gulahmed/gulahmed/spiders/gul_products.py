__author__ = 'mateenahmeed'
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from gulahmed.items import gulItem


class GulahmedSpider(CrawlSpider):
    name = "gulahmed"
    allowed_domains = ["gulahmedshop.com"]
    start_urls = ['http://www.gulahmedshop.com/']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=("//*[@id='site-menu']//ul[contains(@class,'mega-sub')]",))),
        Rule(SgmlLinkExtractor(deny=("PriceCondition",), restrict_xpaths=("//*[@id='brands-list']",)),
             callback="parse_items")
    )

    # this will parse all the products on current page
    def parse_items(self, response):

        sel = response.xpath("/html")
        nextpage = sel.xpath("//a[@data-title='Next Page']/@href")
        if nextpage:
            next_page_url = response.urljoin(nextpage[0].extract())
            yield scrapy.Request(next_page_url, callback=self.parse_items)

        # getting all products on current page
        product_links = response.xpath("//*[@id='main-content']//div[@class ='product']")
        for href in product_links:
            plink = href.xpath(".//div[@class='entry-media']/a/@href").extract()
            full_url = response.urljoin(plink[0])
            # availability of item
            availability = self.get_availability(href)
            yield scrapy.Request(full_url, callback=self.parse_product, meta={'availability': availability})

    # for each product
    def parse_product(self, response):
        sel = response.xpath("/html")

        item = gulItem()
        item['item_is_avaiable'] = response.meta["availability"]
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
        des = sel.xpath("//*[@id='product-description']//p//text()").extract()
        return des[0] if des else ""

    # category
    def get_category(self, sel):
        return sel.xpath("//*[@id='main-content']//header//h2/text()").extract()[0].strip()

    # image url
    def get_image_url(self, response):
        src = response.xpath("//img[@id='zoom1']/@src")
        return response.urljoin(src[0].extract())

    # price for product
    def get_price(self, sel):
        price = sel.xpath("//article[@class='entry-content']"
                          "//span[contains(., 'Price')]/following::span[1]//text()").extract()[0].strip()
        return price.split(" ")[-1]

    def get_availability(self, sel):
        availblilty = sel.xpath(".//div[@class='entry-main']//span/text()").extract()[0]
        if "Not" in availblilty:
            return False
        return True

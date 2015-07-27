__author__ = 'mateenahmeed'
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from orsayspider.items import orsayItem
from orsayspider.items import skuItem


class OrsaySpider(CrawlSpider):
    name = 'orsay_spider'
    allowed_domains = ["orsay.com"]
    start_urls = ['http://www.orsay.com/']

    # this will extract all the links of the main categories in website
    rules = (Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=("//ul[@id='nav']/li/ul/li/a")),
                  callback="parse_links"),
             )

    # it extracts all the product links present in each category
    def parse_links(self, response):

        # checking fort pagination
        nextpage = response.xpath("//div[@class='pages']/ul[@class='pagination']"
                                  "/li/a[@title='Weiter']/@href")
        if len(nextpage):
            next_page_url = response.urljoin(nextpage[0].extract())
            yield scrapy.Request(next_page_url, callback=self.parse)

        # getting all products on current page
        product_links = response.xpath("//ul[@id='products-list']/li/article/div/a/@href")
        for href in product_links:
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_product)

    # it parses all the details of one particular product
    def parse_product(self, response):

        sel = response.xpath("/html")

        # just to make things little simpler
        # sel1 is used when we are getting more specific information related to product main
        sel1 = response.xpath("//div[@id='product_main']")

        # Making an object of our class present in items.py
        item = orsayItem()

        self.get_retailer_sku(sel1, item)
        self.get_description(sel, item)
        self.get_category(response.url, item)
        self.get_image_urls(sel, item)
        self.get_care(sel, item)
        self.get_lang(sel, item)
        self.get_name(sel1, item)
        self.get_currency(sel1, item)
        self.get_skus(sel, item)
        item['url_orignal'] = response.url

        yield item

    # for sku retailer id
    def get_retailer_sku(self, sel1, item):
        sku = sel1.xpath("//p[@class='sku']/text()").extract()
        print ("sku ", sku)
        if len(sku):
            sku1 = sku[0].strip()
            item['retailer_sku'] = re.findall('\d+', sku1)[0]

    # for product description
    def get_description(self, sel, item):
        item['description'] = [i.strip() for i in
                               sel.xpath("//div[@class='product-info six columns']"
                                         "/p/text()").extract()]

    # extracting the category from url
    def get_category(self, url, item):
        url_link = url.split("/")
        if (len(url_link) > 5):
            item['category'] = url_link[4:-1]
        else:
            item['category'] = []

    # image urls
    def get_image_urls(self, sel, item):
        item['image_urls'] = sel.xpath("//div[@id='product_media']/div/img/@src").extract()

    # care for product
    def get_care(self, sel, item):
        item['care'] = [i.strip() for i in
                        sel.xpath("//p[@class='material']/text() |"
                                  " //ul[@class='caresymbols']/li/img/@src").extract()]

    # for language
    def get_lang(self, sel, item):
        item['lang'] = sel.xpath("/html/@lang").extract()[0]

    # for product name
    def get_name(self, sel1, item):
        item['name'] = sel1.xpath("//h2[@class='product-name']/text()").extract()[0].strip()

    # for getting currency
    def get_currency(self, sel1, item):
        # price for currency
        price = sel1.xpath("//div[@class='product-main-info']"
                           "/div/span/span[@class='price']/text()").extract()
        if not len(price):
            price = sel1.xpath("//p[@class='special-price']"
                               "/span[@class='price']/text()").extract()
        item['currency'] = price[0].strip()[-3:]

    # for skus
    def get_skus(self, sel1, item):
        # sku as dictionary
        item['skus'] = {}

        colors = sel1.xpath("//ul[@class='product-colors']/li/a/@href").extract()
        length = len(colors)

        if length:

            in_item = skuItem()

            self.get_sku_price(sel1, in_item)
            self.get_sku_color(sel1, in_item)
            self.get_sku_previous_price(sel1, in_item)
            # extracting price from currency
            in_item['currency'] = item['currency']
            # size available
            size_list = self.get_sku_size_list(sel1)

            # adding sku with color+size key in skus dictionary
            for sz in size_list:
                in_item_t = skuItem(in_item)
                in_item_t['size'] = sz
                color_size = in_item_t['colour'] + "_" + sz
                item['skus'][color_size] = in_item_t

    # for Sku price
    def get_sku_price(self, sel1, in_item):
        # price
        price = sel1.xpath("//div[@class='product-main-info']"
                           "/div/span/span[@class='price']/text()").extract()
        if not len(price):
            price = sel1.xpath("//p[@class='special-price']"
                               "/span[@class='price']/text()").extract()
        in_item['price'] = re.sub("[^\d\.]", "", price[0].strip())

    # for sku previous prices
    def get_sku_previous_price(self, sel1, in_item):
        # previous pricess
        prev = []
        for i in sel1.xpath(
                "//div[@class='product-main-info']/div/p[@class='old-price']"
                "/span[@class='price']/text()").extract():
            prev.append(i.strip())
        in_item['previous_prices'] = []
        for s in prev:
            in_item['previous_prices'].append(re.sub("[^\d\.]", "", s))

    # for sku color
    def get_sku_color(self, sel1, in_item):
        # color
        in_item['colour'] = sel1.xpath("//li[@class='active']"
                                       "/a/img[@class='has-tip']/@alt").extract()[0].strip()

    # for sku available sizes
    def get_sku_size_list(self, sel1):
        # size available
        size_list = [i.strip() for i in sel1.xpath(
            "//ul/li[@class='size-box ship-available']/text()").extract()]

        # if page doesnt have size
        if (not size_list) or (size_list[0] == "0"):
            size_list = ["oneSize"]

        return size_list

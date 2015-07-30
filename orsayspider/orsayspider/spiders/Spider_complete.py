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

    # this will extract all the links of the products in website.Also includes pagination
    rules = (Rule(SgmlLinkExtractor(restrict_xpaths=("//ul[@id='nav']/li/ul/li/a",
                                                     "//div[@class='pages']/ul[@class='pagination']"
                                                     "/li/a[@title='Weiter']",)),
                  follow=True),
             Rule(SgmlLinkExtractor(restrict_xpaths=("//ul[@id='products-list']/li/article/div/a",)),
                  callback="parse_product")
             )

    # it parses all the details of one particular product
    def parse_product(self, response):

        sel = response.xpath("/html")

        # just to make things little simpler
        # sel1 is used when we are getting more specific information related to product main
        sel1 = response.xpath("//div[@id='product_main']")

        # Making an object of our class present in items.py
        item = orsayItem()

        item['retailer_sku'] = self.get_retailer_sku(sel1)
        item['description'] = self.get_description(sel)
        item['category'] = self.get_category(response.url)
        item['image_urls'] = self.get_image_urls(sel)
        item['care'] = self.get_care(sel)
        item['lang'] = self.get_lang(sel)
        item['name'] = self.get_name(sel1)
        item['currency'] = self.get_currency(sel1)
        item['url_orignal'] = response.url
        item['skus'] = {}
        item['skus'] = self.get_skus(sel)

        more_colors = self.get_colors(sel)
        return self.make_sku_requests(more_colors, item)

    # for sku request for more colors
    def make_sku_requests(self, more_colors, item):
        if more_colors:
            full_url = more_colors.pop(0)
            # full_url = response.urljoin(my_url)
            req = scrapy.Request(full_url, callback=self.parse_color_sku,
                                 meta={'item': item, 'urls': more_colors})
            yield req
        else:
            yield item

    # for colors list
    def get_colors(self, sel):
        colors = sel.xpath("//ul[@class='product-colors']/li/a/@href").extract()
        if colors:
            # remove the current colors
            # saves one page crawling
            my_url = colors.pop(0)
        return colors

    # for sku retailer id
    def get_retailer_sku(self, sel1):
        sku = ""
        sku = sel1.xpath("//p[@class='sku']/text()").extract()
        if sku:
            sku1 = sku[0].strip()
            sku = re.findall('\d{6}', sku1)[0]
        return sku

    # for product description
    def get_description(self, sel):
        description = [i.strip() for i in
                       sel.xpath("//div[@class='product-info six columns']"
                                 "/p/text()").extract()]
        return description

    # extracting the category from url
    def get_category(self, url):
        category = []
        url_link = url.split("/")
        if (len(url_link) > 5):
            category = url_link[4:-1]
        return category

    # image urls
    def get_image_urls(self, sel):
        return sel.xpath("//div[@id='product_media']/div/img/@src").extract()

    # care for product
    def get_care(self, sel):
        care = [i.strip() for i in
                sel.xpath("//p[@class='material']/text() |"
                          " //ul[@class='caresymbols']/li/img/@src").extract()]
        return care

    # for language
    def get_lang(self, sel):
        return sel.xpath("/html/@lang").extract()[0]

    # for product name
    def get_name(self, sel1):
        return sel1.xpath("//h2[@class='product-name']/text()").extract()[0].strip()

        # for getting currency

    def get_raw_price_currency(self, sel1):
        # price for currency
        price_curr = sel1.xpath("//div[@class='product-main-info']"
                                "//span[@class='price']/text()").extract()
        if not price_curr:
            price_curr = sel1.xpath("//p[@class='special-price']"
                                    "//span[@class='price']/text()").extract()
        return price_curr

    # for getting currency
    def get_currency(self, sel1):
        # price for currency
        currency = self.get_raw_price_currency(sel1)
        return currency[0].strip()[-3:]

    # for skus
    def get_skus(self, sel1):
        # sku as dictionary
        item_sku = {}

        in_item = skuItem()

        in_item['price'] = self.get_sku_price(sel1)
        in_item['previous_prices'] = self.get_sku_previous_price(sel1)
        in_item['currency'] = self.get_currency(sel1)
        # getting selected color info ..
        # as each color is associated with different retailer_id
        in_item['colour'] = self.get_sku_color(sel1)
        # size available
        size_list = self.get_sku_size_list(sel1)

        # adding sku with color+size key in skus dictionary
        for sz in size_list:
            in_item_t = skuItem(in_item)
            in_item_t['size'] = sz
            color_size = in_item_t['colour'] + "_" + sz
            item_sku[color_size] = in_item_t

        return item_sku

    # for Sku price
    def get_sku_price(self, sel1):
        # price
        price = self.get_raw_price_currency(sel1)
        return re.sub("[^\d\.]", "", price[0].strip())

    # for sku previous prices
    def get_sku_previous_price(self, sel1):
        # previous pricess
        prev_prices = []
        for s in sel1.xpath("//div[@class='product-main-info']//p[@class='old-price']"
                            "//span[@class='price']/text()").extract():
            prev_prices.append(re.sub("[^\d.]", "", s.strip()))
        return prev_prices

    # for sku color
    def get_sku_color(self, sel1):
        # color
        color = sel1.xpath("//li[@class='active']"
                           "/a/img[@class='has-tip']/@alt").extract()
        if color:
            return color[0].strip()
        else:
            return "no_color"

    # for sku available sizes
    def get_sku_size_list(self, sel1):
        # size available
        size_list = [i.strip() for i in sel1.xpath(
            "//ul/li[@class='size-box ship-available']/text()").extract()]

        # if page doesnt have size
        if (not size_list) or (size_list[0] == "0"):
            size_list = ["oneSize"]

        return size_list

    def parse_color_sku(self, response):

        item = response.meta["item"]
        urls = response.meta["urls"]

        sel = response.xpath("/html")
        sel1 = response.xpath("//div[@id='product_main']")

        # images of new color
        images = self.get_image_urls(sel)
        item['image_urls'].extend(images)

        color_skus_dict = self.get_skus(sel)
        item['skus'].update(color_skus_dict)
        return self.make_sku_requests(urls, item)

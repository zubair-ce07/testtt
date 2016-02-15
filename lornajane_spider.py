from base import BaseParseSpider, BaseCrawlSpider, clean

import urlparse, re

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst



class Mixin(object):
    retailer = 'lorajane-uk'
    market = 'AU'
    start_urls = ['http://www.lornajane.com.au/']
    UNWANTED_CATEGORIES = set(['Books', 'Exercise Mats', 'Gym Towels', 'MNB Shop',
                               'Water Bottles', 'Books by Lorna Jane Clarkson'])


class LorajaneParseSpider(BaseParseSpider, Mixin):
    name = '{0}-parse'.format(Mixin.retailer)
    take_first = TakeFirst()
    currency = 'AUD'
    brand = 'Lora Jane'
    test_urls= open("url_pattrens.txt", 'w')
    def parse(self, response):

        hxs = HtmlXPathSelector(response)

        categories = self.product_category(hxs)
        if set(categories) & Mixin.UNWANTED_CATEGORIES:
            return

        pid = self.product_id(hxs)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        if self.out_of_stock(hxs):
            return self.out_of_stock_item(hxs, response, pid)
        garment['categories'] = categories
        self.boilerplate_normal(garment, hxs, response)

        garment['spider_name'] = self.name
        garment['gender'] = 'womens'
        garment['image_urls'] = self.product_image_urls(hxs)
        garment['skus'] = self.skus(hxs)
        return garment

    def skus(self, hxs):
        skus = {}
        sizes = hxs.select(".//*[@name = 'productCodePost']")
        colours = hxs.select(".//*[@id='colour-size-picker-container']//li")

        for colour in colours:
            for size in sizes:
                sku = {}

                sku['size'] = self.take_first(size.select("@size").extract())
                if sku['size'] == 'One Sz':
                    sku['size'] = 'One Size'

                sku['price'] = self.price_str_to_int(self.take_first(size.select("@discount").extract()))
                if not sku['price']:
                    sku['price'] = self.price_str_to_int(self.take_first(size.select("@price").extract()))
                else:
                    sku['previous_prices'] = [self.price_str_to_int(self.take_first(size.select("@price").extract()))]
                sku['colour'] = self.take_first(colour.select("@title").extract())
                sku['currency'] = self.currency
                sku['out_of_stock'] = self.take_first(size.select("@stocklevel").extract()) == '0'

                skus['{0}_{1}'.format(sku['colour'], sku['size'])] = sku

        return skus

    def price_str_to_int(self, price):
        return int(re.sub('\.', '', price.strip())) if price else None

    def out_of_stock(self, hxs):
        return 'out' in hxs.select(".//*[@class='prod_block left']//text()")

    def product_brand(self, hxs):
        return self.brand

    def product_care(self, hxs):
        return []

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select(".//*[@id='productDetailUpdateable']//h2//text()")))

    def product_category(self, hxs):
        return clean(hxs.select(".//*[@id='breadcrumb']//ul//a[not(contains(text(),'Home') or contains(text(),'Categories'))]//text()"))

    def product_description(self, hxs):
        return re.sub("PH:[0-9 ]+ for more info", '', ' '.join(clean(hxs.select(".//*[@id='tab-details']//text()"))))

    def product_image_urls(self, hxs):
        urls = clean(hxs.select(".//*[@id='gallery_base']//a/@rev"))
        return [urlparse.urljoin('http://www.lornajane.com.au/', image_url) for image_url in urls]

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("(.//*[@productcode]/@productcode)[1]")))


class LorajaneCrawlSpider(BaseCrawlSpider, Mixin):

    name = '{0}-crawl'.format(Mixin.retailer)
    listings_x = [".//*[@id='ShopLink' or @id ='SaleLink']//li//a", ".//*[@class='pager']//a"]
    products_x = [".//*[@id='content']//*[@class='details']"]
    denied_paths = ['books','lornajane.com.au/(A|M)[0-9]+/', '/MNB']
    rules = [
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x, deny= denied_paths), callback='parse'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x, deny= denied_paths), callback='parse_item')
    ]
    parse_spider = LorajaneParseSpider()


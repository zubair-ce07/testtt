from base import BaseParseSpider, BaseCrawlSpider, clean, CurrencyParser
import urlparse
import re
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst


class Mixin(object):
    retailer = 'lornajane-au'
    market = 'AU'
    start_urls = ['http://www.lornajane.com.au/']


class LornajaneParseSpider(BaseParseSpider, Mixin):
    name = '{0}-parse'.format(Mixin.retailer)
    take_first = TakeFirst()
    UNWANTED_CATEGORIES = set(['Books',
     'Exercise Mats',
     'Gym Towels',
     'MNB Shop',
     'Water Bottles',
     'Books by Lorna Jane Clarkson'])

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        categories = self.product_category(hxs)

        if set(categories) & self.UNWANTED_CATEGORIES:
            return 

        pid = self.product_id(hxs)

        if not pid:
            return

        garment = self.new_unique_garment(pid)

        if not garment:
            return 

        if self.out_of_stock(hxs):
            return self.out_of_stock_item(hxs, response, pid)

        self.boilerplate_normal(garment, hxs, response)
        garment['gender'] = 'women'
        garment['image_urls'] = self.image_urls(hxs)
        garment['skus'] = self.skus(hxs)
        return garment

    def skus(self, hxs):
        skus = {}
        sizes = hxs.select(".//*[@name = 'productCodePost']")
        colours = hxs.select(".//*[@id='colour-size-picker-container']//li")

        for colour in colours:

            for size in sizes:
                sku = {}
                sku['size'] = self.take_first(size.select('@size').extract())
                sku['size'] = self.one_size if sku['size'] == 'One Sz' else sku['size']

                if not [x for x in size.select('@discount|@price').extract() if x.strip()]:
                    continue

                previous_price, sku['price'], sku['currency'] = self.extract_prices(size, '@discount|@price')

                if previous_price:
                    sku['previous_prices'] = [previous_price]

                sku['colour'] = self.take_first(colour.select('@title').extract())
                sku['currency'] = CurrencyParser.currency(
                    self.take_first(hxs.select(".//meta[@property='og:price:currency']/@content").extract()))
                sku['out_of_stock'] = self.take_first(size.select('@stocklevel').extract()) == '0'
                skus['{0}_{1}'.format(sku['colour'], sku['size'])] = sku

        return skus

    def out_of_stock(self, hxs):
        return 'out' in hxs.select(".//*[@class='prod_block left']//text()")

    def product_brand(self, hxs):
        return 'Lorna Jane'

    def product_care(self, hxs):
        return [x for x in self.raw_description(hxs) if self.care_criteria(x)]

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select(".//*[@id='productDetailUpdateable']//h2//text()")))

    def product_category(self, hxs):
        return clean(hxs.select(
            ".//*[@id='breadcrumb']//ul//a[not(contains(text(),'Home') or contains(text(),'Categories'))]//text()"))

    def raw_description(self, hxs):
        return clean(hxs.select(".//*[@id='tab-details']//text()"))

    def product_description(self, hxs):
        return [x for x in self.raw_description(hxs)
                if not re.match('PH:[0-9 ]+ for more info', x) and not self.care_criteria(x) and len(x) > 1]

    def image_urls(self, hxs):
        urls = clean(hxs.select(".//*[@id='gallery_base']/@rev"))
        return [urlparse.urljoin('http://www.lornajane.com.au/', image_url) for image_url in urls]

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select('(.//*[@productcode]/@productcode)[1]')))


class LornajaneCrawlSpider(BaseCrawlSpider, Mixin):
    name = '{0}-crawl'.format(Mixin.retailer)
    listings_x = [".//*[@id='ShopLink' or @id ='SaleLink']//li//a", ".//*[@class='pager']//a"]
    products_x = [".//*[@id='content']//*[@class='details']"]
    denied_paths = ['books', 'lornajane.com.au/(A|M)[0-9]+/', '/MNB']
    rules = [
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x, deny=denied_paths), callback='parse'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x, deny=denied_paths), callback='parse_item')]

    parse_spider = LornajaneParseSpider()

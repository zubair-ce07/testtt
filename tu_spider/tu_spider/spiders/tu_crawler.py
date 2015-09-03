import re
import json
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tu_spider.items import TuSpiderItem
from tu_spider.items import SkuItem
from scrapy.http import Request
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
import logging
import requests
import urllib2
from urlparse import urljoin


class TuCrawler(CrawlSpider):
    name = "tu"
    allowed_domians = ["tuclothing.sainsburys.co.uk"]
    start_urls = ["http://tuclothing.sainsburys.co.uk"]

    # Set the rules for scraping all the available products of a website
    rules = (
        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                "//*[@id='nav_block']/li/span",
                "//ul[@class='facet_block indent']/li")),
            callback='parse_item', follow=True
        ),
        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                "//div[@id='productContents']/div/div/a[@class='productMainLink']")),
            callback='parse_product'
        ),

    )

    def parse_skus(self, response):

        hxs = HtmlXPathSelector(text=response)
        item = SkuItem()

        p = (hxs.select("//p[@class='big-price']/span[1]/text()").extract()[0]).strip()
        item["price"] = re.sub(ur'\D', u'', p, flags=re.UNICODE)
        previous_prices = hxs.select("//p[@class='big-price']/span/strike/text()").extract()

        for i, s in enumerate(previous_prices):
            previous_prices[i] = re.sub(ur'\D', u'', s, flags=re.UNICODE)

        item["previous_prices"] = previous_prices
        item["out_of_stock"] = bool(hxs.select("//p[@class='outOfStockMessage']"))
        item["color"] = hxs.select("//p[@class='swatchDesc']/text()").extract()
        item["currency"] = hxs.select("//span[@itemprop='priceCurrency']/@content").extract()
        size = (hxs.select("//select[@id='Size']/option[@selected]/text()")[0]).extract()
        size = re.sub(ur'\D', u'', size, flags=re.UNICODE) + " years"
        item["size"] = size
        return item

    def get_skus(self, skus, response):

        # Make a dictionary
        skus_collection = {}
        skus.pop(0)
        url_domain = response.url

        for s in skus:
            # Making full URL
            url_of_sku = urljoin(url_domain, s)
            data = urllib2.urlopen(url_of_sku).read()
            skus_collection[(s).split('=')[-1]] = self.parse_skus(data)

        return skus_collection

    def parse_product(self, response):

        hxs = HtmlXPathSelector(response)

        # Extracting data from the page of one product
        url_orignal = response.url
        product_id = hxs.select("//div[@class='productDetails_product_code']/text()[2]").extract()
        brand = hxs.select("//*[@itemprop='brand']/@content").extract()
        image_urls = hxs.select('//ul[@class="productImages"]//li/a/@href').extract()
        description = (hxs.select("//div[@class='productDescription']/span/text()").extract()[0]).strip()
        description = [description] + hxs.select("//div[@id='tab-details']/ul//li/text()").extract()
        name = hxs.select("//span[@itemprop='name']/text()").extract()
        category = hxs.select("//ul[@class='clearfix']/li/a/text()").extract()
        category.pop(0)
        care_instructions = hxs.select("//div[@class='productDetails_materials']//li/text()").extract()
        care_instructions = care_instructions + hxs.select("//div[@class='productDetails_care_instructions']/text()[2]").extract()
        care_instructions[1] = care_instructions[1].strip()
        gender = category[0]
        skus = self.get_skus(hxs.select("//select[@id='Size']/option/@value").extract(), response)

        # Defining an object for storing the product data
        item = TuSpiderItem()
        item["product_id"] = product_id
        item["care"] = care_instructions
        item["category"] = category
        item["name"] = name
        item["description"] = description
        item["image_urls"] = image_urls
        item["url_orignal"] = url_orignal
        item["brand"] = brand
        item["gender"] = gender
        item["skus"] = skus
        yield item
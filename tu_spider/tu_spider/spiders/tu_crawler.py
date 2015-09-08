import re
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from tu_spider.items import TuSpiderItem
from tu_spider.items import SkuItem
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
import logging
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

    def parse_product(self, response):

        hxs = HtmlXPathSelector(response)

        # Defining an object for storing the product data
        item = TuSpiderItem()  # that will always create a new item

        # Extracting data from the page of one product
        url_original = response.url
        product_id = hxs.select("//div[@class='productDetails_product_code']/text()[2]").extract()
        brand = hxs.select("//*[@itemprop='brand']/@content").extract()
        image_urls = hxs.select('//ul[@class="productImages"]//li/a/@href').extract()
        description = (hxs.select("//div[@class='productDescription']/span/text()").extract()[0]).strip()
        description = [description] + hxs.select("//div[@id='tab-details']/ul//li/text()").extract()
        name = hxs.select("//span[@itemprop='name']/text()").extract()
        category = hxs.select("//ul[@class='clearfix']/li/a/text()").extract()
        category.pop(0)
        care_instructions = hxs.select("//div[@class='productDetails_materials']//li/text()").extract()
        care_instructions = care_instructions + hxs.select(
            "//div[@class='productDetails_care_instructions']/text()[2]").extract()
        care_instructions[1] = care_instructions[1].strip()
        gender = category[0]

        item["product_id"] = product_id
        item["care"] = care_instructions
        item["category"] = category
        item["name"] = name
        item["description"] = description
        item["image_urls"] = image_urls
        item["url_original"] = url_original
        item["brand"] = brand
        item["gender"] = gender
        item['skus'] = {}

        return self.get_skus(hxs.select("//select[@id='Size']/option/@value").extract(), item, response.url)
         

    def get_skus(self, skus, item, url):

        for s in skus[1:]:
            # Making full URL
            url_of_sku = urljoin(url, s)
            yield Request(url_of_sku, callback=self.parse_skus, meta={'item': item}, dont_filter=True)

    def parse_skus(self, response):

        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        skus_collection = item['skus']
        logging.info(skus_collection)

        item1 = SkuItem()

        p = (hxs.select("//p[@class='big-price']/span[1]/text()").extract()[0]).strip()
        item1["price"] = re.sub(ur'\D', u'', p, flags=re.UNICODE)
        previous_prices = hxs.select("//p[@class='big-price']/span/strike/text()").extract()

        for i, s in enumerate(previous_prices):
            previous_prices[i] = re.sub(ur'\D', u'', s, flags=re.UNICODE)

        item1["previous_prices"] = previous_prices
        item1["out_of_stock"] = bool(hxs.select("//p[@class='outOfStockMessage']"))
        item1["color"] = hxs.select("//p[@class='swatchDesc']/text()").extract()
        item1["currency"] = hxs.select("//span[@itemprop='priceCurrency']/@content").extract()
        size = (hxs.select("//select[@id='Size']/option[@selected]/text()")[0]).extract()
        size = re.sub(ur'\D', u'', size, flags=re.UNICODE) + " years"
        item1["size"] = size
        skus_collection[(response.url).split('=')[-1]] = item1
        item['skus'] = skus_collection
        yield item


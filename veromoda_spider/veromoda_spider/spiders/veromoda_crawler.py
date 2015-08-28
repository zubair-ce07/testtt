import re
import json
from scrapy.spiders 		import BaseSpider
from scrapy.selector 		import HtmlXPathSelector
from veromoda_spider.items		import VeromodaSpiderItem
from veromoda_spider.items		import skuItem
from scrapy.http		import Request
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
import logging


class VeromodaCrawler(CrawlSpider):

    name = "veromoda"
    allowed_domians = ["veromoda.com"]
    start_urls = ["http://www.veromoda.com/"]

    # Set the rules for scraping all the avaliable products of a website
    rules = (
        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                "//*[@id='category_1']/a",
                "//*[@id='category-level-1']/li/a")),
            callback='parse_item',follow=True
        ),
        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                "//div[@class='thumbnail']/a")),
            callback='parse_product'
        ),

    )

    def get_skus(self, skus, product_id):

        product_id = str(product_id[0])
        # Make a dictionary
        skus_collection={}

        # Using regular expression to remove comments
        skus = re.sub(ur'\s', u'', skus, flags=re.UNICODE)
        logging.info(type(skus))
        skus = re.sub(ur'<!--\[\w*\]>', u'', skus, flags=re.UNICODE)
        skus = re.sub(ur'<!\[\w*\]-->', u'', skus, flags=re.UNICODE)

        # Convert string to dictionary
        skus = json.loads(skus)

        # Check how many items are there in the dictionary

        for s in skus[product_id]["variations"]["variants"]:

            item = skuItem()
            item["price"] = s["pricing"]["standard"]
            item["out_of_stock"] = not(s["inWarehouse"])
            item["color"] = s["attributes"]["colorPattern"]
            item["size"] = s["attributes"]["size"]
            skus_collection[s["id"]] = item

        return skus_collection


    def parse_product(self, response):

        hxs = HtmlXPathSelector(response)

        # Extracting data from the page of one product
        category = hxs.select('//div[@id="breadcrumb"]/div/a/span/text()').extract()
        care_instructions = hxs.select('//div[@class="tabs__half  tabs__half--last"]/div[@class="tabs__content"]/p/text()').extract()
        name = (hxs.select('//h1[@class="productname"]/text()').extract()[0]).strip()
        description = hxs.select('//div[@class="tabs__half tabs__half--first"]/div[@class="tabs__content"]/p/text()').extract()
        img_urls = self.get_images(hxs.select('(//div[@id="pdpMain"]//script)[7]/text()').extract()[0])
        url_orignal = response.url
        brand = hxs.select('//*[@id="jsCurrentBrand"]/text()').extract()
        product_id = hxs.select('//div[@class="productimage js-product-image concealed"]/a/@href').extract()

        # Defining an object for storing the product data
        item = VeromodaSpiderItem()
        item ["product_id"] = product_id
        item["care"] = care_instructions[0]
        item["category"] = category
        item["name"] = name
        item["description"] = description
        item["image_urls"] = img_urls
        item["url_orignal"] = url_orignal
        item["brand"] = brand
        skus = self.get_skus(hxs.select('//div[@id="jsVariantsJSON"]/comment()').extract()[0], product_id)
        item["skus"] = skus
        yield item

    def get_images(self, image_urls):

        # Remove white space characters
        image_urls = image_urls.strip()
        # Getting only urls from the given string
        image_urls = re.findall('http.*jpg', image_urls)

        return image_urls


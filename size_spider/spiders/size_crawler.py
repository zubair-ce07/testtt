from size_spider.items import SizeSpiderItem
from size_spider.items import SkuItem
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.http import Request
from scrapy.selector import Selector
import logging
import json
import re


class SizeCrawler(CrawlSpider):

    name = "size-uk-crawl"
    allowed_domians = ["size.co.uk"]
    start_urls = ["http://www.size.co.uk"]

    #: Set the rules for scraping all the available products of a website
    rules = (
        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                "(//*[@id='primaryNavigation']/li/span/a)[position() >= 3]",  # get all cloths, footwear and accessories
            )),
            follow=False, callback='add_gender'
        ),
    )

    def add_gender(self, response):

        hxs = Selector(response)
        urls = hxs.xpath("//*[@id='categoryMenu']//li/a/@href").extract()

        #: Modifying url else it will give 402 error
        for i in range(len(urls)):
            url1 = urls[i].split('uk')
            urls[i] = url1[0] + 'uk/' + response.url.split('/')[-2] + url1[1]

        #: Separating the Requests based on the gender
        yield Request(urls[0], callback=self.get_product_links, meta={'gender': 'For women'})

        for url in urls[1:]:
            yield Request(url, callback=self.get_product_links, meta={'gender': 'For men'})

    def get_product_links(self, response):

        hxs = Selector(response)
        products_links = hxs.xpath("//div[@class='product-list gallery-view medium-images']/ol//h2/a/@href").extract()
        #: Get all Products
        for link in products_links:
            yield Request(link, callback=self.parse_product, meta={'gender': response.meta.get('gender')})

    def parse_product(self, response):

        l = ItemLoader(item=SizeSpiderItem(), response=response)
        l.add_value('spider_name', self.name)
        l.add_value('retailer', 'size-uk')
        l.add_xpath('currency', '//*[@id="productAttributes"]/comment()[1]')
        l.add_value('market', 'UK')
        l.add_xpath('category', '//div[@id="breadCrumbTrail"]/a/text()')
        l.add_value('retailer_sku', response.url.split('/')[-2])
        l.add_xpath('price', '//*[@id="productName"]/div/text()')
        l.add_xpath('description', '//div[@id="productInfo"]/p/text()')
        l.add_xpath('brand', '(//h1[@class="product-name fn"]/text())[1]')
        l.add_value('skus', self.get_skus(response))
        l.add_xpath('care', '//div[@id="productInfo"]/p/text()')
        l.add_xpath('name', '(//h1[@class="product-name fn"]/text())[1]')
        l.add_value('url', response.url)
        l.add_value('gender', response.meta['gender'])
        url = str(Selector(response).xpath('//img[@class="mainImage"]/@src')[0].extract().split('_a')[0]+'_is.js').replace('/i/','/s/')
        yield Request(url, callback=self.get_images, meta={'item': l})

    def get_skus(self, response):

        skus_collection = {}
        #: Getting the full list of all elements of skus
        l1 = ItemLoader(item=SkuItem(), response=response)
        l1.add_xpath('size', '//div[@class="product-size"]//ul/li//span/text()')
        l1.add_xpath('out_of_stock', '//div[@class="product-size"]//ul/li/@title')
        l1.add_xpath('price', '//*[@id="productName"]/div/text()')
        l1.add_xpath('color', '//div[@id="productInfo"]/p/text()[2]')
        l1.add_xpath('currency', '//*[@id="productAttributes"]/comment()[1]')
        items = l1.load_item()

        #: Now separate the list of items and place in SkuItem individually
        for item in items['size']:
            new_item = SkuItem()
            new_item['color'] = items['color']
            new_item['price'] = items['price']
            new_item['currency'] = items['currency']
            new_item['size'] = item
            new_item['out_of_stock'] = items['out_of_stock'][items['size'].index(item)]
            skus_collection['{0}_{1}'.format(str(new_item['color']), str(item))] = new_item

        return skus_collection

    def get_images(self, response):

        l = response.meta['item']
        json_data = response.body
        json_data = re.search('{.*}', json_data).group()
        json_data = json.loads(unicode(json_data))

        for item in json_data['items']:
            l.add_value('image_urls', item['src'])

        return l.load_item()
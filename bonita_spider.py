from tutorial.items import ProductItem, SkuItem, SkuItemDetail
from scrapy.loader import ItemLoader

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BonitaSpider(CrawlSpider):
    name = "bonita"
    allowed_domains = ["bonita.de"]
    start_urls = ["http://www.bonita.de"]

    product = ProductItem()
    product['brand'] = 'bonita'
    product['lang'] = 'de'
    product['market'] = 'DE'
    product['retailer'] = 'bonita-de'

    rules = (
        Rule(LinkExtractor(allow=('http://www.bonita.de/home/women', 'http://www.bonita.de/home/men'))),
        Rule(LinkExtractor(restrict_xpaths=('//ul[@id="categoryContentMenu"]/li[1]/ul/li',
                                            '//nav[@class="paginator"]/ul/li[@class="next"]'))),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="categoryArticleWrapperWrapper"]'
                                           '/div[@class="categoryArticleWrapper"]/div[@class="categoryArticle"]'),
             callback='parse_product_info')
    )

    def parse_product_info(self, response):
        productItemLoader = ItemLoader(self.product, response=response)
        productItemLoader.add_xpath('care', '//div[@id="materials"]/div[@class="material"]/strong/text()'
                                            '|//div[@id="materials"]/div[@class="material"]/text()'
                                            '|//div[@id="materials"]/span/strong/text()'
                                            '|//div[@id="materials"]/ul[@id="careInstructions"]/li/span/text()')
        productItemLoader.add_xpath('category', '//nav[@class="breadCrumb"]/span[not(@class="first")]/a/span/text()'
                                                '|//nav[@class="breadCrumb"]/span/span/text()')
        productItemLoader.add_xpath('description', '//div[@id="infos"]/p/text()'
                                                   '|//div[@id="toggleStatic"]/ul/li/text()')
        productItemLoader.add_xpath('gender', '//nav[@class="breadCrumb"]/span[2]/a/span/text()')
        productItemLoader.add_xpath('image_urls', '//div[@id="articleImagesSmallWrapperWrapper"]/div/a/@href')
        productItemLoader.add_xpath('name', '//div[@id="articleLabel"]/h1/text()')
        productItemLoader.add_xpath('retailer_sku', '//div[@id="infos"]/strong/text()')
        skuDict = self.parse_skus(response)
        productItemLoader.add_value('skus', skuDict)
        productItemLoader.load_item()
        return self.product

    def parse_skus(self, response):
        skuDict = dict()
        for selector in response.xpath('.//div[@id="articleSizes"]/div/a'):
            skuItem = SkuItem()
            skuItemLoader = ItemLoader(skuItem, response=response)
            skuDetailItem = SkuItemDetail()
            key = selector.xpath('@data-articleid').extract()
            size = selector.xpath('text()').extract()
            skuDetailItemLoader = ItemLoader(skuDetailItem, response=response)
            skuDetailItemLoader.add_value('currency', 'EUR')
            skuDetailItemLoader.add_value('size', size)
            skuDetailItemLoader.add_xpath('colour', '//div[@id="articleColors"]/a/@title')
            skuDetailItemLoader.add_xpath('previous_prices',
                                          '//div[@id="articlePrice"]/span[@class="price sale"]/text()')
            skuDetailItemLoader.add_xpath('price',
                                          '//div[@id="articlePrice"]/span[@class="price" or @class="salePrice"]/text()')
            skuDetailItemLoader.load_item()
            skuDict[key[0]] = skuDetailItem
        return skuDict

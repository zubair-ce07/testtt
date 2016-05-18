from tutorial.items import ProductItem, SkuItem, SkuItemDetail
from scrapy.loader import ItemLoader

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BonitaSpider(CrawlSpider):
    name = "bonita"
    allowed_domains = ["bonita.de"]
    start_urls = ["http://www.bonita.de"]

    rules = (
        Rule(LinkExtractor(allow=('http://www.bonita.de/home/women', 'http://www.bonita.de/home/men'))),
        Rule(LinkExtractor(restrict_xpaths=('//ul[@id="categoryContentMenu"]/li[1]/ul/li/a',
                           '//nav[@class="paginator"]/ul/li[@class="next"]/a'))),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="categoryArticleWrapperWrapper"]'
                                           '/div[@class="categoryArticleWrapper"]/div[@class="categoryArticle"]/a'),
             callback='parse_product_info')
    )

    def parse_product_info(self, response):
        product = ProductItem()
        product['brand'] = 'bonita'
        product['gender'] = ''
        product['lang'] = 'de'
        product['market'] = 'DE'
        product['retailer'] = 'bonita-de'
        product['gender'] = ''
        productItemLoader = ItemLoader(product, response=response)
        productItemLoader.add_xpath('care', '//div[@id="materials"]/div[@class="material"]/strong/text()')
        productItemLoader.add_xpath('care', '//div[@id="materials"]/div[@class="material"]/text()')
        productItemLoader.add_xpath('care', '//div[@id="materials"]/span/strong/text()')
        productItemLoader.add_xpath('care', '//div[@id="materials"]/ul[@id="careInstructions"]/li/span/text()')
        productItemLoader.add_xpath('category', '//nav[@class="breadCrumb"]/span[2]/a/span/text()')
        productItemLoader.add_xpath('category', '//nav[@class="breadCrumb"]/span[3]/a/span/text()')
        productItemLoader.add_xpath('category', '//nav[@class="breadCrumb"]/span/span/text()')
        productItemLoader.add_xpath('description', '//div[@id="infos"]/p/text()')
        productItemLoader.add_xpath('description', './/div[@id="toggleStatic"]/ul/li/text()')
        productItemLoader.add_xpath('gender', '//nav[@class="breadCrumb"]/span[2]/a/span/text()')
        productItemLoader.add_xpath('image_urls', '//div[@id="articleImagesSmallWrapperWrapper"]/div/a/@href')
        productItemLoader.add_xpath('name', '//div[@id="articleLabel"]/h1/text()')
        productItemLoader.add_xpath('retailer_sku', '//div[@id="infos"]/strong/text()')

        skuDict = dict()
        for selector in response.xpath('.//div[@id="articleSizes"]/div/a'):
            skuItem = SkuItem()
            skuItemLoader = ItemLoader(skuItem, response=response)
            skuDetailItem = SkuItemDetail()
            key = selector.xpath('@data-articleid').extract()
            size = selector.xpath('text()').extract()
            skuDetailItemLoader = ItemLoader(skuDetailItem, response=response)
            skuDetailItemLoader.add_xpath('colour', '//div[@id="articleColors"]/a/@title')
            skuDetailItemLoader.add_value('currency', 'EUR')
            skuDetailItemLoader.add_xpath('previous_prices',
                                          '//div[@id="articlePrice"]/span[@class="price sale"]/text()')
            skuDetailItemLoader.add_xpath('price',
                                          '//div[@id="articlePrice"]/span[@class="price" or @class="salePrice"]/text()')
            skuDetailItemLoader.add_value('size', size)
            skuDetailItemLoader.load_item()

            skuDict[key[0]] = skuDetailItem

        productItemLoader.add_value('skus', skuDict)
        productItemLoader.load_item()
        return product

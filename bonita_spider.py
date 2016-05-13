import scrapy

from tutorial.items import ProductItem, SkuItem, SkuItemDetail
from scrapy.loader import ItemLoader


class BonitaSpider(scrapy.Spider):
    name = "bonita"
    allowed_domains = ["bonita.de"]
    start_urls = ["http://www.bonita.de"]

    def parse(self, response):
        for href in response.xpath('//div[@id="primaryMenu"]/nav/a'):
            product = ProductItem()
            product['brand'] = 'bonita'
            product['gender'] = ''
            product['lang'] = 'de'
            product['market'] = 'DE'
            product['retailer'] = 'bonita-de'
            gender = href.xpath('text()').extract()[0]
            url = href.xpath('@href').extract()[0]
            if gender == 'DAMEN':
                product['gender'] = 'women'
                request = scrapy.Request(url, callback=self.parse_category_links)
                request.meta['product'] = product
                yield request
            if gender == 'HERREN':
                product['gender'] = 'men'
                request = scrapy.Request(url, callback=self.parse_category_links)
                request.meta['product'] = product
                yield request

    def parse_category_links(self, response):
        for href in response.xpath('//ul[@id="categoryContentMenu"]/li[1]/ul/li/a/@href'):
            url = href.extract()

            request = scrapy.Request(url, callback=self.parse_category_pagination_links)
            request.meta['product'] = response.meta['product']
            yield request

    def parse_category_pagination_links(self, response):
        pageLinks = [response.url]
        hasNextPage = response.xpath(
            '//div[@id="categoryPaginationTop"]/div[@class="categoryPageList"]/nav/ul/li/a').extract()
        if hasNextPage:
            for href in response.xpath('//div[@id="categoryPaginationTop"]/div[@class="categoryPageList"]/nav/ul/li'):
                page = href.xpath('a/text()').extract()
                if page:
                    pageLinks.append(href.xpath('a/@href').extract()[0])
        for pageLink in pageLinks:
            url = pageLink
            request = scrapy.Request(url, callback=self.parse_product_links)
            request.meta['product'] = response.meta['product']
            yield request

    def parse_product_links(self, response):
        for href in response.xpath(
                '//div[@id="categoryArticleWrapperWrapper"]/div[@class="categoryArticleWrapper"]'
                '/div[@class="categoryArticle"]/a/@href'):
            url = href.extract()
            request = scrapy.Request(url, callback=self.parse_product_info)
            request.meta['product'] = response.meta['product']
            yield request

    def parse_product_info(self, response):
        product = response.meta['product']
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

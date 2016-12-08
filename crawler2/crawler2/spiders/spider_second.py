#!/usr/bin/python3

import scrapy
from scrapy.spiders import CrawlSpider, BaseSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
from crawler2.items import Crawler2Item
import time


class ScrapySpider(CrawlSpider):
    name = "spider_second"
    allowed_domains = ["orsay.com"]
    start_urls = ["http://www.orsay.com/de-de/"]
    rules = (Rule(LinkExtractor(restrict_xpaths=['//*[@class="pages"]'
                                                 , '//*[@class="main-navigation"]'
                                                 ])),
             Rule(LinkExtractor(restrict_xpaths=['//*[@id="products-list"]']),
                  callback='parse_item'
                  ))

    def parse_item(self, response):
        item = Crawler2Item()
        print('\n***************************** GETTING URL:\n%s' % response.url)
        item['spider_name'] = self.name
        item['uuid'] = "None"
        item['industry'] = "None"
        item['crawl_id'] = "None"
        item['product_hash'] = "None"

        item['crawl_start_time'] = time.ctime(time.time())

        bodyscript_22 = response.xpath('//*[@id="body"]/script[22]/text()').extract()[0]
        bodyjson_22 = json.loads(bodyscript_22)
        bodyscript_24 = response.xpath('//*[@id="body"]/script[24]/text()').extract()[0]
        bodyscript_18 = response.xpath('//*[@id="body"]/script[18]').extract()[0]

        currency = bodyjson_22[2]['offers']['priceCurrency']
        item['currency'] = currency
        price = bodyjson_22[2]['offers']['price']
        item['price'] = price

        retailer_sku = bodyjson_22[2]['sku']
        item['retailer_sku'] = retailer_sku
        item['retailer'] = bodyjson_22[2]['manufacturer']['name']
        item['category'] = bodyjson_22[2]['category']
        len_trail = len(bodyjson_22[1]['itemListElement'])
        item['trail'] = []
        for i in range(0, len_trail - 1):
            trailitem = bodyjson_22[1]['itemListElement'][i]['item']['name'], bodyjson_22[1]['itemListElement'][i]['item']['@id']
            item['trail'].append(trailitem)

        item['brand'] = bodyjson_22[2]['brand']['name']
        item['url'] = bodyjson_22[1]['itemListElement'][-1]['item']['@id']
        item['name'] = bodyjson_22[1]['itemListElement'][-1]['item']['name']

        url_original = response.xpath('/html/head/link[5]/@href').extract()[0]
        item['url_original'] = url_original

        ind1 = bodyscript_24.find('customer_gender')
        ind2 = bodyscript_24.find(',', ind1)
        gender = bodyscript_24[ind1 + len('"customer_gender":"') - 1:ind2 - 1]
        item['gender'] = "women" if (gender == 'female') else "men"

        ind1 = bodyscript_18.find('google_base_country')
        ind2 = bodyscript_18.find(']', ind1)
        market = bodyscript_18[ind1 + len('"google_base_country", "') - 1:ind2 - 1]
        item['market'] = market

        ind1 = bodyscript_18.find('google_base_language')
        ind2 = bodyscript_18.find(']', ind1)
        lang = bodyscript_18[ind1 + len('"google_base_language", "') - 1:ind2 - 1]
        item['lang'] = lang

        sDesc = response.xpath('//*[@id="product_main"]/div[7]/div/div[1]//*[@class="description"]/text()').extract()
        item['description'] = sDesc
        item['care'] = []

        sMaterial = response.xpath('//*[@id="product_main"]/div[7]/div/div[2]//*[@class="material"]/text()').extract()
        for mat in sMaterial:
            item['care'].append(mat)

        sCare = response.xpath('//*[@id="product_main"]/div[7]/div/div[2]//*[@class="caresymbols"]//@src').extract()
        for caresym in sCare:
            item['care'].append(caresym)
        item['date'] = 'None'

        colors = response.xpath('//*[@id="product_main"]/div[3]/ul//li//@title').extract()
        subUrls = response.xpath('//*[@id="product_main"]/div[3]/ul//li//@href').extract()
        for i in range(0, len(subUrls)):
            if subUrls[i] == '#':
                skusSizes = response.xpath('//*[@id="product-options-wrapper"]/dl/dd/div/div//li/text()').extract()
                skusSizes = [s.strip() for s in skusSizes]
                skusAvailability = response.xpath('//*[@id="product-options-wrapper"]/dl/dd/div/div//li/@data-qty').extract()
                skus = {}
                for j in range(0, len(skusSizes)):
                    skus[retailer_sku + '_' + skusSizes[j]] = {}
                    skus[retailer_sku + '_' + skusSizes[j]]['currency'] = currency
                    skus[retailer_sku + '_' + skusSizes[j]]['price'] = price
                    if skusAvailability[j] == '0':
                        skus[retailer_sku + '_' + skusSizes[j]]['out_of_stock'] = 'True'
                    else:
                        skus[retailer_sku + '_' + skusSizes[j]]['out_of_stock'] = 'False'
                    skus[retailer_sku + '_' + skusSizes[j]]['colour'] = colors[i]
                    skus[retailer_sku + '_' + skusSizes[j]]['size'] = skusSizes[j]

                item['skus'] = skus
                image_urls = response.xpath('//*[@id="product_media"]/div[1]//img/@src').extract()
                item['image_urls'] = image_urls
                if len(subUrls) <= 1:
                    # print('One Color Item')
                    yield item
                # else:
                #     print('Multi Color Item')
            else:
                yield scrapy.Request(subUrls[i], self.parse_sublink, dont_filter=True,
                                     meta={'item': item, 'ref': response.url, 'colorIndex': i, 'colorTotal': len(subUrls)})
                print('Multi Color Item, ', subUrls[i])

    def parse_sublink(self, response):
        print("colorVariant", response.url, "Ref:", response.meta['ref'])
        colorIndex = response.meta.get('colorIndex')
        colorTotal = response.meta.get('colorTotal')
        item = response.meta.get('item')
        bodyscript_22 = response.xpath('//*[@id="body"]/script[22]/text()').extract()[0]
        bodyjson_22 = json.loads(bodyscript_22)
        currency = bodyjson_22[2]['offers']['priceCurrency']
        price = bodyjson_22[2]['offers']['price']

        retailer_sku = bodyjson_22[2]['sku']

        colors = response.xpath('//*[@id="product_main"]/div[3]/ul//li//@title').extract()
        subUrls = response.xpath('//*[@id="product_main"]/div[3]/ul//li//@href').extract()

        skusSizes = response.xpath('//*[@id="product-options-wrapper"]/dl/dd/div/div//li/text()').extract()
        skusSizes = [s.strip() for s in skusSizes]
        skusAvailability = response.xpath('//*[@id="product-options-wrapper"]/dl/dd/div/div//li/@data-qty').extract()
        skus = item['skus']
        for i in range(0, len(subUrls)):
            if subUrls[i] == '#':
                for j in range(0, len(skusSizes)):
                    skus[retailer_sku + '_' + skusSizes[j]] = {}
                    skus[retailer_sku + '_' + skusSizes[j]]['currency'] = currency
                    skus[retailer_sku + '_' + skusSizes[j]]['price'] = price
                    if skusAvailability[j] == '0':
                        skus[retailer_sku + '_' + skusSizes[j]]['out_of_stock'] = 'True'
                    else:
                        skus[retailer_sku + '_' + skusSizes[j]]['out_of_stock'] = 'False'
                    skus[retailer_sku + '_' + skusSizes[j]]['colour'] = colors[i]
                    skus[retailer_sku + '_' + skusSizes[j]]['size'] = skusSizes[j]

                item['skus'] = skus
                image_urls_new = response.xpath('//*[@id="product_media"]/div[1]//img/@src').extract()
                for imgsrc in image_urls_new:
                    item['image_urls'].append(imgsrc)

        if int(colorIndex) == int(colorTotal)-1:
            print('JSON COMPLETE, FOR: ', response.meta['ref'])
            yield item
        # else:
            # print('more to come')

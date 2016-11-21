#!/usr/bin/python2.7

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import json
from crawler1.items import Crawler1Item


# class ScrapySpider(scrapy.Spider):
class ScrapySpider(CrawlSpider):
    name = "spider_first"
    allowed_domains = ["bluefly.com"] # Where the spider is allowed to go
    start_urls = ["http://www.bluefly.com"]
    # start_urls = ["http://www.bluefly.com/bungalow-20-sleeveless-overlay-top-with-jeweled-neckline/p/416904201"]
    # start_urls = ["http://www.bluefly.com/m-bottiglieri-classic-cotton-poplin-button-down-hudson-shirt/p/367310204?green=5D2302FD-EEDF-5530-0800-DA9D32D6CFBD&cm_vc=PDP"]
    # start_urls = ["http://www.bluefly.com/m-bottiglieri-silk-collared-waverly-shirt/p/367310802?green=5D2302FD-EEDF-5530-0800-DA9D32D6CFBD&cm_vc=PDP"]
    # start_urls = ["http://www.bluefly.com/tavan-tavan-jeanne-ladies-watch/p/382995612?green=5D2302FD-EEDF-5530-0800-DA9D32D6CFBD&cm_vc=PDP"]
    # start_urls = ["http://www.bluefly.com/fly-london-fly-london-piat-leather-wedge/p/398002701"]
    # start_urls = ["http://www.bluefly.com/tods-tods-suede-slipon/p/396681401"]

    # rules = (
    # Rule(LinkExtractor(restrict_css=["#nav", ".pagination"])),
    # Rule(LinkExtractor(restrict_css=".product-image"), callback="parse_item")
    # )

    rules = (Rule(LinkExtractor(restrict_xpaths=['//*[@id="page-wrapper"]/header/div/nav', '//*[@class="mz-pagenumbers"]'])),
             Rule(LinkExtractor(restrict_xpaths='//*[@class="mz-productlist-item"]'), callback='parse_item'))


    # def parse(self, response):


    def parse_item(self, response):
        item = Crawler1Item()
        # self.log('\n\n************************************************************************************************'
        #          '***********\nGETTING URL:\n%s\n*********************************************************************'
        #          '*****************\n\n' % response.url)
        print('\n******************'
                 '*********** GETTING URL:\n%s\n*************************************'
                 '*****************\n' % response.url)

        # hxs = scrapy.Selector(response)  # The XPath selector
        # hxs = scrapy.HtmlXPathSelector(response)  # The XPath selector
        # hxs = Selector(response)

        # item['field1'] = response.url
        # item['field2'] = response.xpath('//title')[0]
        # item['field2'] = response.xpath('//title/text()')[0].extract()
        # print(response.url)
        # print(response.xpath('//title'))
        # print(response.xpath('//title')[0])
        # print(response.xpath('//title')[0].extract())
        # print(response.xpath('//title/text()')[0].extract())
        # print(response.xpath('/html/head/meta[15]').extract())
        # print(response.xpath('/html/head/meta[15]'))
        # print(response.xpath('//meta[@property="og:site_name"]').extract())
        # print(hxs.select('//meta[@property="og:site_name"]').extract())

        # print("--{0}\n{1}\n".format("select0", response.xpath('//meta[@property="og:site_name"]').extract()))
        # print("--{0}\n{1}\n".format("select0", response.xpath('//meta[@property="og:site_name"]')[0].extract()))
        # print("--{0}\n{1}\n".format("select1", response.xpath('/html/head/meta[15]').extract()))
        # print("--{0}\n{1}\n".format("select2", response.xpath('//*[@id="page-content"]/div[2]/script[2]').extract()))
        # print("--{0}\n{1}\n".format("select4", response.xpath('//*[@id="data-mz-preload-apicontext"]/text()').extract()))
        # print("--{0}\n{1}\n".format("select40", response.xpath('//*[@id="data-mz-preload-apicontext"]').extract()))
        # print("--{0}\n{1}\n".format("select5", response.xpath('//*[@id="data-mz-preload-apicontext"]/text()').extract()))
        # print("--{0}\n{1}\n".format("select6", response.xpath('//*[@id="page-content"]/div[1]').extract()))
        # print("--{0}\n{1}\n".format("select7", response.xpath('//*[@id="page-content"]/div[1]/a[1]').extract()))
        # print("--{0}\n{1}\n".format("select8", response.xpath('//*[@id="page-content"]/div[1]/a[2]').extract()))
        # print("--{0}\n{1}\n".format("select80", response.xpath('//a[@class="mz-breadcrumb-link"]/text()').extract()))
        # print("--{0}\n{1}\n".format("select81", response.xpath('//a[@class="mz-breadcrumb-link"][1]/text()').extract()))
        # print("--{0}\n{1}\n".format("select81", response.xpath('//a[@class="mz-breadcrumb-link"][2]/text()').extract()))
        # print("--{0}\n{1}\n".format("select81", response.xpath('//a[@class="mz-breadcrumb-link"][3]/text()').extract()))
        # print("--{0}\n{1}\n".format("select9", response.xpath('//*[@id="page-content"]/div[1]/a[3]').extract()))
        # print("--{0}\n{1}\n".format("select10", response.xpath('//*[@id="page-content"]/div[1]/a[4]').extract()))
        # POI/faizan/
        # s1 = response.xpath('//*[@id="data-mz-preload-pagecontext"]/text()').extract()[0]
        # print(s1)
        # s2 = response.xpath('//*[@id="data-mz-preload-pagecontext"]').extract()[0]
        # print()
        # print(s2)
        # js1 = json.loads(s1)
        # print()
        # print()
        # print(js1)
        # print()
        # print()
        # print(js1['url'])
        # print("--{0}\n{1}\n".format("select11", response.xpath('//*[@id="data-mz-preload-pagecontext"]').extract()))
        # print("--{0}\n{1}\n".format("select12", response.xpath('/html/body/script[2]/text()').extract()))
        # print("--{0}\n{1}\n".format("select13", response.xpath('//*[@id="data-mz-preload-product"]/text()').extract()))
        # print("--{0}\n{1}\n".format("select15", response.xpath('//*[@id="data-mz-preload-product"][contains[@A,"product"]').extract()))
        # POI/faizan/
        # print("--{0}\n{1}\n".format("select15", response.xpath('//*[@id="data-mz-preload-product"]').extract()))
        # print("--{0}\n{1}\n".format("select15", response.xpath('//*[@id="data-mz-preload-product"]//[productFullDescription]').extract()))
        # print("--{0}\n{1}\n".format("select16", response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li/text()').extract()))
        # print("--{0}\n{1}\n".format("select16", response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[1]/text()').extract()))
        # print("--{0}\n{1}\n".format("select17", response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[2]').extract()))
        # print("--{0}\n{1}\n".format("select18", response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[3]').extract()))
        # print("--{0}\n{1}\n".format("select19", response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[4]').extract()))
        # print("--{0}\n{1}\n".format("select20", response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[6]').extract()))
        # print("--{0}\n{1}\n".format("select21", response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[8]').extract()))
        # print("--{0}\n{1}\n".format("select22", response.xpath('/html/head/meta[11]').extract()))
        # POI/faizan/
        # print("--{0}\n{1}\n".format("select220", response.xpath('/html/head/meta[11][@property="og:url"]/text()').extract()))
        # print("--{0}\n{1}\n".format("select220", response.xpath('/html/head/meta[11][1]/text()').extract()))
        # print("--{0}\n{1}\n".format("select23", response.xpath('/html/body/script[2]/text()').extract()))
        # print("--{0}\n{1}\n".format("select24", response.xpath('//*[@id="product-info-416904201"]').extract()))
        # print("--{0}\n{1}\n".format("select25", response.xpath('//*[@id="mouse-zoom"]').extract()))
        # print("--{0}\n{1}\n".format("select26", response.xpath('<div id="mouse-zoom" data-zoom-image="//cdn-tp4.mozu.'
        #                                                        'com/12106-m2/cms/files/416904201?maxWidth=1800&amp;'
        #                                                        'maxHeight=2160&amp;v=3" style="display: none;">'
        #                                                        '</div>').extract()))
        # print("--{0}\n{1}\n".format("select27", response.xpath('//*[@id="productimages"]/div[1]/div[2]/div[2]/img').extract()))
        # print("--{0}\n{1}\n".format("select27", response.xpath('//*[@id="productimages"]').extract()))
        # print("--{0}\n{1}\n".format("select270", response.xpath('//*[@id="productimages"]/div[1]').extract()))
        # print("--{0}\n{1}\n".format("select270", response.xpath('//*[@id="productimages"]//img').extract()))
        # print("--{0}\n{1}\n".format("select270", response.xpath('//*[@id="productimages"]').extract()))
        # print("--{0}\n{1}\n".format("select270", response.xpath('//*[@id="productimages"]').extract()))
        # print("--{0}\n{1}\n".format("select28", response.xpath('//*[@id="product-selection"]/div[3]/div/div/div/span[1]').extract()))
        # print("--{0}\n{1}\n".format("select29", response.xpath('//*[@id="product-selection"]/div[3]/div/div/div/span[2]').extract()))
        # print("--{0}\n{1}\n".format("select29", response.xpath('//*[@id="product-selection"]').extract()))
        # print("--{0}\n{1}\n".format("select30", response.xpath('//*[@id="data-mz-preload-product"]/text()').extract()))
        # print("--{0}\n{1}\n".format("select30", response.xpath('/html/body/script[2]/text()').extract()))
        # print("--{0}\n{1}\n".format("select31", response.xpath('//*[@id="product-selection"]/div[2]/div/span').extract()))
        # print("--{0}\n{1}\n".format("select32", response.xpath('//*[@id="product-selection"]/div[1]/div/div[1]').extract()))
        # print("--{0}\n{1}\n".format("select33", response.xpath('//*[@id="data-mz-preload-product"]/text()').extract()))
        # print("--{0}\n{1}\n".format("select34", response.xpath('//*[@id="product-selection"]/div[3]/div/div/div/span[1]').extract()))
        # print("--{0}\n{1}\n".format("select35", response.xpath('//*[@id="product-selection"]/div[3]/div/div/div/span[2]').extract()))
        # print("--{0}\n{1}\n".format("select36", response.xpath('//*[@id="data-mz-preload-product"]/text()').extract()))
        # print("--{0}\n{1}\n".format("select37", response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[5]').extract()))
        # print("--{0}\n{1}\n".format("select38", response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[7]').extract()))
        # print("--{0}\n{1}\n".format("select39", response.xpath('/html/body/script[2]/text()').extract()))
        # print("--{0}\n{1}\n".format("select40", response.xpath('//*[@id="data-mz-preload-pagecontext"]/text()').extract()))
        # print("--{0}\n{1}\n".format("select41", response.xpath('//*[@id="page-content"]/div[1]/a[2]').extract()))

        item['spider_name'] = self.name

        # item['retailer'] = response.xpath('//meta[@property="og:site_name"]')[0].extract()
        s1 = response.xpath('//meta[@property="og:site_name"]/@content')[0].extract()
        # print(s1)
        print("-1-")
        item['retailer'] = s1
        # print(response.xpath('//meta[@property="og:site_name"][@atr=content]')[0].extract())

        # item['currency'] = response.xpath('//*[@id="data-mz-preload-apicontext"]').extract()
        s1 = response.xpath('//*[@id="data-mz-preload-apicontext"]/text()').extract()[0]
        js1 = json.loads(s1)
        # print(s1)
        # print(js1)
        # print(js1['headers']['x-vol-currency'])
        print("-2-")
        item['currency'] = js1['headers']['x-vol-currency']

        item['market'] = "*TBD*"
        # print(s1)

        s1 = response.xpath('//a[@class="mz-breadcrumb-link"]/text()').extract()
        # print(s1)
        print("-3-")
        item['category'] = s1

        item['uuid'] = "*TBD*"
        # print(s1)

        s1 = response.xpath('//*[@id="page-content"]/div[2]/script[2]/text()').extract()
        s2 = response.xpath('//*[@id="page-content"]/div[2]/script[2]/text()').extract()[0]
        # print(s1)
        # print(s2)
        # print(s2.strip())
        # print(s2.split('='))
        # print(s2.strip().split('=')[1])
        # print(s2.find('='))
        # print(s2.find(';'))
        print("-4-")
        # print(s1[0])
        item['retailer_sku'] = s2.strip().split('=')[1]

        s1 = response.xpath('/html/body/script[2]/text()').extract()
        s2 = response.xpath('/html/body/script[2]/text()').extract()[0]
        # print(s1)
        # print(s2)
        # print(s2.strip())
        s3 = s2.replace("dataLayer.push(", "").replace(");", "").replace("\n", "")
        # print(s3)
        s3 = s3.strip()
        s3 = ' '.join(s3.split())

        # s3 = s3[0]
        # s3 = s3.strip().encode('utf-8', errors='ignore')
        # print(s3)
        js1 = json.dumps(s3).strip()
        js2 = json.loads(' '.join(js1.split()))
        # print(s3['ecommerce'])
        # print(js1)
        # print(js2)
        # print(dict(js2))
        # print(js2[5])
        # print(js2['ecommerce']['detail']['products']['price'])

        # js1 = json.loads(s2.replace("dataLayer.push(", "").replace(");", ""))
        # print(js1)
        # print(s2.split())
        # print(s2.strip().split())
        # print(s2.find('='))
        # print(s2.find(';'))
        i1 = (js2.find('price'))
        i2 = (js2.find("',", i1))
        # print(js2[i1+len("'price':"):i2])
        print("-5-")
        item['price'] = js2[i1+len("'price':'"):i2]

        s1 = response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li/text()').extract()
        s2 = response.xpath('//*[@id="data-mz-preload-product"]/text()').extract()[0]
        # item['description'].append(response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li/text()').extract())
        js2 = json.loads(s2)
        # print(s1)
        # print(s2)
        # print(js2)
        # print(js2['content']['productFullDescription'])
        # print(s1[0])
        # print(s1[1])
        # print(s1[2])
        # print(s1[3])
        # print(s1[5])
        # print(s1[7])
        print("-6-")
        # item['description'] = [js2['content']['productFullDescription'], s1]
        # item['description'] = []
        # item['description'].append(js2['content']['productFullDescription'])
        # item['description'].append(s1)
        item['description'] = s1
        # item['description'].insert(0, js2['content']['productFullDescription'])

        # print(item['description'])

        s1 = response.xpath('/html/head/meta[11]/@content').extract()[0]
        # print(s1)
        print("-7-")
        item['url_original'] = s1

        s2 = response.xpath('/html/body/script[2]/text()').extract()[0]
        # print(s2)
        s3 = s2.replace("dataLayer.push(", "").replace(");", "").replace("\n", "")
        s3 = s3.strip()
        s3 = ' '.join(s3.split())
        js1 = json.dumps(s3).strip()
        js2 = json.loads(' '.join(js1.split()))
        # print(js2)
        i1 = (js2.find('brand'))
        i2 = (js2.find("',", i1))
        print("-8-")
        # print(js2[i1+len("'brand':'"):i2])
        item['brand'] = js2[i1+len("'brand':'"):i2]

        # s1 = response.xpath('//*[@id="productimages"]//img').extract()
        # s2 = response.xpath('//*[@id="productimages"]//img//@src').extract()[0]
        # s2 = response.xpath('//*[@id="productimages"]//img//@src').extract()
        s2 = response.xpath('//*[@class="mz-productimages-thumbs"]//img//@src').extract()
        # s3 = response.xpath('//*[@id="productimages"]//img//@data-src').extract()[0]
        # print(s1)
        # print(len(s1))
        # print("--")
        # print(s2)
        # print(s3)
        # print("--")
        # print(s1[0])
        # print("--")
        # print(s1[1])
        print("-9-")
        # item['image_urls'] = ['http:'+s2, 'http:'+s3]
        # item['image_urls'] = ['http:'+s2[0], 'http:'+s3[1]]
        item['image_urls'] = s2

        s1 = response.xpath('//*[@id="product-selection"]').extract()[0]
        # s1 = response.xpath('//*[@id="product-selection"]/div[3]/div/div/div/span[1]').extract()
        # s2 = response.xpath('//*[@id="product-selection"]/[@class="mz-productoptions-sizebox"]').extract()
        # s2 = response.xpath('//*[@id="product-selection"]/@class').extract()
        # s2 = response.xpath('//*[@id="product-selection"]//@itemprop').extract()
        # s2 = response.xpath('//*[@id="product-selection"]//@class="mz-productoptions-sizebox"').extract()
        s2 = response.xpath('//*[@id="product-selection"]//span').extract()
        s3 = response.xpath('//*[@id="product-selection"]//span/text()').extract()
        s4 = response.xpath('//*[@id="product-selection"]//span//@data-value').extract()
        s5 = response.xpath('//*[@id="data-mz-preload-apicontext"]/text()').extract()[0]
        s6 = response.xpath('//*[@id="data-mz-preload-product"]/text()').extract()[0]
        # s7 = response.xpath('//*[@id="product-selection"]/div[2]/div/span').extract()
        s7 = response.xpath('//*[@id="page-content"]/div[2]/div[1]/div[2]/div[3]/div/span/text()').extract()[0]

        # print(s1)
        # print("--")
        # s2 = s1.strip()
        s1 = s1.strip()
        s1 = ' '.join(s1.split())
        # print(s1)
        # print("\n-111-\n")
        # s2 = s2.strip()
        # s2 = ' '.join(s2.split())
        # print(s2)
        # print("--")
        print(s3)
        # print("--")
        print(s4)
        # print(len(s4))
        # print("--")
        # print(s5)
        # print("--")
        # print(s6)
        # print("--")
        # print(s7)
        # print("--")
        js5 = json.loads(s5)
        # js6 = json.loads(s6)
        # print(s1)
        # print(js1)
        # print(js5)
        # print(js5['headers']['x-vol-currency'])
        # print(item['price'])
        # print(s5)
        print("-10-")
        # item['skus'] = {s4[0]: {js5['headers']['x-vol-currency'], s7, item['price'], s3}, s4[1]: {js5['headers']['x-vol-currency'], s7, item['price'], s3}}
        # item['skus'] = {s4[0]: {s7}, s4[1]: {s7}}
        # item['skus'] = {}
        # item['skus'][s4[0]] = {}
        # item['skus'][s4[1]] = {}
        # item['skus'][s4[0]] = {'currency': js5['headers']['x-vol-currency'], 'colour': s7, 'price': item['price'],
        #                        'size': s3[0]}
        # item['skus'][s4[1]] = {'currency': js5['headers']['x-vol-currency'], 'colour': s7, 'price': item['price'],
        #                        'size': s3[1]}
        item['skus'] = {}
        for i in range(len(s4)):
            # print(i)
            # print(js5['headers']['x-vol-currency'])
            # print(s7)
            # print(item['price'])
            # print(s3[i])
            # print(s4[i])
            item['skus'][s4[i]] = {}
            item['skus'][s4[i]] = {'currency': js5['headers']['x-vol-currency'], 'colour': s7, 'price': item['price'],
                                   'size': s3[i]}

        # {
        # currency = scrapy.Field()
        # colour = scrapy.Field()
        # price = scrapy.Field()
        # size = scrapy.Field()
        # }

        #POI/faizan/LEAVE 'care'/ s1 = response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[5]/text()').extract()[0]
        # s2 = response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li[7]/text()').extract()[0]
        # # print(s1)
        # # print("--")
        # # print(s2)
        print("-11-")
        # item['care'] = [s1, s2]
        item['care'] = "*Embedded in 'Description'*"

        s2 = response.xpath('/html/body/script[2]/text()').extract()[0]
        # print(s2)
        # print("--")
        s3 = s2.replace("dataLayer.push(", "").replace(");", "").replace("\n", "")
        s3 = s3.strip()
        s3 = ' '.join(s3.split())
        js1 = json.dumps(s3).strip()
        js2 = json.loads(' '.join(js1.split()))
        # print(js2)
        i1 = (js2.find('name'))
        i2 = (js2.find("',", i1))
        print("-12-")
        # print(js2[i1+len("'name':'"):i2])
        item['name'] = js2[i1+len("'name':'"):i2]

        s1 = response.xpath('//*[@id="data-mz-preload-pagecontext"]/text()').extract()[0]
        # print(s1)
        # print("--")
        js1 = json.loads(s1)
        # print(js1)
        # print(js1['url'])
        print("-13-")
        item['url'] = js1['url']

        s1 = response.xpath('//*[@id="page-content"]/div[1]/a[2]/text()').extract()[0]
        # print(s1)
        print("-14-")
        item['gender'] = s1

        # print('\n******************************************************\n')
        # print("item['spider_name']: {}".format(item['spider_name']))
        # print("item['retailer']: {}".format(item['retailer']))
        # print("item['currency']: {}".format(item['currency']))
        # print("item['market']: {}".format(item['market']))
        # print("item['category']: {}".format(item['category']))
        # print("item['uuid']: {}".format(item['uuid']))
        # print("item['retailer_sku']: {}".format(item['retailer_sku']))
        # print("item['price']: {}".format(item['price']))
        # print("item['description']: {}".format(item['description']))
        # print("item['url_original']: {}".format(item['url_original']))
        # print("item['brand']: {}".format(item['brand']))
        # print("item['image_urls']: {}".format(item['image_urls']))
        # print("item['skus']: {}".format(item['skus']))
        # print("item['care']: {}".format(item['care']))
        # print("item['name']: {}".format(item['name']))
        # print("item['url']: {}".format(item['url']))
        # print("item['gender']: {}".format(item['gender']))

        # return item
        yield item
        # yield {
        #     self.log("\n**********Crawling\n")
        #     print("\n**********Crawling\n")
        #     item.field1 = response.xpath('//title')
        #     item.field1 = 'ZILCH'
        #     # item.field2 = "STH"
        #     # item.field3 = "STHSTH"
        #     # item.field4 = "STHSTHSTH"
        # }
        # yield item


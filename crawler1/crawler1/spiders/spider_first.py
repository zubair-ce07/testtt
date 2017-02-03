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

    rules = (Rule(LinkExtractor(restrict_xpaths=['//*[@id="page-wrapper"]/header/div/nav',
                                                 '//*[@class="mz-pagenumbers"]'])),
             Rule(LinkExtractor(restrict_xpaths='//*[@class="mz-productlist-item"]'),
                  callback='parse_item'))

    def parse_item(self, response):
        item = Crawler1Item()
        print('\n***************************** GETTING URL:\n%s\n*************************************\n' % response.url)

        item['spider_name'] = self.name

        s1 = response.xpath('//meta[@property="og:site_name"]/@content')[0].extract()
        # print("-1-")
        item['retailer'] = s1

        s1 = response.xpath('//*[@id="data-mz-preload-apicontext"]/text()').extract()[0]
        js1 = json.loads(s1)
        # print("-2-")
        item['currency'] = js1['headers']['x-vol-currency']

        item['market'] = "*TBD*"

        s1 = response.xpath('//a[@class="mz-breadcrumb-link"]/text()').extract()
        # print("-3-")
        item['category'] = s1

        item['uuid'] = "*TBD*"

        s2 = response.xpath('//*[@id="page-content"]/div[2]/script[2]/text()').extract()[0]
        # print("-4-")
        item['retailer_sku'] = s2.strip().split('=')[1]

        s2 = response.xpath('/html/body/script[2]/text()').extract()[0]
        s3 = s2.replace("dataLayer.push(", "").replace(");", "").replace("\n", "")
        s3 = s3.strip()
        s3 = ' '.join(s3.split())

        js1 = json.dumps(s3).strip()
        js2 = json.loads(' '.join(js1.split()))
        i1 = (js2.find('price'))
        i2 = (js2.find("',", i1))
        # print("-5-")
        item['price'] = js2[i1+len("'price':'"):i2]

        s1 = response.xpath('//*[@id="product-detail"]/div[2]/div[3]/ul/li/text()').extract()
        s2 = response.xpath('//*[@id="data-mz-preload-product"]/text()').extract()[0]
        # print("-6-")
        item['description'] = s1

        s1 = response.xpath('/html/head/meta[11]/@content').extract()[0]
        # print("-7-")
        item['url_original'] = s1

        s2 = response.xpath('/html/body/script[2]/text()').extract()[0]
        s3 = s2.replace("dataLayer.push(", "").replace(");", "").replace("\n", "")
        s3 = s3.strip()
        s3 = ' '.join(s3.split())
        js1 = json.dumps(s3).strip()
        js2 = json.loads(' '.join(js1.split()))
        i1 = (js2.find('brand'))
        i2 = (js2.find("',", i1))
        # print("-8-")
        item['brand'] = js2[i1+len("'brand':'"):i2]

        s2 = response.xpath('//*[@class="mz-productimages-thumbs"]//img//@src').extract()
        # print("-9-")
        item['image_urls'] = s2

        s1 = response.xpath('//*[@id="product-selection"]').extract()[0]
        s2 = response.xpath('//*[@id="product-selection"]//span').extract()
        s3 = response.xpath('//*[@id="product-selection"]//span/text()').extract()
        s4 = response.xpath('//*[@id="product-selection"]//span//@data-value').extract()
        s5 = response.xpath('//*[@id="data-mz-preload-apicontext"]/text()').extract()[0]
        s6 = response.xpath('//*[@id="data-mz-preload-product"]/text()').extract()[0]
        s7 = response.xpath('//*[@id="page-content"]/div[2]/div[1]/div[2]/div[3]/div/span/text()').extract()[0]

        s1 = s1.strip()
        s1 = ' '.join(s1.split())
        # print(s3)
        # print(s4)
        js5 = json.loads(s5)
        # print("-10-")
        item['skus'] = {}
        for i in range(len(s4)):
            item['skus'][s4[i]] = {}
            item['skus'][s4[i]] = {'currency': js5['headers']['x-vol-currency'], 'colour': s7, 'price': item['price'],
                                   'size': s3[i]}

        # print("-11-")
        item['care'] = "*Embedded in 'Description'*"

        s2 = response.xpath('/html/body/script[2]/text()').extract()[0]
        s3 = s2.replace("dataLayer.push(", "").replace(");", "").replace("\n", "")
        s3 = s3.strip()
        s3 = ' '.join(s3.split())
        js1 = json.dumps(s3).strip()
        js2 = json.loads(' '.join(js1.split()))
        # print(js2)
        i1 = (js2.find('name'))
        i2 = (js2.find("',", i1))
        # print("-12-")
        item['name'] = js2[i1+len("'name':'"):i2]

        s1 = response.xpath('//*[@id="data-mz-preload-pagecontext"]/text()').extract()[0]
        js1 = json.loads(s1)
        # print("-13-")
        item['url'] = js1['url']

        s1 = response.xpath('//*[@id="page-content"]/div[1]/a[2]/text()').extract()[0]
        # print("-14-")
        item['gender'] = s1

        print("-Done-")
        yield item


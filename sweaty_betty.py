import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
import re
import json

class SweatyBettySpider(CrawlSpider):
    name = "sweaty_betty"
    allowed_domains = ['sweatybetty.com']
    start_urls = ['http://www.sweatybetty.com/']

    rules = (
        Rule(LinkExtractor(restrict_css=('div.megamenu'))),
        Rule(LinkExtractor(restrict_css=('a.next'))),
        Rule(LinkExtractor(restrict_css=('div.productlistcell-inner div.prodlink')),callback='detail_parse'),
    )

    def detail_parse(self, response):
        title = response.css('meta[property="og:title"]::attr(content)').extract()
        price =  response.css('meta[property="og:price:amount"]::attr(content)').extract_first()
        currency = response.css('meta[property="og:price:currency"]::attr(content)').extract_first()
        retailor = response.css('meta[property="og:site_name"]::attr(content)').extract_first()
        description = response.css('meta[property="og:description"]::attr(content)').extract_first()
        org_url = response.css('meta[property="og:url"]::attr(content)').extract_first()
        category = response.css('head script::text').re('"breadcrumb"\s:\s(.+]),"environment.*')
        lang = response.css('head script::text').re('"language":\s"(.+)"},"pro.*')
        item_data = response.css('head script::text').re('"googlevariants"\s:(.*])')[0]
        items = json.loads(item_data)
        img_urls_data = data = response.css('div.product-tabs~script::text').extract()[0]
        img_urls =  re.findall('"(http.*\.jpg)"',img_urls_data)
        sizes_data = response.css('div.variant-holder script::text').extract_first()
        sizes_info_data = re.findall('=new\sseldata\(new\sArray(.*)\);v', sizes_data)
        sizes_info = sizes_info_data[0].split(");")
        skus = self.make_skus(sizes_info, items)
        yield {
            'spider-name': SweatyBettySpider.__name__,
            'retailor': retailor,
            'currency':currency,
            'price':price,
            'description':description,
            'language': lang,
            'category': category,
            'org_url':org_url,
            'title': title,
            'image_urls': img_urls,
            'skus':skus,
            'brand': "SweatyBetty",
            "crawler_start_time": self.crawler.stats.get_value('start_time'),
        }

    def make_skus(self ,sizes_info, items):
        sizes = {}
        for size in sizes_info:
            size = size.replace("'","")
            v = size.split(',')
            size_s = v[1].split(')')[0]
            sku = v[4]
            if not "Select" in size_s:
                sizes[sku] = size_s
        skus = {}
        for item in items:
            size = sizes[item['sku']]
            size_data = size.split('-')
            if len(size_data) == 2:
                item['status'] = size_data[1]
            key = item["id"]+"_"+size_data[0]
            skus[key] = item
        return skus
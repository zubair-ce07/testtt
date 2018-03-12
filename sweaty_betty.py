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
        Rule(LinkExtractor(restrict_css=(['div.megamenu', 'a.next']))),
        Rule(LinkExtractor(restrict_css=('.productlistcell-inner .prodlink')), callback='parse_detail'),
    )

    def parse_detail(self, response):
        items = self.get_items(response)
        sizes_info = self.get_sizes_info(response)
        skus = self.make_skus(sizes_info, items)
        yield {
            'spider-name': SweatyBettySpider.__name__,
            'retailor': self.get_retailor(response),
            'currency': self.get_currency(response),
            'price': self.get_price(response),
            'description': self.get_description(response),
            'language': self.get_lang(response),
            'category': self.get_category(response),
            'org_url': self.get_org_url(response),
            'title': self.get_title(response),
            'image_urls': self.get_img_urls(response),
            'skus': skus,
            'brand': "SweatyBetty",
            "crawler_start_time": self.crawler.stats.get_value('start_time'),
        }

    def make_skus(self, sizes_info, items):
        sizes = {}
        for size in sizes_info:
            size = size.replace("'", "")
            v = size.split(',')
            size_s = v[1].split(')')[0]
            sku = v[4]
            if "Select" not in size_s:
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

    def get_title(self, response):
        return response.css('meta[property="og:title"]::attr(content)').extract()

    def get_price(self, response):
        return response.css('meta[property="og:price:amount"]::attr(content)').extract_first()

    def get_currency(self, response):
        return response.css('meta[property="og:price:currency"]::attr(content)').extract_first()

    def get_retailor(self, response):
        return response.css('meta[property="og:site_name"]::attr(content)').extract_first()

    def get_description(self, response):
        return response.css('meta[property="og:description"]::attr(content)').extract_first()

    def get_org_url(self, response):
        return response.css('meta[property="og:url"]::attr(content)').extract_first()

    def get_category(self, response):
        return response.css('head script::text').re('"breadcrumb"\s:\s(.+]),"environment.*')

    def get_lang(self, response):
        return response.css('head script::text').re('"language":\s"(.+)"},"pro.*')

    def get_items(self, response):
        item_data = response.css('head script::text').re('"googlevariants"\s:(.*])')[0]
        return json.loads(item_data)

    def get_img_urls(self, response):
        img_urls_data = response.css('.product-tabs~script::text').extract()[0]
        return re.findall('"(http.*\.jpg)"', img_urls_data)

    def get_sizes_info(self, response):
        sizes_data = response.css('.variant-holder script::text').extract_first()
        sizes_info_data = re.findall('=new\sseldata\(new\sArray(.*)\);v', sizes_data)
        return sizes_info_data[0].split(");")


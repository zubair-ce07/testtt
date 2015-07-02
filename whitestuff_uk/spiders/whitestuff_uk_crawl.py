from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from whitestuff_uk.items import WhitestuffUkItem
import re
import json
from scrapy.http import Request


class WhiteStuff(CrawlSpider):
    name = 'whitestuff_uk_crawl'
    allowed_domains = ['whitestuff.com']
    start_urls = ['http://www.whitestuff.com/womens/']
    item_response = []
    rules = [
        Rule(
            SgmlLinkExtractor(restrict_xpaths='.//*[@id="leftNAVIGATIONDepartment"]/ul//a'),
            callback="parse_url", follow=True
        )
    ]

    def parse_url(self, response):
        cat_type = response.url.split('/')[-2]
        cat = response.xpath('//script[contains(text(),"category")]/text()').extract()[0]
        cat_tree = re.search(r'/(.*)/', cat).group(1)
        cat_no = re.search(r'"category", "(.*)"', cat).group(1)
        yield (
            Request(
                'http://esp.locayta.com/zones-js.aspx?version=2.16.2&'
                'siteId=f98ab651-c74b-42a5-9bc8-c45c0029e97f'
                '&UID=c97f7319-822d-5d00-19d0-10f694ce492e&'
                'SID=95d04c2f-bf69-0a13-bad3-fb6f97177b0e&referrer='
                '&sitereferrer=&pageurl=http%3A%2F%2Fwww.whitestuff.com'
                '%2Fwomens%2F'+cat_type+'s%2F&zone0='
                'category&facetmode=html&mergehash=false&'
                'config_categorytree=%2F'+cat_tree+'%2F&config_category='+
                cat_no+'&config_fsm_sid=95d04c2f-bf69-0a13-bad3-fb6f97177b0e'
                '&config_fsm_returnuser=1&config_fsm_currentvisit='
                '28%2F04%2F2015&config_fsm_visitcount=2&'
                'config_fsm_lastvisit=27%2F04%2F2015',
                dont_filter=True, callback=self.parse_items
            )
        )

    def parse_items(self, response):
        res = re.search(r'"html":(.*),"filterHtml"', response.body).group(1)
        items = Selector(text=res).xpath(
            './/*[@class=\'\\\"catHOLDER\\\"\']//h3//@href'
        ).extract()
        for item in items:
            item = item.strip("\\\"")
            yield Request(item, callback=self.parse_item_details)

    def parse_item_details(self, response):
        item = WhitestuffUkItem()
        item['category'] = self.get_category(response)
        item['care'] = self.get_care(response)
        item['gender'] = self.get_gender(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['description'] = self.get_description(response)
        item_code = item['description'][-1].split(' ')[1]
        item['image_urls'] = self.get_image_urls(response, item_code)
        item['skus'] = self.get_sku(response, item_code)
        yield item

    def get_category(self, res):
        categories = res.xpath(
            './/*[@id="crumb"]//a//text()'
        ).extract()
        return categories

    def get_retailer_sku(self, res):
        retailer_sku = res.xpath(
            './/*[@id="accordion"]//span/text()'
        ).extract()[0]
        return re.findall(r'(\d+[\.]?\d*)', retailer_sku)

    def get_description(self, res):
        description = res.xpath(
            './/*[@id="accordion"]/div[1]//text()'
        ).extract()
        return description

    def get_image_urls(self, res, item_code):
        variant = res.xpath(
            './/*[@id="prodDETAILS"]/script[1]'
        ).extract()[0].replace('\n', '')
        image_names = re.search(r'var imgItems = (.*)//REM', variant).group(1)
        base_url = re.search(r'large:.*prefix":"(.*)"}', variant).group(1)
        image_data = json.loads(image_names)
        image_urls = []
        image_data = image_data[item_code].strip('#').split('#')
        for data in image_data:
            image_urls.append(base_url+data)
        return image_urls

    def get_care(self, res):
        care = res.xpath(
            './/*[@id="accordion"]/div[1]//text()[3]'
        ).extract()
        return care

    def get_gender(self, res):
        gender = res.xpath(
            './/*[@id="crumb"]/span[1]//text()'
        ).extract()[0]
        return gender

    def get_sku(self, res, item_code):
        variant = res.xpath(
            './/*[@id="prodDETAILS"]/script[1]'
        ).extract()[0].replace('\n', '')
        sku_details = re.search(r'var variants = (.*)var imgItems', variant).group(1)
        sku_data = json.loads(sku_details)
        skus = {}
        for data in sku_data:
            if item_code == sku_data[data]['pf_id']:
                temp = {}
                temp['color'] = sku_data[data]['option1']
                temp['currency'] = 'GBP'
                temp['price'] = sku_data[data]['line_price']
                if sku_data[data]['lead_text'] == 'Out of stock':
                    temp['out_of_stock'] = True
                else:
                    temp['out_of_stock'] = False
                temp['size'] = sku_data[data]['option2']
                skus[data] = temp
        return skus


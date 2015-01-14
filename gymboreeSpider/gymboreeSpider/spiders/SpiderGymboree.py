from gymboree.items import GymboreeItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re


def last_link_break(value):
    if ('javascript:Detail_Loader' in value):
        match = re.search("javascript:Detail_Loader\('(.*?)', '(.*?)'", value)
        value = match.group(2)
    return value


def link_break(value):
    temp_link = value.split('&bmUID')
    value = temp_link[0]
    return value


class SpiderGymboree(CrawlSpider):
    name = "Gmyboreespider"
    allowed_domains = ["gymboree.com"]
    start_urls = [
        "http://www.gymboree.com/"
    ]

    first_page = '//ul/li[1]/a[contains(@href,"department") and contains(@href,"ASSORTMENT")]'
    cat_page = '//*[@id="left-menu"]/ul[1]/li[1]/a[not(contains(@href,"#"))]'
    items_page = './/div[@class="product-list-data"]/div[position() <4]//*[@class="collection-pricing"]/a'
    item_detail_page = '//body'
    rules = [
        Rule(SgmlLinkExtractor(deny=[r'Eprd_id'], restrict_xpaths=first_page, process_value=link_break), follow=True),
        Rule(SgmlLinkExtractor(deny=[r'Eprd_id'], restrict_xpaths=cat_page, process_value=link_break), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=items_page, process_value=link_break), follow=True),
        Rule(SgmlLinkExtractor(deny=[r'index'], restrict_xpaths=item_detail_page, tags=('body'), attrs='onload',
                               process_value=last_link_break), callback='parse_get_detail')
        # Rules for crawling
    ]
    product_response = ''

    def get_title(self):
        title = self.product_response.xpath('.//head/@name').extract()[0]
        return title

    def get_skus(self, res):
        skus = {}
        color = self.get_color(res)
        for rec in res.xpath('.//sku'):
            arr = {}
            id = rec.xpath('./@id').extract()
            arr['size'] = rec.xpath('./@title').extract()[0]
            arr['color'] = color
            arr['currency'] = 'USD'
            reg_price = rec.xpath('./@reg-price').extract()
            start = reg_price[0].find('$')
            end = reg_price[0].find('<', start + 1)
            arr['previous_price'] = reg_price[0][start:end]
            sale_price = rec.xpath('./@sale-price').extract()
            sale_start = sale_price[0].find('$')
            sale_end = sale_price[0].find('<', sale_start + 1)
            arr['price'] = sale_price[0][sale_start:sale_end]
            skus[id[0]] = arr
        return skus

    def get_link(self, res):
        link = res.xpath('./@readReviewsURL').extract()[0]
        newlink = link.replace('#readReviews', '')
        m = newlink.find("&bmUID")
        newlink = newlink[:m]
        return newlink


    def get_retailer_sk(self, res):
        retailer_sk = res.xpath('./@code').extract()[0]
        return retailer_sk

    def get_color(self, res):
        color = res.xpath('./@title').extract()[0]
        return color


    def get_images(self, res):
        image = res.xpath('./@image').extract()
        return image


    def parse_get_detail(self, response):
        print response
        self.product_response = response
        item = GymboreeItem()
        for res in self.product_response.xpath('.//silhouette//product'):
            item['retailer'] = 'gymboree'
            item['currency'] = 'USD'
            item['spy_name'] = self.name
            item['link'] = self.get_link(res)
            item['title'] = self.get_title()
            item['skus'] = self.get_skus(res)
            item['retailer_sk'] = self.get_retailer_sk(res)
            item['color'] = self.get_color(res)
            item['image_urls'] = self.get_images(res)
            yield item



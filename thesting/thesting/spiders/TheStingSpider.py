import json
from scrapy.http.request import Request
from scrapy.link import Link
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from thesting.items import TheStingItem


class ProductLinkExtractor(LinkExtractor):
    def extract_links(self, response):
        script = response.css('div.listings > script')
        links = script.re('\"urlProductDetailPage\":\s*\"(.*)\"')
        return [Link(url='http://www.thesting.com/'+link) for link in links]


class TheStingSpider(CrawlSpider):
    name = "thesting"
    start_urls = [
        'http://www.thesting.com/en-gb/'
    ]

    allowed_domains =[
        'www.thesting.com'
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=('.topnav-container', 'ul.pages'), ), callback='parse_list'),
    ]

    def parse_list(self, response):
        gender = response.css('script:contains("pageAffinity")')\
            .re_first('\"pageAffinity\": \"(.+)\"')

        for link in ProductLinkExtractor().extract_links(response):
            yield Request(url=link.url, callback=self.parse_item, meta={'gender': gender})

    def parse_item(self, response):
        script = response.css('div#overlay-mask + script')
        item = TheStingItem()
        item['retailer_sku'] = script.re_first('(?<="genericCode":)\s*\"(.*)\"')
        item['url'] = response.url
        item['name'] = script.re_first('(?<="productName":)\s*\"(.*)\"')
        item['category'] = script.re_first('(?<="productCategory":)\s*\"(.*)\"')
        item['brand'] = script.re_first('(?<="brandName":)\s\"(.*)\"')
        item['description'] = response.css('meta[name="description"]::attr(content)').extract_first()
        item['currency'] = self.product_currency(script)
        item['gender'] = response.meta['gender']
        item['image_urls'] = self.get_image_urls(response)
        item['spider_name'] = self.name
        item['retailer'] = 'thesting'
        item['price'] = self.product_price(script)
        item['url_original'] = response.url
        color_info = self.get_color_info(response)
        item['skus'] = {}
        return self.get_skus(item, color_info)

    def get_image_urls(self, response):
        script = response.css('div#overlay-mask + script')
        str_json = script.re_first('(?<="listImages":)[\s"]*(\[[^\]]*\])')
        array = json.loads(str_json)
        return [obj['urlPresetZoom'] for obj in array]

    def get_skus(self, item, color_info):
        if color_info:
            name, url = color_info.pop()
            return Request(url='http://www.thesting.com/'+url,
                           callback=self.parse_color_sku,
                           meta = {
                               'item': item,
                               'color_name': name,
                               'color_info': color_info,
                           })
        return item

    def parse_color_sku(self, response):
        item = response.meta['item']
        color_info = response.meta['color_info']

        script = response.css('div#overlay-mask + script')
        color = response.meta['color_name']
        price = self.product_price(script)
        currency = self.product_currency(script)

        sizes = self.product_sizes(response)
        for size in sizes:
            variantCode = size[0]
            item['skus'][variantCode] = {
                'color': color,
                'size': size[1],
                'price': price,
                'currency': currency,
            }

        return self.get_skus(item, color_info)

    def get_color_info(self, response):
        script_elem = response.css('div#overlay-mask + script::text')
        allColors_raw = script_elem.re_first('(?<="allColors":)\s*(\[[^\]]*\])')
        allColors_json = json.loads(allColors_raw)
        return [(color_obj['name'], color_obj['productPageColorUrl'])
                for color_obj in allColors_json]

    def product_price(self, script):
        return int(script.re_first('(?<="price":)[\s"]*([\d\.]*)').replace('.',''))

    def product_currency(self, script):
        return script.re_first('(?<="currency":)[\s"]*([^:ascii:])')

    def product_sizes(self, response):
        script_elem = response.css('div#overlay-mask + script::text')
        availableSizes_raw = script_elem.re_first('(?<="availableSizes":)\s*(\[[^\]]*\])')
        availableSizes_json = json.loads(availableSizes_raw)
        return [(size['variantCode'], size['name'])
                for size in availableSizes_json
                if size['available']]

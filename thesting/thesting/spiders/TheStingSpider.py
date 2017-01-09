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
        return [Link(url='http://www.thesting.com/' + link) for link in links]


class TheStingSpider(CrawlSpider):
    name = "thesting"
    start_urls = [
        'http://www.thesting.com/en-gb/'
    ]

    allowed_domains = [
        'www.thesting.com'
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=('.topnav-container', 'ul.pages'), ), callback='parse_list'),
    ]

    def parse_list(self, response):
        gender = response.css('script:contains("pageAffinity")') \
            .re_first('\"pageAffinity\": \"(.+)\"')

        for link in ProductLinkExtractor().extract_links(response):
            yield Request(url=link.url, callback=self.parse_item, meta={'gender': gender})

    def parse_item(self, response):
        script = response.css('div#overlay-mask + script')
        item = TheStingItem()
        item['retailer_sku'] = script.re_first('(?<="genericCode":)\s*\"(.*)\"')
        item['url'] = response.url
        item['name'] = script.re_first('(?<="productName":)\s*\"(.*)\"')
        item['category'] = script.re('(?<="productCategory":)\s*\"(.*)\"')
        item['brand'] = script.re_first('(?<="brandName":)\s\"(.*)\"')
        item['description'] = response.css('meta[name="description"]::attr(content)').extract_first()
        item['currency'] = self.product_currency(script)
        item['gender'] = self.product_gender(response)
        item['image_urls'] = self.get_image_urls(response)
        item['spider_name'] = self.name
        item['retailer'] = 'thesting'
        item['price'] = self.product_price(response)
        item['url_original'] = response.url
        item['care'] = self.product_care(response)
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
            return Request(url='http://www.thesting.com/' + url,
                           callback=self.parse_color_sku,
                           meta={
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
        price = self.product_price(response)
        currency = self.product_currency(script)
        sizes = self.product_sizes(response)
        for size in sizes:
            variant_code = size[0]
            item['skus'][variant_code] = {
                'color': color,
                'size': size[1],
                'price': price,
                'currency': currency,
            }

        return self.get_skus(item, color_info)

    def get_color_info(self, response):
        script_elem = response.css('div#overlay-mask + script::text')
        all_colors_raw = script_elem.re_first('(?<="allColors":)\s*(\[[^\]]*\])')
        all_colors_json = json.loads(all_colors_raw)
        return [(color_obj['name'], color_obj['productPageColorUrl'])
                for color_obj in all_colors_json]

    def product_price(self, response):
        script = response.css('script:contains("saleStatus")::text')
        sale_status = int(script.re_first('(?<=\"saleStatus\":) (\d+)'))
        if sale_status:
            return int(script.re_first('(?<="fromPrice":)[\s"]*([\d\.]*)').replace('.', ''))
        else:
            return int(script.re_first('(?<="price":)[\s"]*([\d\.]*)').replace('.', ''))

    def product_currency(self, script):
        return script.re_first('(?<="currency":)[\s"]*([^:ascii:])')

    def product_care(self, response):
        script= response.css('div#overlay-mask + script::text')
        care_raw = script.re_first('(?<="productFabrics":)\s*(\[[^\]]*\])')
        care_json = json.loads(care_raw)
        return [care['value'] for care in care_json]

    def product_gender(self, response):
        script = response.css('script:contains("pageAffinity")')
        affinity = script.re_first('(?<="pageAffinity":) "(.*)"')
        if affinity.lower() == 'male':
            return 'men'
        elif affinity.lower() == 'female':
            return 'women'

    def product_sizes(self, response):
        script_elem = response.css('div#overlay-mask + script::text')
        available_sizes_raw = script_elem.re_first('(?<="availableSizes":)\s*(\[[^\]]*\])')
        available_sizes_json = json.loads(available_sizes_raw)
        return [(size['variantCode'], size['name'])
                for size in available_sizes_json
                if size['available']]

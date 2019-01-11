import json

from scrapy import Spider, Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from item_structure import Item
from helpers import extract_price_details, extract_gender, item_or_request


class ProductParser(Spider):
    def __init__(self):
        self.seen_ids = set()

    def parse(self, response):
        item = Item()
        retailer_sku = self.extract_product_id(response)

        if not self.is_new_item(retailer_sku):
            return

        item['retailer_sku'] = retailer_sku
        item['name'] = self.extract_name(response)
        item['gender'] = self.extract_gender(response)
        item['spider_name'] = 'vipshop'
        item['brand'] = self.extract_brand(response)
        item['care'] = self.extract_care(response)
        item['url'] = response.url
        item['description'] = self.extract_description(response)
        item['market'] = self.extract_market()
        item['retailer'] = self.extract_retailer()
        item['trail'] = response.meta.get('trail', [])
        item['image_urls'] = self.extract_image_urls(response)
        item['category'] = self.extract_categories(response)
        item['skus'] = self.extract_skus(response)
        item['meta'] = {'requests': self.extract_requests(response)}

        return item_or_request(item)

    def parse_colour_item(self, response):
        item = response.meta.get('item', {})
        item['skus'].update(self.extract_skus(response))
        item['image_urls'] += self.extract_image_urls(response)
        return item_or_request(item)

    def parse_stock_item(self, response):
        item = response.meta.get('item', {})
        stock_details = response.xpath('//text()').re_first('stock_detail\({"items":(.*])')
        out_of_stock = [std['id'] for std in json.loads(stock_details) if std['stock'] == 0]

        for sku in item['skus']:
            if int(item['skus'][sku]['id']) in out_of_stock:
                item['skus'][sku].pop('id')
                item['skus'][sku]['out_of_stock'] = True

        return item_or_request(item)


    def extract_requests(self, response):
        prod_id = self.extract_product_id(response)
        url = f"https://stock.vip.com/detail/?callback=stock_detail&merchandiseId={prod_id}&is_old=0&areaId=104104101"
        requests = self.extract_colour_requests(response)
        requests.append(Request(url, callback=self.parse_stock_item))
        return requests

    def extract_colour_requests(self, response):
        css = '.color-list a:not([class="J-colorItem color-selected"])::attr(href)'
        urls = response.css(css).extract()
        return [Request(url=response.urljoin(url), callback=self.parse_colour_item) for url in urls]

    def is_new_item(self, product):
        if product and product not in self.seen_ids:
            self.seen_ids.add(product)
            return True

        return False

    def extract_product_id(self, response):
        pattern = 'leftSideCoupon.*?productId":"(.*?)"'
        return response.xpath("//script/text()").re_first(pattern)

    def extract_description(self, response):
        description = response.css('.goods-description-title::text').extract_first()
        return [des.strip() for des in description.split('.') if des.strip()] if description else []

    def extract_name(self, response):
        return response.css('.pib-title-detail::text').extract_first()

    def extract_care(self, response):
        raw_care = response.css('.dc-table.fst td::text').extract()
        return [care.strip() for care in raw_care if '℃' in care]

    def extract_brand(self, response):
        return response.css('.pib-title-class ::text').extract_first()

    def extract_categories(self, response):
        trail = response.meta.get('trail', [])
        return [category[0] for category in trail]

    def extract_image_urls(self, response):
        image_urls = response.css('.pic-sliderwrap a::attr(href)').extract()
        return [response.urljoin(url) for url in image_urls]

    def extract_skus(self, response):
        skus = {}
        common_sku = extract_price_details(self.extract_price(response))
        common_sku['colour'] = self.extract_colour(response)
        raw_skus = self.extract_raw_skus(response)

        for raw_sku in raw_skus:
            sku = common_sku.copy()
            sku['id'] = raw_skus[raw_sku]['id']
            sku['size'] = raw_skus[raw_sku]['name']
            skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus

    def extract_colour(self, response):
        css = '.J-colorItem.color-selected .color-item-name::text'
        return response.css(css).extract_first()

    def extract_market(self):
        return 'CHINA'

    def extract_gender(self, response):
        css = '.pib-title-detail::text, .goods-description-title::text'
        return extract_gender(' '.join(response.css(css).extract()))

    def extract_price(self, response):
        css = '.pi-price-box .pbox-yen::text, .pi-price-box .J-price::text, .pi-price-box .J-mPrice::text'
        return response.css(css).extract()

    def extract_retailer(self):
        return 'vipshop'

    def extract_currency(self):
        return 'YUAN'

    def extract_raw_skus(self, response):
        xpath = "//script[contains(., 'sizeStock')]/text()"
        pattern = '"sizeStock":(.*?),"sizeLength"'
        raw_skus = response.xpath(xpath).re_first(pattern)
        return json.loads(raw_skus)


class DrmartensSpider(CrawlSpider):
    name = 'vipshop-crawl-spider'
    allowed_domains = ['vip.com']
    start_urls = ['https://www.vip.com/']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 '
                      'Safari/537.36'
    }

    listing_css = ['.g-wrap', '.c-goods-list', '.goods-list', '.c-hot-category']
    product_css = ['.wrap.clearfix', '.column-operation', '.index-content.s_bg_top', '.c-page']
    rules = [
        Rule(LinkExtractor(restrict_css=product_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item')
    ]

    def parse(self, response):
        title = self.extract_title(response)
        trail = response.meta.get('trail', [])
        trail = trail + [[title, response.url]]

        for request in super().parse(response):
            request.meta['trail'] = trail.copy()
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        return title.split('|')[0] or None

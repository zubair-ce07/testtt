import json

from scrapy import Spider, Request
from scrapy.contrib.spiders import CrawlSpider, Rule

from item_structure import Item
from helpers import extract_price_details, extract_gender, item_or_request


class ProductParser(Spider):
    stock_request_t = 'https://stock.vip.com/detail/?callback=stock_detail&merchandiseId={}'

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
        requests = self.extract_colour_requests(response) + self.extract_stock_detail_request(response)
        item['meta'] = {'requests': requests}

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
                item['skus'][sku]['out_of_stock'] = True

        return item_or_request(item)

    def extract_stock_detail_request(self, response):
        product_id = self.extract_product_id(response)
        return [Request(self.stock_request_t.format(product_id), callback=self.parse_stock_item)]

    def extract_colour_requests(self, response):
        css = '.color-list a:not([class="J-colorItem color-selected"])::attr(href)'
        return [response.follow(url, callback=self.parse_colour_item) for url in response.css(css).extract()]

    def is_new_item(self, product_id):
        if product_id and product_id not in self.seen_ids:
            self.seen_ids.add(product_id)
            return True

        return False

    def extract_product_id(self, response):
        pattern = 'leftSideCoupon.*?productId":"(.*?)"'
        xpath = "//script[contains(., 'leftSideCoupon')]/text()"
        return response.xpath(xpath).re_first(pattern)

    def extract_description(self, response):
        description = response.css('.goods-description-title::text').extract_first()
        return [des.strip() for des in description.split('.') if des.strip()] if description else []

    def extract_name(self, response):
        return response.css('.pib-title-detail::text').extract_first()

    def extract_care(self, response):
        raw_care = response.css('.dc-table.fst td::text').extract()
        return [care.strip() for care in raw_care if '℃' in care or '度' in care]

    def extract_brand(self, response):
        return response.css('.pib-title-class ::text').extract_first()

    def extract_categories(self, response):
        trail = response.meta.get('trail', [])
        return [c for c, _ in trail]

    def extract_image_urls(self, response):
        image_urls = response.css('.pic-sliderwrap a::attr(href)').extract()
        return [response.urljoin(url) for url in image_urls]

    def extract_skus(self, response):
        skus = {}
        raw_skus = self.extract_raw_skus(response)
        if not raw_skus:
            return skus

        common_sku = extract_price_details(self.extract_price(response))
        common_sku['colour'] = self.extract_colour(response)

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
        return json.loads(raw_skus) if raw_skus else None


class VipshopSpider(CrawlSpider):
    name = 'vipshop-crawl-spider'
    allowed_domains = ['vip.com']
    start_urls = ['https://category.vip.com/']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 '
                      'Safari/537.36'
    }

    products_url_t = 'https://category.vip.com/ajax/mapi.php?service=product_info&productIds={}'
    category_url_t = 'https://category.vip.com/ajax/getTreeList.php?tree_id=107&cid={}'
    sub_category_url_t = 'https://category.vip.com/{}'
    product_detail_url_t = 'https://detail.vip.com/detail-{}-{}.html'

    def parse(self, response):
        meta = {'trail': self.extract_trail(response)}
        categories = response.xpath('//script/text()').re_first('cateIdList =(.*])')

        for catg in json.loads(categories):
            yield Request(self.category_url_t.format(catg['cate_id']), callback=self.parse_category, meta=meta.copy())

    def parse_category(self, response):
        meta = {'trail': self.extract_trail(response)}
        sub_categories = response.xpath('//text()').re_first('children":(.*)}]')

        for url in self.extract_sub_cat_urls(sub_categories):
            yield Request(self.sub_category_url_t.format(url), callback=self.parse_sub_category, meta=meta.copy())

    def parse_sub_category(self, response):
        meta = {'trail': self.extract_trail(response)}
        raw_product_ids = response.xpath('//text()').re_first('merchandise.*productIds":(.*])')

        yield Request(self.products_url_t.format(",".join(json.loads(raw_product_ids))), callback=self.parse_products,
                      meta=meta.copy())

    def parse_products(self, response):
        meta = {'trail': self.extract_trail(response)}
        products = response.xpath('//text()').re_first('products":(.*])')
        if not products:
            return

        for product in json.loads(products):
            yield Request(self.product_detail_url_t.format(product['productId'], product['brandId']), meta=meta.copy(),
                          callback=self.parse_item)

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_sub_cat_urls(self, sub_categories):
        urls = []

        for sub_cat in json.loads(sub_categories):
            urls.append(sub_cat['url'])

            for sub_cat2 in sub_cat['children']:
                urls.append(sub_cat2['url'])

        return urls

    def extract_trail(self, response):
        title = self.extract_title(response)
        trail = response.meta.get('trail', [])
        if title:
            trail = trail + [[title, response.url]]

        return trail

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        if title:
            title = title.split('|')[0]

        return title

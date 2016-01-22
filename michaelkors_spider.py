# -*- coding: utf-8 -*-
import re
import json
from base import clean
from scrapy.http import Request
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector
from base import BaseParseSpider, BaseCrawlSpider
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.utils.url import url_query_parameter, url_query_cleaner


class Mixin(object):
    market = 'US'
    retailer = 'michaelkors-us'
    allowed_domains = ['www.michaelkors.com', 'michaelkors.scene7.com']

    url_t = 'http://www.michaelkors.com%s'

    start_urls_with_meta = [(url_t % '/_/N-28ee', {'gender': 'women'}),
                            (url_t % '/men/_/N-2861', {'gender': 'men'}),
                            (url_t % '/shoes/kids/_/N-28ik', {'gender': 'girls'}),
                            (url_t % '/accessories/_/N-282b', {'gender': 'women'}),
                            (url_t % '/watches/watch-hunger-stop/_/N-28z7', {'gender': 'men'}),
    ]


class MichaelKorsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    take_first = TakeFirst()

    price_x = "//div[@id='productPrice']//text()"
    image_url_t = '%s?req=set,json,UTF-8&labelkey=label&id=222835650&handler=s7sdkJSONResponse'
    category_url_t = 'http://www.michaelkors.com/common/ajax/ajaxBreadCrumbs.jsp?productId=%s&isReferer=true'
    sku_url_t = 'http://www.michaelkors.com/browse/pdp/ajax/ajaxProductDetailsInclude.jsp?productId=%s&color' \
                '=%s&skuId=%s'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        pid = self.product_id(hxs)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, hxs, response)

        garment['merch_info'] = self.merch_info(hxs)
        garment['skus'], garment['image_urls'] = {}, []
        garment['meta'] = {'requests_queue': self.sku_requests(hxs) + self.category_request(hxs)}

        return self.next_request_or_garment(garment)

    def parse_category(self, response):
        hxs = HtmlXPathSelector(response)
        garment = response.meta['garment']

        garment['category'] = self.product_category(hxs)

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        hxs = HtmlXPathSelector(response)
        garment = response.meta['garment']

        garment['skus'].update(self.skus(hxs))

        return self.next_request_or_garment(garment)

    def parse_colors(self, response):
        hxs = HtmlXPathSelector(response)
        garment = response.meta['garment']

        color_id = url_query_parameter(response.url, 'color')
        product_id = url_query_parameter(response.url, 'productId')

        #: If sizes for a product does not exists
        if not hxs.select("//select[@class='size_select']"):
            garment['skus'].update(self.skus(hxs))

        skus_id = clean(hxs.select("//select[@class='size_select']//option[position() > 1]/@value"))

        for sku_id in skus_id:
            url = self.sku_url_t % (product_id, color_id, sku_id)
            garment['meta']['requests_queue'] += [Request(url, callback=self.parse_skus)]

        garment['meta']['requests_queue'] += self.images_request(hxs)

        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']

        img_url = "http://michaelkors.scene7.com/is/image/{0}?wid=2000&hei=2000"
        img_data = json.loads(re.search(r's7sdkJSONResponse\(({.*})', response.body).group(1))

        images = img_data['set']['item'] if type(img_data['set']['item']) == list else [img_data['set']['item']]
        for image in images:
            garment['image_urls'] += [img_url.format(image['i']['n'])]

        return self.next_request_or_garment(garment)

    def images_request(self, hxs):
        xpath = "//script[contains(., 'socialSceneURL')]//text()"
        url = hxs.select(xpath).re("socialSceneURL\s*=\s*'(.*?)'")[0]

        return [Request(url=self.image_url_t % url, callback=self.parse_images)]

    def category_request(self, hxs):
        url = self.category_url_t % self.product_id(hxs)

        return [Request(url, callback=self.parse_category)]

    def sku_requests(self, hxs):
        requests = []
        xpath = "//ul[contains(@class,'color_swatch')]//li//@onclick"
        product_id = self.product_id(hxs)
        colors_data = clean(hxs.select(xpath))
        color_ids = [color_data.split("','")[1] for color_data in colors_data]

        for color_id in color_ids:
            url = self.sku_url_t % (product_id, color_id, '')
            requests += [Request(url, callback=self.parse_colors)]

        return requests

    def skus(self, hxs):
        skus = {}
        color = self.take_first(clean(hxs.select("//span[@class='product_color_swatch']//text()")))
        color = color.strip(' - Sold Out')
        size = self.take_first(clean(hxs.select("//span[@class='product_size_labels']/text()").re('SIZE:(.*)')))

        previous_price, price, currency = self.product_pricing(hxs)

        sku = {
            'size': size if size else self.one_size,
            'colour': color,
            'out_of_stock': hxs.select("//div[@class='outofstock-pdp']") != [],
            'price': price,
            'currency': currency
        }

        if not color:
            sku.pop('colour')

        if previous_price:
            sku['previous_prices'] = [previous_price]

        sku_id = self.take_first(clean(hxs.select("//input[@id='rrPDPSkuId']/@value")))
        skus[sku_id] = sku

        return skus

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("//input[@id='productId']//@value")))

    def product_brand(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@class='brand_name']//text()")))

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@class='prod_name']//text()")))

    def product_category(self, hxs):
        return clean(hxs.select("//div[@class='breadcrumb']//text()"))[1:-1]

    def raw_description(self, hxs):
        xpath = "//div[contains(@class,'description_tabs_2')]//text()"
        return clean(hxs.select(xpath))

    def product_description(self, hxs):
        xpath = "//div[contains(@class,'description_tabs_1')]//text()"
        desc = self.take_first(clean(hxs.select(xpath)))
        desc = [desc] + [rd.title() for rd in self.raw_description(hxs) if not self.care_criteria(rd)]

        return desc

    def product_care(self, hxs):
        return [rd for rd in self.raw_description(hxs) if self.care_criteria(rd)]

    def merch_info(self, hxs):
        if 'exclusive' in ' '.join(self.product_category(hxs)).lower():
            return ['EXCLUSIVELY OURS']


class MichaelKorsCrawlSpider(BaseCrawlSpider, Mixin):
    '''
    We don't want to crawl "Gift Cards": http://www.michaelkors.com/gifts/gift-cards/_/N-284w
    '''

    name = Mixin.retailer + '-crawl'
    parse_spider = MichaelKorsParseSpider()

    pagination_url_t = 'http://www.michaelkors.com/browse/search/lazyLoading.jsp' \
                       '?No=%s&N=%s&atgDefaultSku=true&deptCatId=%s&rlPath=%s'

    listings_x = ["//div[@class='sticky-nav fixed']"]
    products_x = ["//div[@class='product_panel']"]
    deny_r = ['gift-cards', 'view-all']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x, deny=deny_r,
                               process_value=lambda url: "http://www.michaelkors.com%s" % url)
             , callback='parse_pages'),

        Rule(SgmlLinkExtractor(restrict_xpaths=products_x,
                               process_value=lambda url: url_query_cleaner(url))
             , callback='parse_item')
    )

    def parse_pages(self, response):

        meta_data = {'trail': self.add_trail(response), 'gender': response.meta['gender']}
        hxs = HtmlXPathSelector(response)
        products = clean(hxs.select("//div[@class='product_panel']//a/@href"))

        for product in products:
            if 'http://' not in product:
                product = 'http://www.michaelkors.com/' + product

            yield Request(product, callback=self.parse_item, meta=meta_data)

        if hxs.select("//input[@id='totalRecord']/@value"):
            #: yield next pages
            total_items = clean(hxs.select("//input[@id='totalRecord']/@value"))[0]
            deptCatId = clean(hxs.select("//input[@id='deptCatId']/@value"))[0]
            N = clean(hxs.select("//input[@id='navValue']/@value"))[0]
            rlPath = clean(hxs.select("//input[@id='rlPath']/@value"))[0]

            products_per_page = 42

            for item_no in range(products_per_page, int(total_items), products_per_page):
                url = self.pagination_url_t % (item_no, N, deptCatId, rlPath)
                yield Request(url, callback=self.parse_pages, meta=meta_data)

    def add_trail(self, response):
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        return response.meta.get('trail', []) + trail_part

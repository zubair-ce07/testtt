# -*- coding: utf-8 -*-
import re
import json
from base import clean, Garment
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

    url_prefix = 'http://www.michaelkors.com%s'

    start_urls_with_meta = [(url_prefix % '/_/N-28ee', {'gender': 'women',
                                                        'link_text': 'Women'}),
                            (url_prefix % '/men/_/N-2861', {'gender': 'men',
                                                            'link_text': 'Men'}),
                            (url_prefix % '/shoes/kids/_/N-28ik', {'gender': 'girls',
                                                                   'link_text': 'Kids'}),
                            (url_prefix % '/accessories/_/N-282b', {'gender': 'women',
                                                                    'link_text': 'Accessories'}),
                            (url_prefix % '/watches/watch-hunger-stop/_/N-28z7', {'gender': 'men',
                                                                                  'link_text': 'Watches'})]


class MichaelKorsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    take_first = TakeFirst()

    price_x = "//div[@id='productPrice']//text()"
    image_url_t = '%s?req=set,json,UTF-8&labelkey=label&id=222835650&handler=s7sdkJSONResponse'
    sku_url_t = 'http://www.michaelkors.com/browse/pdp/ajax/ajaxProductDetailsInclude.jsp?productId=%s_%s&color' \
                '=%s&skuId=%s'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        if hxs.select("//div[contains(.,'This product is no longer available')]"):
            return

        pid = self.product_id(hxs)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, hxs, response)

        garment['category'] = self.product_category(garment)
        garment['merch_info'] = self.merch_info(hxs)
        garment['skus'], garment['image_urls'] = {}, []
        garment['meta'] = {'requests_queue': self.color_requests(hxs)}

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
        product_id = url_query_parameter(response.url, 'productId').split('_')[1]

        #: If sizes for a product does not exist
        if not hxs.select("//select[@class='size_select']"):
            garment['skus'].update(self.skus(hxs))

        skus_id = clean(hxs.select("//select[@class='size_select']//option[position() > 1]/@value"))

        for sku_id in skus_id:
            url = self.sku_url_t % (self.market, product_id, color_id, sku_id)
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

    def color_requests(self, hxs):
        requests = []
        xpath = "//ul[contains(@class,'color_swatch')]//li//@onclick"
        product_id = self.product_id(hxs)
        colors_data = clean(hxs.select(xpath))
        color_ids = [color_data.split("','")[1] for color_data in colors_data]

        for color_id in color_ids:
            url = self.sku_url_t % (self.market, product_id, color_id, '')
            requests += [Request(url, callback=self.parse_colors)]

        return requests

    def skus(self, hxs):
        skus = {}
        color = self.take_first(clean(hxs.select("//span[@class='product_color_swatch']//text()"))) or ''
        size = self.take_first(clean(hxs.select("//span[@class='product_size_labels']/text()").re('SIZE:(.*)')))

        previous_price, price, currency = self.product_pricing(hxs)

        sku = {
            'size': size if size else self.one_size,
            'colour': color.strip(' - Sold Out'),
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
        return self.take_first(clean(hxs.select("//input[@id='productId']//@value"))).split('_')[1]

    def product_brand(self, hxs):
        brand = self.take_first(clean(hxs.select("//h1[@class='brand_name']//text()"))) or "Michael Kors"
        return re.findall('Michael Kors Kid|Michael Michael Kors|Michael Kors', brand.title(), re.I)[0]

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@class='prod_name']//text()")))

    def product_category(self, garment):
        if isinstance(garment, Garment):
            return clean([trail[0] for trail in garment['trail']])

    def raw_description(self, hxs):
        xpath = "//div[contains(@class,'description_tabs_2')]//text()"
        return clean(hxs.select(xpath))

    def product_description(self, hxs):
        xpath = "//div[contains(@class,'description_tabs_1')]//text()"
        desc = clean(hxs.select(xpath))
        desc = desc + [rd.strip('-').strip('"') for rd in self.raw_description(hxs) if not self.care_criteria(rd)]

        return clean(desc)

    def product_care(self, hxs):
        return clean([rd.strip('-').strip('"') for rd in self.raw_description(hxs) if self.care_criteria(rd)])

    def merch_info(self, hxs):
        soup = ' '.join(self.product_description(hxs)).lower()

        if 'exclusive' in soup:
            return ['EXCLUSIVELY OURS']
        return []


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
             , callback='parse_listing'),

        Rule(SgmlLinkExtractor(restrict_xpaths=products_x,
                               process_value=lambda url: url_query_cleaner(url))
             , callback='parse_item')
    )

    def parse_listing(self, response):
        hxs = HtmlXPathSelector(response)
        meta_data = {'trail': self.add_trail(response), 'gender': response.meta['gender']}
        products = clean(hxs.select("//div[@class='product_panel']//a/@href"))

        for product in products:
            if 'http://' not in product:
                product = 'http://www.michaelkors.com/%s' % product

            yield Request(product, callback=self.parse_item, meta=meta_data)

        if hxs.select("//input[@id='totalRecord']/@value"):
            total_items = clean(hxs.select("//input[@id='totalRecord']/@value"))[0]
            dept_cat_id = clean(hxs.select("//input[@id='deptCatId']/@value"))[0]
            n = clean(hxs.select("//input[@id='navValue']/@value"))[0]
            rl_path = clean(hxs.select("//input[@id='rlPath']/@value"))[0]

            products_per_page = 42

            for item_no in range(products_per_page, int(total_items), products_per_page):
                url = self.pagination_url_t % (item_no, n, dept_cat_id, rl_path)
                yield Request(url, callback=self.parse_listing, meta=meta_data)

    def add_trail(self, response):
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        return response.meta.get('trail', []) + trail_part

# -*- coding: utf-8 -*-
import scrapy
import re
import json
import demjson

from parsel import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest

from items import GapItem


class WoolrichParser:
    gender_map = [('女孩', 'girl'), 
                  ('男装', 'men'), 
                  ('女装', 'women'), 
                  ('男孩', 'boy'), 
                  ('孕妇装','women'), 
                  ('幼儿', 'children'), 
                  ('婴儿', 'baby')]
    care_words = ['洗', '棉', '干', '熨', '聚酯', '面料', '纤', '%']
    currency = 'CNY'

    def parse_item(self, response):
        raw_item = self._extract_raw_product(response)
        self.currency = raw_item['currency']

        item = GapItem()
        item['retailer_sku'] = raw_item['identifier']
        item['category'] = raw_item['category']
        item['brand'] = raw_item['brand']
        item['name'] = raw_item['fn']
        item['url'] = response.url
        item['gender'] = self._get_gender(raw_item['category'])
        item["description"] = self._get_description(response)
        item['care'] = self._get_care(response)
        item['image_urls'] = self._get_image_urls(response)
        item['skus']=self._get_skus(response)

        return self._stock_request(item)
    
    def _stock_request(self, item):
        url = 'https://www.gap.cn/catalog/product/getstock?entityId=' + item['retailer_sku']
        return scrapy.Request(url=url, callback=self._skus_availability, meta={'item': item})
    
    def _skus_availability(self, response):
        item = response.meta.get('item')
        stocks = json.loads(response.text)
        for sku in item['skus']:
            if not stocks[sku['id']]:
                sku['out_of_stock'] = True
        return item

    def _get_gender(self, categories):
        for text, gender in self.gender_map:
            if text in categories:
                return gender

        return 'unisex-adults'
    
    def _get_description(self, response):
        description = response.css('#short_description').xpath('descendant-or-self::*/text()').extract()
        return [self.clean_text(d) for d in description if len(d.strip()) > 1]

    def _get_care(self, response):
        css = '.pdp-mainImg td::text, #materialFeatures td::text'
        cares = response.css(css).extract()
        is_care = lambda c: any(word in c for word in self.care_words)
        return [self.clean_text(care) for care in cares if is_care(care)]
    
    def _get_image_urls(self, response):
        return response.css('.more-views a::attr(href)').extract()

    def _get_skus(self, response):
        colors = response.css('.onelist a::attr(title)').extract()
        color_ids = response.css('.onelist a::attr(key)').extract()
        skus = []
        for color, color_id in zip(colors, color_ids):
            skus += self._get_color_skus(response, color, color_id)
        return skus
    
    def _get_color_skus(self, response, color, color_id):
        css = '.size_list_{} a'.format(color_id)
        sizes_sel = response.css(css)
        return [self._make_sku(color, sel) for sel in sizes_sel]
    
    def _make_sku(self, color, selector):
        return {
            'color': color,
            'currency': self.currency,
            'price': selector.css('a::attr(data-final_price)').extract_first(),
            'previous price': selector.css('a::attr(data-price)').extract_first(),
            'size': selector.css('a::attr(data-title)').extract_first(),
            'id': selector.css('a::attr(data-id)').extract_first()
        }

    def _extract_raw_product(self, response):
        xpath = '//script[contains(., "var product = {")]/text()'
        script = response.xpath(xpath).extract_first()
        raw_item = re.search(r"({.*?})", self.clean_text(script)).group(1)
        return demjson.decode(raw_item)

    def clean_text(self, text):
            return re.sub(r'\s+', ' ', text)


class WoolrichCrawler(CrawlSpider):
    parser = WoolrichParser()
    name = 'gap-cn'
    allowed_domains = ['gap.cn']
    start_urls = ['https://www.gap.cn/category/17040.html#side']

    pagination_url = 'https://www.gap.cn/catalog/category/getCategoryProduct'
    download_delay = 0.2

    # rules = (
    #             Rule(LinkExtractor(restrict_css=('#navs'))),
    #             Rule(LinkExtractor(restrict_css=['.treeCenter', '.gapTreeUl']), callback='parse_category')
    #             # Rule(LinkExtractor(restrict_css=('.categoryProductItem')), callback='parse_item')
    #         )

    def parse(self, response):
        return self.parse_category(response)

    def parse_item(self, response):
        print('>'*10, response.url)
    
    def parse_category(self, response):
        categories = response.css('#allCategoryId::attr(value)').extract_first()
        categories = categories[:-1].split(',')
        if len(categories) > 1:
            return

        print("#"*5, "Parsing Category")
        return self.next_page_req(response)

    def next_page_req(self, response):
        last_display_num = int(response.meta.get('displayed_num', 0))

        category_meta_sel = response.css('.clear1')
        if not category_meta_sel:
            return

        cat_id = category_meta_sel.css('::attr(currentcategoryid)').extract_first()
        cat_total_num = category_meta_sel.css('::attr(currentcategorytotalnum)').extract_first()
        display_css = '::attr(currentcategorydisplaynum{})'.format(cat_id)
        cur_display_num = category_meta_sel.css(display_css).extract_first()
        total_displayed = int(cur_display_num) + last_display_num

        if total_displayed < int(cat_total_num):
            all_products_css = '::attr(allproductids{})'.format(cat_id)
            formdata = {
                'urlDisplayCatagoryId': response.css('#category_id::attr(value)').extract_first(),
                'allCategoryId': cat_id + ',',
                'lastCategoryId': cat_id,
                'lastCategoryTotalNum': cat_total_num,
                'currentPage': category_meta_sel.css('::attr(currentpage)').extract_first(),
                'haveDisplayAllCategoryId': cat_id + ',',
                'lastCategoryDisplayNum': cur_display_num,
                'productIds': category_meta_sel.css(all_products_css).extract_first()
            }
            print('@'*5, 'Yielding request')
            return FormRequest(url=self.pagination_url, formdata=formdata,
                                callback=self.parse_page_items,
                                meta={'displayed_num': total_displayed},)


    def parse_page_items(self, response):
        json_res = json.loads(response.text)
        if json_res['status'] != "success":
            return
        res_selector = Selector(json_res['message'])
        category_meta = res_selector.css('.clear1')
        category_id = category_meta.css('::attr(currentcategoryid)').extract_first()
        display_css = '::attr(currentcategorydisplaynum{})'.format(category_id)
        cur_display_num = category_meta.css(display_css).extract_first()
        print('Display Num: ', cur_display_num)
        print(response.meta.get('displayed_num'))
        products_links = res_selector.css('.categoryProductItem h5 a::attr(href)').extract()
        print('L'*5, len(products_links))
        for link in products_links:
            print('^'*10, link)
            #yield FormRequest(url=prod_url, callback=self.parse_item)

        return self.next_page_req(response)

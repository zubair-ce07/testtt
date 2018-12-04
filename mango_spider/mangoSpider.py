# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.http import Request
from mango_spider.items import MangoSpiderItem


class MangospiderSpider(scrapy.Spider):
    name = 'mango_spider'
    allowed_domains = ['mango.com']
    start_urls = ['https://shop.mango.com/us']

    def parse(self, response):

        url = 'https://shop.mango.com/services/menus/header/US/?selectedMenu={}'
        script = response.css('script').re_first('var viewObjectsJson = (.+);')

        page_session = json.loads(script)

        url = url.format(page_session['headerMenusParams']['optionalParams']['selectedMenu'])
        yield Request(url=url, callback=self.parse_menu)

    def parse_menu(self, response):
        page = json.loads(response.text)
        for link in page['menus']:

            level2_links = link.get('menus', [])
            if not level2_links:
                continue

            for key, links in level2_links.items():
                for level3_link in links:
                    url = level3_link.get('link')
                    if not url:
                        continue
                    yield Request(url=url, callback=self.parse_categories)

    def parse_categories(self, response):

        url = 'https://shop.mango.com/services/cataloglist/filtersProducts/US/{}/{}/?columnsPerRow={}'
        script = response.css('script').re_first('var viewObjectsJson = (.+);')

        page_session = json.loads(script)

        if not page_session.get('catalogParameters'):
            return

        url = url.format(page_session['catalogParameters']['idShop'],
                         page_session['catalogParameters']['idSection'],
                         page_session['catalogParameters']['optionalParams']['columnsPerRow']
                         )

        yield Request(url=url, callback=self.parse_items)

    def parse_items(self, response):
        page = json.loads(response.text)
        for items in page['products']['groups']:
            garments = items.get('garments', [])
            for garments_id in garments:
                mango_items = MangoSpiderItem()

                item_name = garments[garments_id]['name']

                item_sale_price = garments[garments_id]['price']['salePrice']
                item_crossedout_price = garments[garments_id]['price']['crossedOutPrices']
                item_discount_rate = garments[garments_id]['price']['discountRate']

                item_stock = garments[garments_id]['stock']
                item_category = garments[garments_id]['analyticsEventsData']['category']

                size = garments[garments_id]['colors'][0]['sizes']
                all_sizes = [x['label'] for x in size]

                item_page_url = garments[garments_id]['colors'][0]['linkAnchor']

                images = garments[garments_id]['colors'][0]['images']
                hq_image_url = [x['img1HQSrc'] for x in images]

                mango_items['title'] = item_name
                mango_items['category'] = item_category
                mango_items['sale_price'] = item_sale_price
                mango_items['crossed_out_price'] = item_crossedout_price
                mango_items['discount'] = item_discount_rate
                mango_items['stock'] = item_stock
                mango_items['sizes'] = all_sizes
                mango_items['page_url'] = item_page_url
                mango_items['image_url'] = hq_image_url

                yield mango_items
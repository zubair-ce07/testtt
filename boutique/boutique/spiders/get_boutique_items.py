# -*- coding: utf-8 -*-
import re
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import BoutiqueItem


class BoutiqueSpider(CrawlSpider):
    name = 'boutiqueItem'
    allowed_domains = ['www.boutique1.com']
    start_urls = ['https://www.boutique1.com']
    base_url = ['https://www.boutique1.com']
    price_adjustment = 100
    download_delay = 1

    rules = [Rule(LinkExtractor(allow='/', restrict_css=['.megamenu', '.product-items'], unique=True),
                  callback='parse_item_detail', follow=True)]

    def parse_item_detail(self, response):
        """ parsing the product  """
        is_product_view_url = response.css('body.catalog-product-view').get()
        # Checking for a valid product view url
        if is_product_view_url:
            # getting product Image URLs from page inline script
            parse_scripts = response.css('body').get()
            image_urls = re.findall('"img":"(.+?)",', parse_scripts)
            sku_list = re.findall('"optionStockStatuses":(.+?)}},', parse_scripts)

            boutique_item = BoutiqueItem()
            boutique_item['retailer_sku'] = \
                response.css('.product-info-main .price-final_price::attr(data-product-id)').get(),
            boutique_item['name'] = \
                response.css('.product-info-main .page-title-wrapper h1 span::text').get(),
            boutique_item['price'] = \
                float(response.css('[itemprop=price]::attr(content)').get()) * self.price_adjustment,
            boutique_item['market'] = response.css('#change-destination strong span::attr(data-value)').get(),
            boutique_item['url'] = response.url,
            boutique_item['description'] = response.css('.product.attribute.detail p::text').getall(),
            boutique_item['image_urls'] = image_urls,
            boutique_item['sku_list'] = sku_list

            yield boutique_item

    def change_currency(self, response):
        """ getting the form submit url for changing the shipping and currency """
        shipping_url = 'https://www.boutique1.com/storeswitcher/store/switch/'
        data = {
            'shipping_code': 'AL',
            'currency': 'EUR',
            '___store': 'en_eur'
        }

        yield scrapy.FormRequest(url=shipping_url, formdata=data, callback=self.parse_site)

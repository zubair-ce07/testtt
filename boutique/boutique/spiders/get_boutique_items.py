# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re


class BoutiqueItemSpider(CrawlSpider):
    name = 'boutiqueItem'
    allowed_domains = ['www.boutique1.com']
    start_urls = ['https://www.boutique1.com']
    base_url = ['https://www.boutique1.com']
    price_adjustment = 100
    download_delay = 1

    rules = [Rule(LinkExtractor(allow='/'),
                  callback='parse_item_detail', follow=True)]

    def parse_item_detail(self, response):
        """ parsing the product  """
        def extract_from_css(query):
            return response.css(query)
        is_product_view_url = response.css('body.catalog-product-view').get()
        # Checking for a valid product view url
        if is_product_view_url:
            # getting product Image URLs from page inline script
            parse_scripts = response.css('body').get()
            image_urls = re.findall('"img":"(.+?)",', parse_scripts)
            sku_list = re.findall('"optionStockStatuses":(.+?)}},', parse_scripts)

            yield {
                'retailer_sku': extract_from_css('.product-info-main .price-final_price::attr(data-product-id)').get(),
                'name': extract_from_css('.product-info-main .page-title-wrapper h1 span::text').get(),
                'price': float(extract_from_css('[itemprop=price]::attr(content)').get())*self.price_adjustment,
                'market': extract_from_css('#change-destination strong span::attr(data-value)').get(),
                'url': response.url,
                'description': extract_from_css('.product.attribute.detail p::text').getall(),
                'image_urls':   image_urls,
                'sku_list':   sku_list
                    }


    # def parse(self, response):
    #     """ getting the form submit url for changing the shipping and currency """
    #     shipping_url = 'https://www.boutique1.com/storeswitcher/store/switch/'
    #     data = {
    #         'shipping_code': 'AL',
    #         'currency': 'EUR',
    #         '___store': 'en_eur'
    #     }
    #
    #     yield scrapy.FormRequest(url=shipping_url, formdata=data, callback=self.parse_site)
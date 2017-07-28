# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.spiders import CrawlSpider
from scrapy.spider import Rule
from scrapy.linkextractors import LinkExtractor
from newbal_spiders.items import NewbalanceItem


class NewbalanceSpider(CrawlSpider):
    name = 'newbalance'
    allowed_domains = ['newbalance.com']
    start_urls = [
        'http://www.newbalance.com/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css='.product-paging .page-next')),
        Rule(LinkExtractor(restrict_css='.product-groups .default-content [href]'), callback='parse_prod', follow=True),
        Rule(LinkExtractor(restrict_css='.subcategory-title .no-h-style [href]'), callback='parse_prod', follow=True),
    )

    custom_settings = {
        "ITEM_PIPELINES": {
            'newbal_spiders.pipelines.NewbalSpidersPipeline': 300,
        }
    }

    def parse_prod(self, response):
        for attr in response.css('#product-list-main .tile'):
            item = NewbalanceItem()
            item['product_url'] = attr.css('.product::attr(data-monetate-producturl)').extract_first()
            product_id = attr.css('.product::attr(data-product-id)').extract_first()
            varianturl = 'http://www.newbalance.com/on/demandware.store/Sites-newbalance_us2-Site/en_US/Product-GetVariants?pid=' + product_id

            request = scrapy.Request(item['product_url'], callback=self.parse_details,
                                     meta={'varianturl': varianturl, 'item': item})
            yield request

    def parse_details(self, response):
        item = response.meta['item']
        varianturl = response.meta['varianturl']
        item = self.item_id(item, response)
        item = self.item_title(item, response)
        item = self.item_category(item, response)
        item = self.item_description(item, response)
        item = self.item_locale(item, response)
        item = self.item_currency(item, response)
        yield scrapy.Request(varianturl, callback=self.item_variations, meta={'item': item}, dont_filter=True)
        return item

    def item_id(self, item, response):
        item['product_id'] = response.css('.product-meta::attr(data-pid)').extract_first()
        return item

    def item_title(self, item, response):
        item['title'] = str(response.css('.product-name.hide-for-mobile::text').extract_first()).strip()
        return item

    def item_category(self, item, response):
        item['category'] = response.css('.navbar::attr(data-active-category-url)').extract_first()
        return item

    def item_description(self, item, response):
        item['description'] = response.css('.longdescription::text').extract_first()
        return item

    def item_locale(self, item, response):
        item['locale'] = response.css('#locale::attr(value)').extract_first()
        return item

    def item_currency(self, item, response):
        currency = json.loads(response.css('script[type*="application/ld+json"]::text').extract_first())
        item['currency'] = currency['offers']['priceCurrency']
        return item

    def item_variations(self, response):
        item = response.meta['item']
        dynamic_response = json.loads(response.text)
        variants = dynamic_response['variants']
        styles = dynamic_response['styles']
        color = []
        sizeitem = {}
        sizeitems = []
        for x in variants:
            color.append(x['attributes']['color']['value'])
            unique_color = list(set(color))
            '''for size items'''
            sizeitem['color'] = x.get('attributes').get('color').get('displayValue')
            # for size
            sizeitem['sizeitems'] = x.get('attributes').get('size').get('displayValue')
            # for availibility
            if x['availability']['avStatus'] == "IN_STOCK":
                sizeitem['Is_available'] = True
            else:
                sizeitem['Is_available'] = False
            # for price
            sizeitem['price'] = x.get('pricemodel').get('pricing').get('salesPriceFormatted')
            # fordiscount
            try:
                x['pricemodel']['pricing']['standardPriceFormatted']
                sizeitem['Is_Discounted'] = (True)
                sizeitem['Discounted_price'] = x.get('pricemodel').get('pricing').get('standardPriceFormatted')
            except KeyError:
                sizeitem['Is_Discounted'] = False
                sizeitem['Discounted_price'] = ''
                sizeitems.append(sizeitem)
        # get image urls against unique colors
        for key, value in styles.items():
            image_urls = value['images']
            img = []
            imgs = []
            for url in image_urls:
                img.append(url['URL'])
                imgs.append(img)
            item['variationitems'] = dict(zip(unique_color, imgs))
        return item

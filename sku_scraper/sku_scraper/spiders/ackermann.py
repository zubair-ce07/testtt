# -*- coding: utf-8 -*-
import json

from scrapy import Request,Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.selector import Selector

from ..items import Item


class AckermannParseSpider(Spider):
    name = 'ackermannParser'
    allowed_domains = ['ackermann.ch']
    image_url_t = 'https://media.ackermann.ch/i/empiriecom/{}'

    def parse(self, response):
        """
        Parse the json data in script available on the product page
        """
        raw_product = response.xpath(
            '//script[contains(@class, "data-product-detail")]/text()').extract_first()
        if not raw_product:
            return

        raw_product = json.loads(raw_product)
        item = Item()
        item['retailer_sku'] = self.extract_retailer_sku(raw_product)
        item['name'] = self.extract_name(raw_product)
        item['description'] = self.extract_description(raw_product)
        item['category'] = self.extract_category(raw_product)
        item['image_urls'] = self.extract_image_urls(raw_product)
        item['care'] = self.extract_care(raw_product)
        item['skus'] = self.extract_skus(raw_product)
        item['brand'] = self.extract_brand(raw_product)

        yield item

    def extract_retailer_sku(self, raw_product):
        return raw_product.get('sku')

    def extract_brand(self, raw_product):
        brand = raw_product.get('brandLinkName')
        if brand:
            return brand
        else:
            brand = raw_product.get('name').split(raw_product.get('nameWithoutManufacturer'))[0]
            return brand.strip()

    def extract_name(self, raw_product):
        return raw_product.get('nameWithoutManufacturer')

    def extract_category(self, raw_product):
        return raw_product.get('defaultCategoryName')

    def extract_description(self, raw_product):
        """
        Returns the description as a string
        """
        description = raw_product.get('longDescription')
        return [i for i in Selector(text=description).xpath('//text()').extract() if i] or []


    def extract_image_urls(self, raw_product):
        """
        Groups together the image urls of an item in a list and returns it.
        """
        raw_images = raw_product['imageList']
        return [
            self.image_url_t.format(image_no['image']) 
            for images in raw_images.values() for image_no in images
        ]

    def extract_care(self, raw_product):
        """
        Finds and returns the care for an object
        """
        raw_care = raw_product.get('tags')
        raw_care = [Selector(text=rc).xpath('//text') for rc in raw_care.values()]
        return [rc for rc in raw_care if '%' in rc]

    def extract_skus(self, raw_product):
        """
        Get all the skus or variations of a product.
        Returns dict
        """
        variations = raw_product['variations']
        skus = dict()
        for sku_id, sku_detail in variations.items():
            skus[sku_id] = {
                'price': int(sku_detail['currentPrice']['value']*100),
                'currency': sku_detail['currentPrice']['currency'],
            }
            if sku_detail.get('oldPrice'):
                skus[sku_id]['previous_price'] = int(sku_detail['oldPrice']['value']*100)

            raw_size = sku_detail['variationValues']
            size = [raw_size.get('Var_Size'), raw_size.get('Var_Dimension3')] or ['One Size']
            skus[sku_id]['size'] = '/'.join([s for s in size if s])
            skus[sku_id]['color'] = sku_detail['variationValues'].get('Var_Article')

        return skus


class AckermannCrawlSpider(CrawlSpider):
    name = 'ackermannCrawler'
    allowed_domains = ['ackermann.ch']
    start_urls = ['https://www.ackermann.ch/']
    listings_url = 'https://www.ackermann.ch/suche/mba/magellan'
    product_url_t = 'https://www.ackermann.ch/p/{}'

    product_parser = AckermannParseSpider()

    payload = {
        "start":0,
        "clientId":"AckermannCh",
        "version":42,
        "channel":"web",
        "locale":"de_CH",
        "count":72,
        }
    
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }

    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 6.2; WOW64)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
    }

    listings_xpath = '//li[contains(@class,"customdelay")]'
    rules = (Rule(LinkExtractor(restrict_xpaths=(listings_xpath)),callback='parse_category'),)

    def parse_category(self, response):
        """Called on the html response received from navigating on the
        main nav bar on the home page. Gets the category number from the page
        and calls the api based on that.
        """
        # category number is in this json
        raw_listing = response.xpath('//script[contains(@class, "super-fake-data")]/text()'
                                        ).extract_first()
        if not raw_listing:
            return
        category = json.loads(raw_listing)
        category = category['request']['category']
        payload = self.payload.copy()
        payload["category"] = category

        yield Request(
            url=self.listings_url,
            method='POST',
            body=json.dumps(payload),
            callback=self.parse_listings,
            headers=self.headers
        )
    
    def parse_listings(self, response):
        """
        Receves the json response on a category and then extracts products and child
        categories from that response, keeps calling the listing_url for pagination
        as well.
        """
        raw_listings = json.loads(response.text)
        raw_categories = raw_listings['searchresult']['categoryNavigation']


        for category in raw_categories:
            for subcategory in (category.get('childs') or []) + [category]:
                payload = self.payload.copy()
                if subcategory['selected']:
                    offset = raw_listings['searchresult']['request']['start']
                    total_products = raw_listings['searchresult']['result']['count']
                    
                    product_listings = raw_listings['searchresult']['result']['styles']
                    yield from self.product_requests(product_listings)

                    if offset < total_products and product_listings:
                        payload["start"] = offset + payload["count"]

                payload["category"] = subcategory['id']
                yield Request(
                    url=self.listings_url,
                    method='POST',
                    body=json.dumps(payload),
                    callback=self.parse_listings,
                    headers=self.headers
                )

    def product_requests(self, product_listings):
        for product in product_listings:
            url = self.product_url_t.format(product['masterSku'])
            yield Request(url=url, callback=self.parse_product)
        
    def parse_product(self, response):
        yield from self.product_parser.parse(response)

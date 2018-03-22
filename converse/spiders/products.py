# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from converse.items import ProductData


class ProductsSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['www.converse.ca']
    start_urls = ["https://www.converse.ca/"]

    rules = (
        # First rule extracts links for women sneakers, only exclusion is all-sneakers category
        Rule(LinkExtractor(restrict_css="#nav .nav-1-2>ul a", deny=('/all-sneakers/', )), callback='parse_start_url'),
        # Second rule extracts links for men sneakers,  only exclusion is all-sneakers category
        Rule(LinkExtractor(restrict_css="#nav .nav-2-2>ul a", deny=('/all-sneakers/', )), callback='parse_start_url'),
    )

    def parse_start_url(self, response):
        # Call parse_item
        return self.parse_item(response)

    def parse_item(self, response):
        # Get Item count from the page
        item_count = response.css('.bread_count>strong')
        if item_count:
            # If item count > 24, append show/all(if not already present) with url to fetch all records
            if int(item_count.re(r'[0-9]+')[0]) > 24 and "show/all" not in response.url:
                yield scrapy.Request(url=response.urljoin('show/all/'), callback=self.parse_item)
            else:
                for product in response.css('.category-products .item.last'):
                    result = ProductData()
                    result['product_cat'] = self.product_cat(product)
                    result['gender'], result['category'], result['sub_category'] = self.product_info(product)
                    result['brand'] = self.product_brand(product)
                    result['name'] = self.product_name(product)
                    result['product_id'] = self.product_id(product)
                    result['product_url'] = self.product_url(product)
                    result['data_id'] = self.data_id(product)
                    result['price'], result['currency'] = self.price_info(product)
                    result['image_urls'] = self.image_urls(product)
                    result['item_info'] = self.item_info(product)
                    # Go to item page to fetch additional information
                    if result['item_info']:
                        request = scrapy.Request(url=result['product_url'], callback=self.parse_item_page)
                        request.meta['result'] = result
                    yield result

    def parse_item_page(self, response):
        # Fetch results from individual item page
        result = response.meta['result']
        for item in response.css('.cloneItem>img'):
            result['item_info'].append(
                {
                    'color_detail': item.css('img::attr(title)').extract_first()
                }
            )
        yield result

    def product_cat(self, product):
        """
        Get product category by combining gender, category and sub category
        :param product:
        :return: product cat
        """
        product_info = product.css('.product-image::attr(data-category)').extract_first()
        return str(product_info).replace('/', '_')

    def product_info(self, product):
        """
        Get product Information like gender, category and sub category
        :param product:
        :return: gender, category and sub category
        """
        info = str(product.css('.product-image::attr(data-category)').extract_first()).split('/')
        gender = info[0]
        category = info[1]
        sub_category = info[2]
        return gender, category, sub_category

    def product_brand(self, product):
        """
        Get product brand
        """
        return product.css('.product-image::attr(data-brand)').extract_first()

    def product_name(self, product):
        """
        get product name
        """
        return product.css('.product-image::attr(data-name)').extract_first()

    def product_url(self, product):
        """
        Get product url
        """
        return product.css('.product-image::attr(href)').extract_first()

    def product_id(self, product):
        """
        Get product ID
        """
        img_product_id = product.css('.product-image>img::attr(id)').extract_first()
        return img_product_id.split('-')[-1]

    def data_id(self, product):
        """
        Get data ID
        """
        return product.css('.product-image::attr(data-id)').extract_first()

    def price_info(self, product):
        """
        Get price and currency information
        :param product:
        :return: price, currency
        """
        price = product.css('.price::text').re(r'[0-9\.]+')[0]
        currency = product.css('.price::text').re(r'([a-zA-Z]+)')[0]
        return price, currency

    def image_urls(self, product):
        """
        Get image urls
        """
        img_url = product.css('.product-image>img::attr(src)').extract_first()
        if not img_url.startswith("http"):
            img_url = "https:" + img_url
        return [img_url]

    def item_info(self, product):
        """
        Get item info like iten id and item color
        :param product:
        :return: item id, item color
        """
        info = []
        for item in product.css('ul>li'):
            info.append(
                {
                    'item_id': item.css('li::attr(data-option-label)').extract_first(),
                    'basic_color': item.css('li::attr(data-basic-color)').extract_first()
                }
            )
        return info

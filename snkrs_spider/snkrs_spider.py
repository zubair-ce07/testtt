# -*- coding: utf-8 -*-
import scrapy


class SnkrsSpider(scrapy.Spider):
    name = 'snkrs_spider'
    allowed_domains = ['snkrs.com/en/']
    start_urls = ['https://www.snkrs.com/en']

    def parse(self, response):
        category_urls = response.css('ul.sf-menu li a::attr(href)').extract()

        for url in category_urls:
            yield scrapy.Request(url, callback=self.parse_product_listings, dont_filter=True)

    def parse_product_listings(self, response):
        product_urls = response.css('div.product-container a::attr(href)').extract()

        for url in product_urls:
            yield scrapy.Request(url, callback=self.parse_product_details, dont_filter=True)

    def parse_product_details(self, response):
        colour = response.css('h1[itemprop="name"]::text').extract_first().split(' - ')[1]
        retailer_sku = response.css('span[itemprop="sku"]::text').extract_first()
        category = response.css('div[class="nosto_product"] span[class="category"]::text') \
                        .extract_first().split('/')[2]

        if 'men' in category.lower():
            gender = category.split(' ')[0]
        else:
            gender = 'Unisex adult'

        product_reference = response.css('[id="product_reference"] label::text').extract() + [retailer_sku]
        sizes = response.css('span[class="units_container"] span[class="size_EU"]::text').extract() \
                     or response.css('ul li:not([class=" hidden"]) span[class="units_container"]::text').extract() \
                     or ['oneSize'] 
        
        skus = {}

        for size in sizes:            
            skus[f'{colour}_{size}'] = {
                'price': float(response.css('span[itemprop="price"]::attr(content)').extract_first()),
                'currency': response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first(),
                'size': size,
                'colour': colour,
                }
                 
        yield {
            'retailer_sku': retailer_sku,
            'gender': gender,
            'category': [category],
            'brand':  response.css('meta[itemprop="brand"]::attr(content)').extract_first(),
            'url': response.css('span[class="url"]::text').extract_first(),
            'name': response.css('h1[itemprop="name"]::text').extract_first().split(' - ')[0],
            'description': product_reference + response.css('div[id="short_description_content"] p::text').extract(),
            'care': [],
            'skus': skus,
            'image_urls': response.css('div[id="carrousel_frame"] li a::attr(href)').extract()            
        }

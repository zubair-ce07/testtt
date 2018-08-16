import json
from scrapy import Spider, Request
from urllib.parse import urlparse
from bonmarche.items import ProductItem


class ProductParser(Spider):
    name = "bonmarche-parse"
    image_urls = []
    skus = {}

    def parse(self, response):
        product = ProductItem(brand="bonmarche", market="UK", retailer="bonmarche-uk", currency="GBP", gender="women")
        product['retailer_sku'] = self.product_id(response)
        product['trail'] = self.product_trail(response)
        product['category'] = self.product_category(response)
        product['url'] = response.url
        product['name'] = self.product_name(response)
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        self.generate_skus(response)
        product['image_urls'] = self.image_urls
        product['skus'] = self.skus

        product['spider_name'] = self.name
        return product

    def product_id(self, response):
        return response.css('::attr(data-masterid)').extract_first()

    def product_trail(self, response):
        trail_urls = response.meta.get('trail', ['https://www.bonmarche.co.uk/'])
        return [[url.split("/")[-1].split(".")[0], url] for url in trail_urls]

    def product_category(self, response):
        categories = response.css('.breadcrumb-element [itemprop=name]::text').extract()
        return [category.strip() for category in categories if category][1:-1]

    def product_name(self, response):
        return response.css('.xlt-pdpName::text').extract_first()

    def product_description(self, response):
        description = response.css('.product-description::text, .feature-value::text').extract()
        return [desc.strip() for desc in description if desc][:-1]

    def product_care(self, response):
        return response.css('.product-description::text, .feature-value::text').extract()[-1:]

    def image_url(self, response):
        raw_images = response.css('.productthumbnail::attr(data-lgimg)').extract()
        image_urls_ = [json.loads(url)["url"] for url in raw_images]
        return [urlparse(url).geturl() for url in image_urls_]

    def generate_skus(self, response):
        color_urls = response.css('.color .swatchanchor.selectable::attr(href)').extract()
        for url in color_urls:
            print(url)
            Request(url, callback=self.product_details)

    def product_details(self, response):
        self.image_urls.append(self.image_url(response))
        size_urls = response.css('.size .swatchanchor.selectable::attr(href)').extract()
        sizes = response.css('.size .swatchanchor.selectable::text').extract()
        request = Request(size_urls[0], callback=self.product_sku)
        request.meta['sizes'] = sizes

    def product_sku(self, response):
        sizes = response.meta['sizes']
        pricing = {}
        skus_={}
        color = response.css('.attribute .label::text').extract_first()
        color = color.split(":")[-1].strip()
        pricing['colour'] = color
        pricing['currency'] = 'GBP'
        previous_price = response.css('.price-standard::text')
        if previous_price:
            pricing['previous_price'] = previous_price.remove('£').strip()
        pricing['price'] = response.css('.price-sales::attr(content)').extract_first()
        for size in sizes:
            sku = pricing.copy()
            sku['size'] = size
            skus_[color+'_'+size] = sku
        self.skus.update(skus_)

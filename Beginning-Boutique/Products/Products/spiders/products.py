import scrapy
from ..items import ProductsItem


class BeginningBoutique(scrapy.Spider):
    name = "product_store"

    def start_requests(self):
        start_url = 'https://www.beginningboutique.com.au/'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def store_product(self, brand, name, price, care, description, image_urls, gender,
                      currency, market, url_original, retailer):
        items = ProductsItem()
        items['brand'] = brand
        items['gender'] = gender
        items['name'] = name
        items['price'] = price
        items['care'] = care
        items['description'] = description
        items['currency'] = currency
        items['market'] = market
        items['image_urls'] = image_urls
        items['url_original'] = url_original
        items['retailer'] = retailer
        return items

    def extract_product(self, response):
        gender = 'Women'
        currency = 'AUD'
        url_original = response.url
        domain = url_original.split('/')[2].split('.')
        market = domain[len(domain) - 1]
        retailer = '{}-{}'.format(domain[1], market)
        brand = response.css('.product-heading__vendor a::text')[0].extract()
        name = response.css('.product-heading__title::text')[0].extract()
        price = response.css('.product__price').xpath("//span[@class='money']/text()").extract_first()
        product_spec = response.css('.product__specs-detail')
        care = product_spec[1].xpath(".//ul//div//li/text()").extract()
        description = product_spec[0].xpath(".//p/text()").extract()
        description.extend(product_spec[0].xpath(".//ul//li/text()").extract())
        image_urls = response.css('.product-images__slide').xpath(".//img/@src").extract()
        return self.store_product(brand, name, price, care, description,
                                  image_urls, gender, currency, market, url_original, retailer)

    def parse_product(self, response):
        product_items = self.extract_product(response)
        yield {
            'items': product_items
        }

    def parse_category(self, response):
        category_urls = response.css('a.product-card-image-wrapper::attr(href)').getall()
        for url in category_urls:
            yield response.follow(url=url, callback=self.parse_product, dont_filter=True)

    def parse_category_page(self, response):
        category_pagination_urls = response.css('li.pagination__item a::attr(href)').getall()
        if len(category_pagination_urls) > 0:
            for pagination_url in category_pagination_urls:
                yield response.follow(url=pagination_url, callback=self.parse_category, dont_filter=True)
        yield response.follow(url=response.url, callback=self.parse_category, dont_filter=True)

    def parse(self, response):
        products_urls = response.css('.site-nav--has-dropdown a.site-nav__link::attr(href)').getall()
        for url in products_urls:
            yield response.follow(url, callback=self.parse_category_page, dont_filter=True)

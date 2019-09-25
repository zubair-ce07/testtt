import scrapy

from ..items import ProductsItem


class BeginningBoutique(scrapy.Spider):
    name = "beginning_botique"
    market = 'AU'
    retailer = 'beginningboutique-au'
    start_urls = ['https://www.beginningboutique.com.au/']

    def extract_product(self, response):
        items = ProductsItem()
        items['gender'] = 'Women'
        items['currency'] = 'AUD'
        items['url_original'] = response.url
        items['market'] = BeginningBoutique.market
        items['retailer'] = BeginningBoutique.retailer
        items['brand'] = response.css('.product-heading__vendor a::text')[0].extract()
        items['name'] = response.css('.product-heading__title::text')[0].extract()
        items['price'] = response.css('.product__price').xpath("//span[@class='money']/text()").extract_first()
        product_spec = response.css('.product__specs-detail')
        items['care'] = product_spec[1].xpath(".//ul//div//li/text()").extract()
        items['description'] = product_spec[0].xpath(".//p/text()").extract()
        items['description'].extend(product_spec[0].xpath(".//ul//li/text()").extract())
        items['image_urls'] = response.css('.product-images__slide').xpath(".//img/@src").extract()
        return items

    def parse_product(self, response):
        product_items = self.extract_product(response)
        yield product_items

    def parse_category(self, response):
        product_urls = response.css('.product-card-image-wrapper::attr(href)').getall()
        category_pagination_urls = response.css('li.pagination__item a::attr(href)').getall()
        for url in product_urls:
            yield response.follow(url=url, callback=self.parse_product, dont_filter=True)

        for pagination_url in category_pagination_urls:
            yield response.follow(url=pagination_url, callback=self.parse_category, dont_filter=True)

    def parse(self, response):
        category_urls = response.css('.site-nav--has-dropdown a.site-nav__link::attr(href)').getall()
        for url in category_urls:
            yield response.follow(url, callback=self.parse_category, dont_filter=True)

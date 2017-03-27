
import scrapy
from kith.items import KithItem


class ShoppingCartSpider(scrapy.Spider):
    name = "shoping"
    start_urls = ['https://kith.com']

    def parse(self, response):
        urls = response.xpath("//li[@class='ksplash-header-upper-item']/a/@href").extract()
        for url in urls:
            absolute_urls =  response.urljoin(url)
            yield scrapy.Request(url=absolute_urls, callback=self.main_categories_links)

    def main_categories_links(self, response):
        # Fetch main categories for all genders

        category_url = response.xpath("//*[@class='main-nav-list-subtitle']"
                                      "/parent::li[1]//following-sibling::li/a/@href").extract()
        if category_url:
            for cat_url in category_url:
                absolute_cat_urls = 'https://kith.com{}'.format(cat_url)
                yield scrapy.Request(url=absolute_cat_urls, callback=self.products_main_page)
        else:
            kid_cat_url = response.xpath("//ul/li[@class='main-nav-list-item'][2]/a/@href").extract()
            for kid_url in kid_cat_url:
                absolute_kid_urls = 'https://kith.com{}'.format(kid_url)
                yield scrapy.Request(url=absolute_kid_urls, callback=self.products_main_page)

    def products_main_page(self, response):
        #creats all the products link for further use

        product_links = response.xpath("//a[@class='product-card-info']/@href").extract()
        for prod_link in product_links:
            absolute_products_link =  'https://kith.com{}'.format(prod_link)
            yield scrapy.Request(url=absolute_products_link, callback=self.final_products_details)

    def final_products_details(self, response):
        #collects the final details of product

        item = KithItem()
        item['name'] = response.xpath("//h1[@class='product-header-title']/span/text()").extract()
        item['colour'] = response.xpath("//span[@class='product-header-title -variant']/text()").extract()[0].strip()
        item['price'] = response.xpath("//span[@id='ProductPrice']/text()").extract()[0].strip()
        item['detail'] = response.xpath("//div[@class='product-single-details-rte rte mb0']/p/text()").extract()
        sku_id = response.xpath("//p[contains(text(),'Style')]/text()").extract()
        item['sku_id'] = [d.split(":")[-1] for d in sku_id]
        item['image_link'] = response.xpath("//img[@class='js-super-slider-photo-img super-slider-photo-img']/@src").extract()
        yield item




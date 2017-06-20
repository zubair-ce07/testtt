import scrapy
from scrapy.spiders import Rule

from ernstingsfamily.items import Product, StoreKeepingUnits
from scrapy.linkextractors import LinkExtractor

class ErnstingsFamilySpider(scrapy.Spider):
    name = 'ernstings_family'
    allowed_domains = ['www.ernstings-family.de']
    start_urls = ['http://www.ernstings-family.de']

    rules = [
        Rule(
            LinkExtractor(
                restrict_xpaths=".//ul[@id='navi_main']",
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse"
        )
    ]

    def parse(self, response):
        for page in response.xpath(".//ul[@id='navi_main']/li/a"):
            url = page.xpath("./@href").extract_first()
            #for l in response.xpath('//@href').extract():
            #yield {'u': l}
            yield scrapy.Request(url, callback=self.get_urls_of_given_category)

    def get_urls_of_given_category(self, response):
        for item_page in response.xpath(".//li[contains(@id,'catList')]//a/@href").extract():
            yield scrapy.Request(item_page, callback=self.parse_products)

    def parse_products(self, response):
        for product in response.xpath('.//li[@class="list_product"]'):
            url = response.urljoin(product.xpath('.//div[@class=\'product_basic_content\']/a//@href').extract_first())
            yield scrapy.Request(url, callback=self.get_complete_details_of_single_product)

    def get_complete_details_of_single_product(self, response):
        product_item = Product()
        product_item['url'] = response.url
        product_item['actual_price'] = response.xpath(".//strike/text()").extract_first()
        product_item['discount_price'] = response.xpath("//*[@class='prd_price prd_new_price']/text()").extract_first()
        product_item['description'] = response.xpath(".//p[@class='infotext']/text()").extract()
        product_item['name'] = response.xpath(".//span[@class='prd_name']/text()[1]").extract_first()
        product_item['description'] = product_item['description'][2]
        imgs = []
        for img in response.xpath(".//div[@id='prd_thumbs']/a"):
            imgs.append(img.xpath("./img/@src").extract_first())

        product_item['image_urls'] = imgs
        product_item['skus'] = []
        color = response.xpath("//script[@type='text/javascript']/text()").re(r'"Farbe":\["(.*)"]')
        color = color[0]
        sizes =  response.xpath("//script[@type='text/javascript']/text()").re(r'"Größe":\["(.*)"],')
        sizes = sizes[0]
        sizes = sizes.split(',')
        for s in sizes:
            sku = StoreKeepingUnits()
            sku['actual_price'] = product_item['actual_price']
            sku['discount_price'] = product_item['discount_price']
            sku['colour'] = color
            sku['size'] = s
            sku['sku_id'] = product_item['name'] + '_' + sku['size']
            product_item['skus'].append(sku)

        return product_item

import scrapy
from ernstingsfamily.items import Product, StoreKeepingUnits

class ErnstingsFamilySpider(scrapy.Spider):
    name = 'ernstings_family'
    allowed_domains = ['www.ernstings-family.de']
    start_urls = ['http://www.ernstings-family.de']


    def parse(self, response):

        for page in response.xpath(".//ul[@id='navi_main']/li/a"):
            url = page.xpath("./@href").extract_first()
            yield scrapy.Request(url, callback=self.parse_a_tab)


    def parse_a_tab(self, response):

        for item_page in response.xpath(".//li[contains(@id,'catList')]//a/@href").extract():
            yield scrapy.Request(item_page, callback=self.parse_list_of_product)


    def parse_list_of_product(self, response):

        for product in response.xpath('.//li[@class="list_product"]'):
            url = 'http://www.ernstings-family.de' + product.xpath('.//div[@class=\'product_basic_content\']/a[1]//@href').extract_first()

            yield scrapy.Request(url, callback=self.image_urls_parser)

    def image_urls_parser(self, response):

        p = Product()
        p['url'] = response.url
        p['actual_price'] = response.xpath(".//strike/text()").extract_first()
        p['discount_price'] = response.xpath("//*[@class='prd_price prd_new_price']/text()").extract_first()
        p['description'] = response.xpath(".//p[@class='infotext']/text()").extract()
        p['name'] = response.xpath(".//span[@class='prd_name']/text()[1]").extract_first()
        p['description'] = p['description'][2]
        imgs = []
        for img in response.xpath(".//div[@id='prd_thumbs']/a"):
            imgs.append(img.xpath("./img/@src").extract_first())


        p['image_urls'] = imgs
        p['skus'] = []
        color = response.xpath("//script[@type='text/javascript']/text()").re(r'"Farbe":\["(.*)"]')
        color = color[0]
        sizes =  response.xpath("//script[@type='text/javascript']/text()").re(r'"Größe":\["(.*)"],')
        sizes = sizes[0]
        sizes = sizes.split(',')
        for s in sizes:
            sku = StoreKeepingUnits()
            sku['actual_price'] = p['actual_price']
            sku['discount_price'] = p['discount_price']
            sku['colour'] = color
            sku['size'] = s #s.xpath("./span/text()") escaped for the time being because these things are rendering via javascript
            sku['sku_id'] = p['name'] + '_' + sku['size']
            p['skus'].append(sku)

        return p

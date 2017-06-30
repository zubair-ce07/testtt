import scrapy
from scrapy.spiders import Rule, CrawlSpider
from ernstingsfamily.items import Product, StoreKeepingUnits
from scrapy.linkextractors import LinkExtractor
import urllib

class ErnstingsFamilySpider(CrawlSpider):
    name = 'ernstings_family'
    allowed_domains = ['ernstings-family.de']
    start_urls = ['http://www.ernstings-family.de/']
    rules = (
        Rule(LinkExtractor(restrict_css="ul[id='navi_main'] > li > a")),
        Rule(LinkExtractor(restrict_css="li[id*='catList'] > a"), callback='parse_pagination', follow=True),
        Rule(LinkExtractor(restrict_css="div[class='product_basic_content'] > a"), callback='parse_detail'),
    )

    def parse_pagination(self, response):
        url = response.xpath("//script[@type='text/javascript']").re("endlessScrollingUrl': '(.*)'")
        limit = response.xpath(".//ul[@class='category_product_list']/@data-max-page").extract_first()
        url = urllib.parse.urljoin(self.start_urls[0], url[0][:-1])
        
        for index in range(int(limit)):
            yield scrapy.Request(url + str(index + 1), callback=self.parse_detail)




    def parse_detail(self, response):
        product_item = Product()
        product_item['url'] = self.get_url(response)
        product_item['actual_price'] = self.get_actual_price(response)
        product_item['discount_price'] = self.get_discount_price(response)
        product_item['description'] = self.get_description(response)
        product_item['name'] = self.get_name(response)
        product_item['image_urls'] = self.get_images(response)

        color = response.xpath("//script[@type='text/javascript']/text()").re(r'"Farbe":\["(.*)"]')
        color = color[0]
        sizes =  response.xpath("//script[@type='text/javascript']/text()").re(r'"Größe":\["(.*)"],')
        sizes = sizes[0]
        sizes = sizes.split(',')
        product_item['skus'] = self.get_skus(sizes, product_item, color)

        return product_item

    def get_url(self,response):
        return response.url

    def get_actual_price(self,response):
        return response.css("strike::text").extract_first()

    def get_discount_price(self, response):
        return response.css("span#prd_price::text").extract_first()

    def get_name(self, response):
        return response.css("span[class=prd_name]::text").extract_first()

    def get_description(self, response):
        return response.css("p[class=infotext]::text").extract()[2]

    def get_images(self, response):
        imgs = []
        for img in response.css("div[id=prd_thumbs] > a"):
            imgs.append(img.css("img::attr(src)").extract_first())

        return imgs

    def get_color(self, response):
        color= response.xpath("//script[@type='text/javascript']/text()").re(r'"Farbe":\["(.*)"]')
        return color[0]

    def get_sizes(self, response):
        sizes= response.xpath("//script[@type='text/javascript']/text()").re(r'"Größe":\["(.*)"],')
        return sizes[0]

    def get_skus(self, sizes, product_item,color):
        skus = []
        for s in sizes:
            sku = StoreKeepingUnits()
            sku['actual_price'] = product_item['actual_price']
            sku['discount_price'] = product_item['discount_price']
            sku['colour'] = color
            sku['size'] = s
            sku['sku_id'] = product_item['name'] + '_' + sku['size']
            skus.append(sku)

        return skus

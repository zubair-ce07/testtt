import scrapy
from scrapy.spiders import Rule, CrawlSpider
from ernstingsfamily.items import Product, StoreKeepingUnits
from scrapy.linkextractors import LinkExtractor


class ErnstingsFamilySpider(CrawlSpider):
    name = 'ernstings_family'
    allowed_domains = ['ernstings-family.de']
    start_urls = ['http://www.ernstings-family.de/']


    rules = (
        Rule(LinkExtractor(restrict_css="ul[id='navi_main'] > li > a")),
        Rule(LinkExtractor(restrict_css="li[id*='catList'] > a")),
        Rule(LinkExtractor(restrict_css="div[class='product_basic_content'] > a"),
             callback='get_complete_details_of_product')
    )

    def get_complete_details_of_product(self, response):
        product_item = Product()
        product_item['url'] = response.url
        product_item['actual_price'] = response.css("strike::text").extract_first()
        product_item['discount_price'] = response.css("span#prd_price::text").extract_first()
        product_item['description'] = response.css("p[class=infotext]::text").extract()[2]
        product_item['name'] = response.css("span[class=prd_name]::text").extract_first()
        imgs = []
        for img in response.css("div[id=prd_thumbs] > a"):
            imgs.append(img.css("img::attr(src)").extract_first())

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

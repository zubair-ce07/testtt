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
        Rule(LinkExtractor(restrict_css="li[id*='catList'] > a"), callback='lazy_parser'),

    )

    def lazy_parser(self, response):
        url = response.xpath("//script[@type='text/javascript']").re("endlessScrollingUrl': '(.*)'")
        limit = response.xpath(".//ul[@class='category_product_list']/@data-max-page").extract_first()
        url = self.start_urls[0] + url[0][:-1]
        urls = []
        for l in range(int(limit)):
            urls.append(url+str(l+1))

        for product in response.xpath('.//li[@class="list_product"]'):
            url = response.urljoin(product.xpath('.//div[@class=\'product_basic_content\']/a//@href').extract_first())
            urls.append(url)

        for u in urls:
            yield scrapy.Request(u, callback=self.parse_detail)

    def parse_detail(self, response):
        product_item = Product()
        product_item['url'] = self._get_url(response)
        product_item['actual_price'] = self._get_actual_price(response)
        product_item['discount_price'] = self._get_discount_price(response)
        product_item['description'] = self._get_description(response)
        product_item['name'] = self._get_name(response)
        product_item['image_urls'] = self._get_images(response)

        color = response.xpath("//script[@type='text/javascript']/text()").re(r'"Farbe":\["(.*)"]')
        color = color[0]
        sizes =  response.xpath("//script[@type='text/javascript']/text()").re(r'"Größe":\["(.*)"],')
        sizes = sizes[0]
        sizes = sizes.split(',')
        product_item['skus'] = self._get_skus(sizes, product_item, color)

        return product_item

    def _get_url(self,response):
        return response.url

    def _get_actual_price(self,response):
        return response.css("strike::text").extract_first()

    def _get_discount_price(self, response):
        return response.css("span#prd_price::text").extract_first()

    def _get_name(self, response):
        return response.css("span[class=prd_name]::text").extract_first()

    def _get_description(self, response):
        return response.css("p[class=infotext]::text").extract()[2]

    def _get_images(self, response):
        imgs = []
        for img in response.css("div[id=prd_thumbs] > a"):
            imgs.append(img.css("img::attr(src)").extract_first())

        return imgs

    def _get_color(self, response):
        color= response.xpath("//script[@type='text/javascript']/text()").re(r'"Farbe":\["(.*)"]')
        return color[0]

    def _get_sizes(self, response):
        sizes= response.xpath("//script[@type='text/javascript']/text()").re(r'"Größe":\["(.*)"],')
        return sizes[0]

    def _get_skus(self, sizes, product_item,color):
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

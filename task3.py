import scrapy


class ShoeInfo(scrapy.Item):
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    stock = scrapy.Field()
    color = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()


class AsicsSpider(scrapy.Spider):
    name = "asics"
    start_urls = [
        'https://www.asics.com/us/en-us/',
    ]

    def parse(self, response):

        for major_catg in response.css('li.nav-item > a')[0:3]:
            item = ShoeInfo()
            item['gender'] = major_catg.css('::text').extract_first()
            major_catg_url = major_catg.css('::attr(href)').extract_first()
            major_catg_url = response.urljoin(major_catg_url)

            yield scrapy.Request(url=major_catg_url, callback=self.extract_shoes, meta={'item': item})

    def extract_shoes(self, response):
        item = response.meta.get('item')

        for shoe in response.css('div.col-sm-4.col-xs-6.gridProduct.product.port'):
            item['name'] = shoe.css('p.prod-name::text').extract_first()
            item['category'] = [shoe.css('p.prod-classification-reference::text').extract_first()]
            item['url'] = shoe.css('a.productMainLink::attr(href)').extract_first()
            item['brand'] = "ASICS"

            shoe_url = shoe.css('a.productMainLink::attr(href)').extract_first()
            shoe_url = response.urljoin(shoe_url)
            yield scrapy.Request(url=shoe_url, callback=self.extract_shoe_info, meta={'item': item})

    def extract_shoe_info(self, response):
        item = response.meta.get('item')

        item['description'] = response.css('div.tabInfoChildContent.panel-collapse.collapse'
                                           '::text')[6:].extract_first()
        item['care'] = []
        item['image_urls'] = response.css('div.owl-carousel > img::attr(data-big)').extract()

        color = response.css('title::text').extract_first().split('|')[2]
        skus = {}
        for sku in response.css('div.size-select-list.clearfix > div.SizeOption.inStock'):
            one_sku = {
                sku.css('::attr(data-value)').extract_first():
                    {
                        'color': color,
                        'currency': sku.css('meta::attr(content)')[2].extract(),
                        'price': sku.css('meta::attr(content)')[3].extract()

                    }

            }
            skus.update(one_sku)

        item['skus'] = skus
        yield item

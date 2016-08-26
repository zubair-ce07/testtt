__author__ = 'sayyeda'


import re
from scrapy.spiders import Rule, CrawlSpider
from productspider.items import ProductSpiderItem
from scrapy.linkextractors import LinkExtractor


class AsicsSpider(CrawlSpider):
    name = 'asics_spider'
    allowed_domains = ["asics.com"]
    start_urls = ["http://www.asics.com/us/en-us/"]

    listings_xpath = [
        ".//*[@id='main-menu']//ul[contains(@class,'childLeafNode')]//li[contains(@class,'yCmsComponent')]//a",
        ".//*[contains(@class,'nm center')]/a"]

    product_listings = [".//*[contains(@class,'product-list')]/div/div/a"]

    # this is to get all the product listing including pagination.
    rules = [
        Rule(LinkExtractor(restrict_xpaths=listings_xpath), ),
        Rule(LinkExtractor(deny=["http://www.onitsukatiger.com/us/en-us/"],
                           restrict_xpaths=product_listings, ),
             callback="parse_product_details")
    ]

    def parse_product_details(self, response):  # Retrieving required product details.
        print("hello")
        garment = ProductSpiderItem()

        garment['spider_name'] = 'asics-us-crawl'
        garment['retailer'] = 'asics-us'

        garment['currency'] = 'USD'

        garment['price'] = response.xpath(".//*[contains(@class,'price')]/span//text()").extract()[-1].strip()

        garment['market'] = 'US'

        garment['category'] = response.xpath(
            "//*[contains(@id, 'breadcrumb')]/ul/li[not (@class='active')]/a[not(@href='/us/en-us/')]/span/text()").extract()

        garment['description'] = self.get_description(response)

        garment['url_original'] = response.url

        garment['brand'] = response.xpath(".//*[contains(@class,'singleProduct')]/meta[1]/@content").extract()[-1]

        garment['img_urls'] = self.get_img_urls(response)

        garment['skus'] = self.get_skus(response)

        name = response.xpath(".//*[contains(@class,'single-prod-title')]/text()").extract()[-1]
        if name:
            garment['name'] = name

        garment['url'] = response.url

        garment['gender'] = self.get_gender(garment['category'])

        yield garment


    def get_skus(self, response):
        skus = {}
        sel = response.xpath(".//*[contains(@id, 'SelectSizeDropDown')]/li[@class='SizeOption inStock']")

        for item in sel:
            sku_details = {}
            sku_details['currency'] = item.xpath("meta[3]/@content").extract()
            sku_details['price'] = item.xpath("meta[4]/@content").extract()[0]
            size_ = item.xpath("a/text()").extract()[0]
            size = ' '.join(size_.split())
            sku_details['size'] = size

            current_color = response.xpath(".//*[contains(@class,'border')]/text()").extract()[0].strip()
            color = re.split(':', current_color)
            if color:
                sku_details['color'] = color[1].strip()

            prev_price = response.xpath(".//*[contains(@class,'markdown')]/del/text()").extract()
            if prev_price:
                sku_details['previous price'] = response.xpath(".//*[contains(@class,"
                                                               " 'markdown' )]/del/text()").extract()[0]
            sku_details['out_of_stock'] = 'false'
            skus[item.xpath("meta[1]/@content").extract()[0]] = sku_details
        return skus


    def get_img_urls(self, response):  # getting image-URLS
        url_list = []

        sel = response.xpath(".//*[contains(@id,'product-image-0')]")
        for items in sel:
            first_img_link = items.xpath("./@data-big").extract()[0]
            sec_img_link = items.xpath("./@data-rstmb").extract()[0]
            img_src = items.xpath("./@src").extract()[0]
            img_urls = [first_img_link, sec_img_link, img_src]
            url_list = img_urls
        return url_list


    def get_gender(self, category_list):
        gender_ = ''
        for item in category_list:
            if 'men' in item:
                gender_ = 'Male'

            if 'women' in item:
                gender_ = 'Female'

            if not ('men' in item and 'women' in item):
                gender_ = 'Unisex'

            if 'kids' in item:
                gender_ = 'Children'
        return gender_


    def get_description(self, response):    # Retrieving given description of product.
        desc = response.xpath(".//*[contains(@class,'tabInfoChildContent')]/text()").extract()
        desc_ = []
        for item in desc:
            if not item.isspace():
                desc_.append(item.strip())

        return desc_






















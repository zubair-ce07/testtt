
import scrapy
import json
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from jackwills.items import JackwillsItem


class JackwillsSpider(CrawlSpider):
    name = "jackwill_spider"
    allowed_domains = ["jackwillsoutlet.com"]
    start_urls = ["http://www.jackwillsoutlet.com/"]

    category_listing = [".//div[@class='wrapper pt_storefront']//li[contains(@class,'level')]//li",
                        ".//a[@class='page-next']"]
    product_listing = ["//*[@class='product-name']/h2"]

    # this is to get all the product listing including pagination.
    rules = [Rule(LinkExtractor(restrict_xpaths=category_listing), ),
             Rule(LinkExtractor(restrict_xpaths=product_listing), callback="parse_product_details"), ]

    # Retrieving required product details.
    def parse_product_details(self, response):
        garment = JackwillsItem()

        garment['url'] = response.url
        garment['currency'] ='GBP'
        garment['outlet'] = 'true'
        garment['market'] = 'UK'
        garment['retailer'] = 'jackwills'
        garment['spider_name'] = 'jackwills-crawl'
        garment['image_urls'] = self.product_image_urls(response)
        garment['name'] = response.xpath("//h1[@class='product-name']/text()").extract()[-1].strip()
        garment['price'] = response.xpath("//div[@id='product-content']//span[@class='price-sales']/text()").extract()[0]
        garment['category'] = response.xpath("//ol[@class='breadcrumb']/li/a[not(@href='http://www.jackwillsoutlet.com')]/text()").extract()
        garment['url_original'] = response.url
        garment['brand'] = 'Jack Wills'
        garment['retailer_sku']= response.xpath("//div[@class='product-number']/text()").extract()[0].strip()
        garment['skus'] = self.product_skus(response)
        garment['description'] = response.xpath(".//h3[contains(@class, 'prod-short-desc')]/following::div[1]/p/text()").extract()
        garment['care'] = self.product_care(response)
        garment['gender'] = self.product_gender(garment['category'])
        more_colors = self.get_colors(response)

        return self.parse_color_requests(more_colors, garment)

    def get_sku_elements(self, response):
        sku_details = {}
        sku_details['previous_prices'] = response.xpath("//div[@id='product-content']//span[@class='price-standard']/text()").extract()
        sku_details['color'] = response.xpath("//span[@class='selectedColor']/text()").extract()[0]
        sku_details['price'] = response.xpath("//div[@id='product-content']//span[@class='price-sales']/text()").extract()[0]
        sku_details['currency'] = 'GBP'
        return sku_details

    # getting skus of all colors & sizes.
    def product_skus(self, response):
        selectable_sizes = response.xpath("//li[@class='attribute size-attr']/div/ul/li[@class='emptyswatch' or @class='selected']/a/text()").extract()
        unselectable_sizes = response.xpath("//li[@class='attribute size-attr']/div/ul/li[@class='emptyswatch unselectable']/a/text()").extract()

        color = response.xpath("//span[@class='selectedColor']/text()").extract()[0]
        skus = {}
        sku_elements = self.get_sku_elements(response)
        for sizes in selectable_sizes:
                sku_details = sku_elements
                sku_details['size'] = sizes.strip()
                sku_key = color+'_'+ sizes.strip()
                skus[sku_key] = sku_details

        for sizes in unselectable_sizes:
                sku_details = sku_elements
                sku_details['size'] = sizes.strip()
                sku_details['out_of_stock'] = 'true'
                sku_key = color+'_'+ sizes.strip()
                skus[sku_key] = sku_details

        return skus

    # getting care cautions of products
    def product_care(self,response):
        care_field_paths = ["//h3[contains(@class, 'prod-care')]/following::div[1]/li/text()",
                            "//h3[contains(@class, 'prod-care')]/following::div[1]/ul/li/text()",
                            "//h3[contains(@class, 'prod-care')]/following::div[1]/p/text()"]
        return [response.xpath(path).extract()[0] for path in care_field_paths if response.xpath(path).extract()]

    def product_image_urls(self,response):
        image_field = response.xpath(".//img[@class='productthumbnail']/@data-lgimg").extract()
        image_urls = []
        for item in image_field:
            image_dict = json.loads(item)
            image_urls.append(image_dict['url'])
        return image_urls

    # getting all colors of a product.
    def get_colors(self, response):
        color_links = response.xpath(".//ul[contains(@class, 'swatches Color clearfix')]/li[not (@class='selected-value')]/a/@href").extract()
        if color_links:
            color_links.pop(0)
        return color_links

    # adding a sku of different color of same product.
    def parse_color_requests(self, more_colors, item):
        if more_colors:
            full_url = more_colors.pop(0)
            req = scrapy.Request(full_url, callback=self.product_color_sku,
                                 meta={'item': item, 'urls': more_colors})
            yield req
        else:
            yield item


    def product_color_sku(self, response):
        item = response.meta["item"]
        urls = response.meta["urls"]
        images = response.xpath(".//img[@class='productthumbnail']/@data-lgimg").extract()
        item['image_urls'].extend(images)
        item['skus'].update(self.product_skus(response))
        return self.parse_color_requests(urls, item)

    def product_gender(self, category_list):
        gender_dict = {'Gentlemen': 'men', 'Ladies': 'women'}
        gender_ = ''

        for item in category_list:
            if item in gender_dict:
                gender_ = gender_dict[item]
            else:
                gender_ = 'unisex adults'

        return gender_








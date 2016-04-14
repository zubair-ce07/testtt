import scrapy
from scrapy import Request

from bluefly.items import BlueflyItem


class BlueflySpider(scrapy.Spider):
    name = "bluefly"
    allowed_domains = ["bluefly.com"]
    start_urls = [
        "http://www.bluefly.com/"
    ]

    def parse(self, response):
        for href in response.xpath('//*[@class="sitenav-sub-column"]//li//@href'):
            url = response.urljoin(href.extract())
            yield Request(url, callback=self.parse_product_list)

    def parse_product_list(self, response):
        for href in response.xpath('//li[@class="mz-productlist-item"]//@href'):
            url = response.urljoin(href.extract())
            yield Request(url, callback=self.parse_product_details)
        next_page = response.xpath('//*[@class="mz-pagenumbers-next"]/@href').extract()
        if next_page:
            next_page_url = response.urljoin(next_page[0])
            yield Request(next_page_url, callback=self.parse_product_list)

    def parse_product_details(self, response):
        item = BlueflyItem()
        item['brand'] = self.get_brand(response)
        item['name'] = self.get_name(response)
        item['details'] = self.get_details(response)
        item['merch_info'] = self.get_merch_info(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['image_urls'] = response.xpath('//*[@class="mz-productimages-thumbs"]//@src').extract()
        item['category'] = response.xpath('//*[@class="mz-breadcrumb-link"]/text()').extract()
        item['url'] = response.url
        item['url_original'] = response.url
        item['retailer'] = self.name
        item['skus'] = self.skus(response)
        return item

    def get_brand(self, response):
        brand = response.xpath('//*[@itemprop="brand"]/a/text()').extract()
        if brand:
            brand = brand[0]
            return brand
        return ''

    def get_name(self, response):
        name = response.xpath('//*[@class="mz-breadcrumb-current"]/text()').extract()[0]
        name = name.replace(self.get_brand(response), '')
        return name

    def get_retailer_sku(self, response):
        retailer_sku = response.xpath('//*[@itemprop="productID"]/text()').extract()[0]
        retailer_sku = retailer_sku.replace('Style # ', '')
        return retailer_sku

    def get_merch_info(self, response):
        merch_info = response.xpath('//*[@class="mz-price-message"]/text()').extract()
        if merch_info:
            merch_info[0] = merch_info[0].strip()
            return merch_info
        return ''

    def get_details(self, response):
        description = response.xpath('//*[@itemprop="description"]/text()').extract()
        details = response.xpath('//*[@class="mz-productdetail-props"]/li/text()').extract()
        return description + details

    def skus(self, response):
        skus = {}
        colour = response.xpath('//*[@itemprop="color"]/text()').extract()
        previous_prices = self.get_previous_prices(response)
        sizes = response.xpath('//*[@class="mz-productoptions-valuecontainer"]/*/text()').extract()
        price = self.get_price(response)
        for size in sizes:
            sku = {}
            sku['colour'] = colour[0]
            if previous_prices:
                sku['previous_prices'] = [previous_prices]
            sku['price'] = price
            sku['currency'] = 'USD'
            sku['size'] = size
            skus[size] = sku
        return skus

    def get_price(self, response):
        price = response.xpath('//*[@itemprop="priceSpecification"]/div[1]/text()').extract()
        if price:
            price = price[0].strip().replace('$', '')
            return price
        return ''

    def get_previous_prices(self, response):
        p_prices = response.xpath('//*[@class="mz-price is-crossedout"]//text()').extract()
        if p_prices:
            p_prices = p_prices[0].strip().replace('Retail: $', '')
            return p_prices
        return ''

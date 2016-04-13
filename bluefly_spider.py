import scrapy
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
            # print url
            yield scrapy.Request(url, callback=self.parse_product_list)

    def parse_product_list(self, response):
        for href in response.xpath('//li[@class="mz-productlist-item"]//@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_product_details)
        next_page = response.xpath('(//*[@class="mz-pagenumbers-next"])[1]/@href').extract()
        if next_page:
            next_page_url = response.urljoin(next_page[0])
            yield scrapy.Request(next_page_url, callback=self.parse_product_list)

    def parse_product_details(self, response):
        item = BlueflyItem()
        item['brand'] = response.xpath('//*[@itemprop="brand"]/a/text()').extract()
        item['name'] = response.xpath('//*[@class="mz-breadcrumb-current"]/text()').extract()
        item['description'] = response.xpath('//*[@itemprop="description"]/text()').extract()
        item['details'] = response.xpath('//*[@class="mz-productdetail-props"]/li/text()').extract()
        item['merch_info'] = response.xpath('//*[@class="mz-price-message"]/text()').extract()
        item['image_urls'] = response.xpath('//*[@class="mz-productimages-thumbs"]//*//*//@src').extract()
        item['category'] = response.xpath('//*[@class="mz-breadcrumb-link"]/text()').extract()
        item['url'] = response.url
        item['url_original'] = response.url
        item['retailer'] = self.name
        item['skus'] = self.skus(response)
        return item

    def skus(self, response):
        skus = dict()
        color = response.xpath('//*[@itemprop="color"]/text()').extract()
        previous_prices = response.xpath('//*[@class="mz-price is-crossedout"]//text()').extract()
        if previous_prices:
            previous_prices = previous_prices[0].strip()
        size = response.xpath('//*[@class="mz-productoptions-valuecontainer"]/*/text()').extract()
        prices = response.xpath('//*[@itemprop="priceSpecification"]/div[1]/text()').extract()
        if prices:
            prices = prices[0].strip()
        for s in size:
            sku = dict()
            sku['color'] = color
            sku['previous_prices'] = previous_prices
            sku['prices'] = prices
            sku['size'] = s
            skus[s] = sku
        return skus

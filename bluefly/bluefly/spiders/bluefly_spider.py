import scrapy
from bluefly.items import BlueflyItem


class BlueflySpiderSpider(scrapy.Spider):
    name = "bluefly_spider"
    allowed_domains = ["bluefly.com"]
    start_urls = [
        'http://www.bluefly.com/hayden-purple-cashmere-turtleneck-sweater/p/351480403',
    ]

    def parse(self, response):
        item = BlueflyItem()
        item['brand'] = response.xpath("//*[contains(@class, 'mz-productbrand')]/a/text()").extract()
        item['category'] = response.xpath("//*[contains(@class, 'mz-breadcrumbs')]/a[position()>1]/text()").extract()
        item['description'] = self.get_item_description(response)
        item['gender'] = 'women'
        item['image_urls'] = response.xpath('//*[contains(@class, "mz-productimages-thumbimage")]//@src').extract()
        item['market'] = 'US'
        item['merch_info'] = map(unicode.strip,
                                 response.xpath('//*[contains(@class, "mz-price-message")]//text()').extract())
        item['name'] = \
            response.xpath("//*[contains(@class, 'mz-breadcrumb-current')]//text()").extract()[0].split(' ', 1)[1]
        item['retailer'] = map(unicode.strip,
                               response.xpath('//*[contains(@class, "site-toggler bluefly active")]//text()').extract())
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['skus'] = self.get_retailer_sku(response)
        item['url'] = response.url
        item['url_original'] = response.url
        yield item

    def extract_retailer_sku(self, response):
        retailer_sku = response.xpath("//*[contains(@class, 'mz-productdetail-props')]/li[last()]/text()").extract()
        return (retailer_sku[0].split())[-1]

    def get_item_description(self, response):
        description = response.xpath("//*[contains(@class, 'mz-productdetail-description')]//text()").extract()
        detail = response.xpath(
            "//*[contains(@class, 'mz-productdetail-props')]/li[position()<last()]/text()").extract()
        return description + detail

    def get_retailer_sku(self, response):
        skus = {}
        sizes = response.xpath("//*[contains(@class, 'mz-productoptions-valuecontainer')]//span/text()").extract()
        index = 0
        for size in sizes:
            product = {}
            product['color'] = response.xpath(
                "//*[contains(@class, 'mz-productoptions-optionvalue')]//text()").extract()
            product['currency'] = 'USD'
            prev_price = \
            map(unicode.strip, response.xpath("//*[contains(@class, 'mz-price is-crossedout')]//text()").extract())[-1]
            product['previous_prices'] = prev_price[1:]
            price = map(unicode.strip,
                        response.xpath("//*[contains(@class, 'mz-price is-saleprice')]//text()").extract())[0]
            product['price'] = price[1:]
            product['size'] = size
            skus[index] = product
            index += 1
        return skus
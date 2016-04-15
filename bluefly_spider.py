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
        item['description'] = self.get_description(response)
        item['merch_info'] = self.get_merch_info(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['image_urls'] = self.get_image_urls(response)
        item['category'] = self.get_category(response)
        item['gender'] = self.get_gender(response)
        item['url'] = response.url
        item['url_original'] = response.url
        item['retailer'] = self.name
        item['skus'] = self.skus(response)
        return item

    def get_category(self, response):
        return response.xpath('//*[@class="mz-breadcrumb-link"]/text()').extract()

    def get_image_urls(self, response):
        urls = response.xpath('//*[@class="mz-productimages-thumbs"]//@src').extract()
        img_url = []
        for url in urls:
            img_url.append(url.split('?')[0])
        return img_url

    def get_brand(self, response):
        brand = response.xpath('//*[@itemprop="brand"]/a/text()').extract()
        return brand[0] if brand else ''

    def get_name(self, response):
        name = response.xpath('//*[@class="mz-breadcrumb-current"]/text()').extract()[0]
        return name.replace(self.get_brand(response), '').strip()

    def get_retailer_sku(self, response):
        retailer_sku = response.xpath('//*[@itemprop="productID"]/text()').extract()[0]
        return retailer_sku.replace('Style # ', '')

    def get_merch_info(self, response):
        merch_info = response.xpath('//*[@class="mz-price-message"]/text()').extract()
        return [merch_info[0].strip()] if merch_info else []

    def get_description(self, response):
        description = response.xpath('//*[@itemprop="description"]/text()').extract()
        details = response.xpath('//*[@class="mz-productdetail-props"]/li/text()').extract()
        return description + details

    def get_gender(self, response):
        gender_list = ['Women', 'Men', 'Kids', 'Girls', ' Boys']
        category = self.get_category(response)
        for gender in category:
            return gender if gender in gender_list else 'unisex-adults'

    def skus(self, response):
        skus = {}
        colour = response.xpath('//*[@itemprop="color"]/text()').extract()
        previous_prices = self.get_previous_prices(response)
        price = self.get_price(response)
        sizes = response.xpath('//*[@class="mz-productoptions-valuecontainer"]/*/text()').extract()
        if sizes:
            data_value = response.xpath('//@data-value').extract()
            index = 0
            for size in sizes:
                sku = {}
                sku['colour'] = colour[0]
                if previous_prices:
                    sku['previous_prices'] = [previous_prices]
                sku['price'] = price
                sku['currency'] = 'USD'
                sku['size'] = size
                skus[data_value[index]] = sku
                index += 1
        else:
            skus['colour'] = colour[0]
            if previous_prices:
                skus['previous_prices'] = [previous_prices]
            skus['price'] = price
            skus['currency'] = 'USD'
        return skus

    def get_price(self, response):
        price = response.xpath('//*[@class="mz-price"]/text()|//*[@itemprop="price"]/text()').extract()
        return price[0].strip().replace('$', '') if price else ''

    def get_previous_prices(self, response):
        p_prices = response.xpath('//*[@class="mz-price is-crossedout"]//text()').extract()
        return p_prices[0].strip().replace('Retail: $', '') if p_prices else ''

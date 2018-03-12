import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
import re
import queue


class OrsaySpider(CrawlSpider):
    name = "orsay-de-crawl"
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com']

    rules = (
        Rule(LinkExtractor(restrict_css=(['#nav a:only-child', '.pagination .arrow .next']))),
        Rule(LinkExtractor(restrict_css=('.category-products .product-image-wrapper a:first-of-type')),
             callback='parse_detail'),
    )

    def parse_detail(self, response):
        img_urls = []
        skus = {}
        img_urls, skus = self.scrap_image_skus(response, img_urls, skus)
        color_urls = self.get_color_urls(response)
        url_queue = queue.Queue(maxsize=len(color_urls) + 1)
        retailor_sk = ""
        if img_urls:
            retailor_sk = (str(img_urls[0]).split("/")[-1]).split("_")[0]
        data = {
                "retailor_sk": retailor_sk,
                "image_urls": img_urls,
                "skus": skus,
                "spider_name": OrsaySpider.name,
                "retailer": "orsay-de",
                "currency": self.get_currency(response),
                "market": 'DE',
                "catagory": self.get_category(response),
                "price": self.get_price(response),
                "description": self.get_description(response),
                "brand": "Orsay",
                "care": self.get_care(response),
                "lang": self.get_language(response),
                "name": self.get_name(response),
                "url": response.url,
                "crawler_start_time": self.crawler.stats.get_value('start_time'),
            }

        for url in color_urls:
            url_queue.put_nowait(url)

        if url_queue.empty():
            yield data

        else:
            url = url_queue.get()
            request = scrapy.Request(url=url, callback=self.parse_images_and_skus)
            request.meta['url_queue'] = url_queue
            request.meta['data'] = data
            yield request

    def parse_images_and_skus(self, response):
        data = response.meta['data']
        data['image_urls'], data['skus'] = self.scrap_image_skus(response, data['image_urls'], data['skus'])
        url_queue = response.meta['url_queue']
        if not url_queue.empty():
            url = url_queue.get()
            request = scrapy.Request(url=url, callback=self.parse_images_and_skus)
            request.meta['data'] = data
            request.meta['url_queue'] = url_queue
            yield request
        else:
            yield data

    # scrap image urls and skus form given response,add them to img-urls
    # and skus given as paramters and return modified values
    def scrap_image_skus(self, response, img_urls, skus):
        sku_id = response.css('input#sku::attr(value)').extract_first()
        color = response.css('input#color-field::attr(value)').extract_first()
        price = response.css('.product-main-info  .price::text').extract_first().split()[0]
        currency = response.css('.sizebox-wrapper::attr(data-currency)').extract_first()
        img_urls += response.css('#product_media a::attr(href)').extract()

        if currency == '€':
            currency = "EUR"
        all_size = response.css('.sizebox-wrapper li::text').extract()
        sizes = []

        for item in all_size:
            size_str = re.findall("[a-zA-Z]+", item)
            if size_str:
                sizes.append(size_str[0])
        sizes_quantity = response.css('.sizebox-wrapper li::attr(data-qty)').extract()
        sizes_price = response.css('.sizebox-wrapper li::attr(data-price)').extract()

        if sizes:
            for size, quantity, size_price in zip(sizes, sizes_quantity, sizes_price):
                size_item = {'currency': currency, 'colour': color, 'size': size}
                if float(size_price):
                    size_item['price'] = float(size_price)
                else:
                    size_item['price'] = price
                if not int(quantity):
                    size_item['out_of_stock'] = True
                skus["{}_{}".format(sku_id, size)] = size_item
        else:
            item = {'currency': currency, 'colour': color, 'price': price}
            skus[sku_id] = item
        return img_urls, skus

    def get_price(self, response):
        return response.css('.product-main-info  .price::text').extract_first().split()[0]

    def get_currency(self, response):
        return response.css('.sizebox-wrapper::attr(data-currency)').extract_first()

    def get_color_urls(self, response):
        return response.css('.product-colors>li:not(.active)>a::attr(href)').extract()

    def get_description(self, response):
        return " ".join((response.css('.description::text').extract_first()).split())

    def get_category(self, response):
        return response.css('.breadcrumbs a::text').extract()

    def get_care(self, response):
        return response.css('.product-care .material::text').extract() + \
               response.css('.product-care img::attr(src)').extract()

    def get_language(self, response):
        return response.css('html::attr(lang)').extract_first()

    def get_name(self, response):
        return response.css('.product-main-info .product-name::text').extract_first()


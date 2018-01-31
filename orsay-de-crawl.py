import scrapy
import re
import queue


class OrsaySpider(scrapy.Spider):
    name = "orsay-de-crawl"
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com']

    def parse(self, response):
        all_urls = response.css('ul#nav li a:only-child::attr(href)').extract()
        for url in all_urls:
            yield scrapy.Request(url=url, callback=self.page_parse)

    def page_parse(self, response):
        product_urls = response.css('div.category-products article div.product-image-wrapper '
                                    'a:first-of-type::attr(href)').extract()
        for url in product_urls:
            yield scrapy.Request(url=url, callback=self.detail_parse)
        next_page = response.css('ul.pagination li.arrow a.next::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.page_parse)

    def detail_parse(self, response):
        img_urls = []
        skus = {}
        price = response.css('div.product-main-info  span.price::text').extract_first().split()[0]
        currency = response.css('div.sizebox-wrapper::attr(data-currency)').extract_first()
        img_urls, skus = self.scrap_image_skus(response, img_urls, skus)
        color_urls = response.css('ul.product-colors>li:not(.active)>a::attr(href)').extract()
        url_queue = queue.Queue(maxsize=len(color_urls)+1)
        sk = ""
        if img_urls:
            sk = (str(img_urls[0]).split("/")[-1]).split("_")[0]
        data = {
                "retailor_sk": sk,
                "image_urls": img_urls,
                "skus": skus,
                "spider_name": OrsaySpider.name,
                "retailer": "orsay-de",
                "currency": currency,
                "market": 'DE',
                "catagory": response.css('ul.breadcrumbs>li>a::text').extract(),
                "price": price,
                "description": " ".join((response.css('p.description::text').extract_first()).split()),
                "brand": "Orsay",
                "care": response.css('div.product-care>p.material::text').extract() +
                response.css('div.product-care>ul>li>img::attr(src)').extract(),
                "lang": response.css('html::attr(lang)').extract_first(),
                "name": response.css('div.product-main-info h1.product-name::text').extract_first(),
                "url": response.url,
                "crawler_start_time": self.crawler.stats.get_value('start_time'),
            }

        for url in color_urls:
            url_queue.put_nowait(url)

        if url_queue.empty():
            yield data

        else:
            url = url_queue.get()
            request = scrapy.Request(url=url, callback=self.datail_color_parse)
            request.meta['url_queue'] = url_queue
            request.meta['data'] = data
            yield request

    def datail_color_parse(self, response):
        data = response.meta['data']
        img_urls = data['image_urls']
        skus = data['skus']
        img_urls, skus = self.scrap_image_skus(response, img_urls, skus)
        data['image_urls'] = img_urls
        data['skus'] = skus
        url_queue = response.meta['url_queue']
        if not url_queue.empty():
            url = url_queue.get()
            request = scrapy.Request(url=url, callback=self.datail_color_parse)
            request.meta['img_urls'] = img_urls
            request.meta['data'] = data
            yield request
        else:
            yield data

    # scrap image urls and skus form given response,add them to img-urls
    # and skus given as paramters and return modified values
    def scrap_image_skus(self, response, img_urls, skus):
        sku = response.css('input#sku::attr(value)').extract_first()
        color = response.css('input#color-field::attr(value)').extract_first()
        price = response.css('div.product-main-info  span.price::text').extract_first().split()[0]
        currency = response.css('div.sizebox-wrapper::attr(data-currency)').extract_first()
        img_urls += response.css('div#product_media a::attr(href)').extract()

        if currency == '€':
            currency = "EUR"
        all_size = response.css('.sizebox-wrapper li::text').extract()
        sizes = []

        for item in all_size:
            b = re.findall("[a-zA-Z]+", item)
            if b:
                sizes.append(b[0])
        sizes_quantity = response.css('div.sizebox-wrapper li::attr(data-qty)').extract()
        sizes_price = response.css('div.sizebox-wrapper li::attr(data-price)').extract()

        for size, quantity, size_price in zip(sizes, sizes_quantity, sizes_price):
            size_item = {'currency': currency, 'colour': color, 'size': size}
            if float(size_price):
                size_item['price'] = float(size_price)
            else:
                size_item['price'] = price
            if int(quantity) == 0:
                size_item['out_of_stock'] = True
            skus[sku + "_" + size] = size_item
        return img_urls, skus
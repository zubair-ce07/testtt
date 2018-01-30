import scrapy
import re
import queue


class OrsaySpider(scrapy.Spider):
    name = "orsay-de-crawl"
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/jersey-t-shirt-mit-volant-10308898.html']

    def datail_color_parse(self, response):
        sku = response.css('input#sku::attr(value)').extract_first()
        color = response.css('input#color-field::attr(value)').extract_first()
        price = response.css('div.product-main-info  span.price::text').extract_first().split()[0]
        currency = response.css('div.sizebox-wrapper::attr(data-currency)').extract_first()
        img_urls = response.meta['img_urls']
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
        skus = response.meta['skus']
        for size, quantity, size_price in zip(sizes, sizes_quantity, sizes_price):
            size_item = {'currency': currency, 'colour': color, 'size': size}
            if float(size_price):
                size_item['price'] = float(size_price)
            else:
                size_item['price'] = price
            if int(quantity) == 0:
                size_item['out_of_stock'] = True
            skus[sku + "_" + size] = size_item
        url_queue = response.meta['url_queue']
        if not url_queue.empty():
            url = url_queue.get()
            request = scrapy.Request(url=url, callback=self.datail_color_parse)
            request.meta['skus'] = skus
            request.meta['url_queue'] = url_queue
            request.meta['img_urls'] = img_urls
            yield request
        else:
            if img_urls:
                sk = (str(img_urls[0]).split("/")[-1]).split("_")[0]
            yield {
                "retailor_sk":sk,
                "skus":skus,
                "image_urls": img_urls,
            }

    def parse(self, response):
        img_urls = []
        skus = {}
        price = response.css('div.product-main-info  span.price::text').extract_first().split()[0]
        currency = response.css('div.sizebox-wrapper::attr(data-currency)').extract_first()
        color_urls = response.css('ul.product-colors>li:not(.active)>a::attr(href)').extract()
        url_queue = queue.Queue(maxsize=len(color_urls)+1)
        url_queue.put_nowait(response.url)
        for url in color_urls:
            url_queue.put_nowait(url)
        if not url_queue.empty():
            url = url_queue.get()
            request = scrapy.Request(url=url, callback=self.datail_color_parse)
            request.meta['skus'] = skus
            request.meta['url_queue'] = url_queue
            request.meta['img_urls'] = img_urls
            yield request

        yield {
            "spider_name":  OrsaySpider.name,
            "retailer": "orsay-de",
            "currency": currency,
            "market": 'DE',
            "catagory": response.css('ul.breadcrumbs>li>a::text').extract(),
            "price":  price,
            "description": " ".join((response.css('p.description::text').extract_first()).split()),
            "brand": "Orsay",
            "care": response.css('div.product-care>p.material::text').extract() +
            response.css('div.product-care>ul>li>img::attr(src)').extract(),
            "lang": response.css('html::attr(lang)').extract_first(),
            "name": response.css('div.product-main-info h1.product-name::text').extract_first(),
            "url": response.url,
            "crawler_start_time" : self.crawler.stats.get_value('start_time'),
        }


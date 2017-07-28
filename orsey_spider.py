import scrapy
from product_item import ChildProduct
from product_item import Count
from product_item import GrandChildProduct
from product_item import Product
from  scrapy.http import Request


class OrseySpider(scrapy.Spider):
    name = 'orsay.com'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de', ]
    urls = []

    def parse(self, response):
        #category links
        for href in response.css('span.widget.widget-category-link a::attr(href)'):
            yield response.follow(href, self.parse)
        #extra links
        for href in response.css('ul#nav a::attr(href)'):
            yield response.follow(href, self.parse)
        #product_links
        for href in response.css('h2.product-name a::attr(href)'):
            yield response.follow(href, self.parse_product)

    def parse_product(self, response):
        item = Product()
        child_item = ChildProduct()
        grand_child_item = GrandChildProduct()
        counter = Count()
        if "item" in response.meta.keys():
            counter = response.meta['counter']
            counter['counter'] -= 1
            item = response.meta['item']
            item['image_urls'].append(response.css('a[data-zoom-id^=mainZoom]::attr(href)').extract_first())
            child_item = item['skus']
            key_item = child_item['items']
            sku_key = key_item.keys().pop(0)
            grand_child_item = key_item[sku_key]
            grand_child_key_item = grand_child_item['items']
            grand_child_key_item['colour'].append(
                response.css('div.no-display input[name^=color]::attr(value)').extract_first())
            if not counter['counter']:
                yield item
        else:
            sizes = []
            key_part = response.css('div.twelve.columns label[for^="sku"]+input::attr(value)').extract_first()
            items_for_grand_child = dict(
                colour=response.css('div.no-display input[name^=color]::attr(value)').extract(),
                currency="Euro",
                price=response.css('div.product-view span.price::text').extract_first()
            )
            if response.css('script[type="application/ld+json"]::text').extract_first().find("OutOfStock") > 0:
                items_for_grand_child['OutOfStock'] = "True"
            for size in response.css('div.sizebox-wrapper li::text').extract():
                sizes.append(size.strip('\n').strip(' '))
            sizes_of_item = filter(None, sizes)
            items_for_child = dict()
            for size in sizes_of_item:
                key = "{0}_{1}".format(key_part, size)
                items_for_grand_child['size'] = size
                grand_child_item['items'] = items_for_grand_child
                items_for_child[key] = grand_child_item
            child_item['items'] = items_for_child
            item['brand'] = "orsay"
            item['care'] = response.css('ul.caresymbols img::attr(src)').extract()
            item['category'] = response.css('div.no-display input[name^=category_name]::attr(value)').extract_first()
            item['description'] = response.css('p.description::text').extract()
            item['gender'] = "women"
            item['image_urls'] = [response.css('a[data-zoom-id^=mainZoom]::attr(href)').extract_first()]
            item['name'] = response.css('h1.product-name::text').extract()
            item['retailer_sku'] = response.css('p.sku::text').extract_first().split(':')[1].strip(' ')[:6]
            item['skus'] = child_item
            item['url'] = response.url
            item['url_original'] = response.url
            self.urls = response.css('ul.product-colors  a::attr(href)').extract()
            self.urls.remove('#')
            counter['counter'] = len(self.urls)
        for next_color_page in self.urls:
            self.urls = filter(lambda a: a != next_color_page, self.urls)
            if next_color_page is not None and next_color_page is not "#":
                request = Request(next_color_page, callback=self.parse_product, dont_filter=True)
                request.meta['item'] = item
                request.meta['counter'] = counter
                yield request

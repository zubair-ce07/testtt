# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from jackjone.items import JackjoneItem

class JackjoneComSpider(Spider):
    name = 'jackjones.com'
    start_urls = ['https://www.jackjones.com/gb/en/']

    def parse(self, response):
        category_links = response.xpath("//a[contains(@class, 'category-top-navigation__title')]/@href").extract()[:-2]
        for link in category_links:
            yield Request(link, self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath("//a[contains(@class, 'thumb-link')]/@href").extract()
        for link in product_links:
            yield Request(link, self.parse_product_details, dont_filter=True)

        next_page = response.xpath("//a[@rel='next']/@data-href").extract_first()
        if next_page:
            yield Request(next_page, self.parse_product_links, dont_filter=True)

    def parse_product_details(self, response):
        product = JackjoneItem()
        product['url'] = response.url
        product['pid'] = response.xpath("//input[@id='pid']/@value").extract_first()
        product['article_number'] = response.xpath('//form[@data-articlenumber]/@data-articlenumber').extract_first()
        product['name'] = response.xpath("//h1[@class='product-name--visible']/text()").extract_first()
        category = response.xpath("//div[@class='breadcrumb']/a/text()").extract()
        if category:
            product['category'] = category[0]
            product['subcategory'] = category[1:]
        product['description'] = response.xpath("//meta[@name='description']/@content").extract_first()
        product['attributes'] = self.get_item_attributes(response)
        product['images'] = []
        color_urls = response.xpath("//ul[@class='swatch colorpattern']/li[@class='js-swatch-item swatch__item--selectable-colorpattern']/a/@data-href").extract()
        currency = response.xpath("//meta[@property='og:price:currency']/@content").extract_first()
        meta_dict = {'currency':currency,
         'product':product,
         'color_urls':color_urls,
         'skus':{}}
        yield Request(url=response.url, callback=self.get_sku_attribute_color, meta=meta_dict, dont_filter=True)

    def get_item_attributes(self, response):
        attributes = {}
        fabric = response.xpath("//li[contains(@class,'pdp-description__text__value--fabric')]/text()").extract_first()
        if fabric:
            attributes['fabric'] = fabric.strip()
        care = response.xpath("//li[@class='pdp-description__list__item']/text()").extract()
        if care:
            attributes['care'] = [c.strip() for c in care]
        return attributes

    def get_sku_attribute_color(self, response):
        color = response.xpath("//li[contains(@class, 'swatch__item--selected-colorpattern')]/a/span/text()").extract_first()
        product = response.meta.get('product')
        product['images'].extend(response.xpath("//div[@class='product-images__thumbnails__underlay']/img/@data-src").extract())
        size_urls = response.xpath("//ul[@class='swatch size']/li/a/@data-href").extract()
        sizes = response.xpath("//ul[@class='swatch size']/li/a/div/text()").extract()
        first_size = size_urls[0]
        size_urls = size_urls[1:]
        meta_dict = {'currency':response.meta.get('currency'),
         'product':product,
         'color_urls':response.meta.get('color_urls'),
         'skus':response.meta.get('skus'),
         'size_urls':size_urls,
         'sizes':sizes,
         'color':color}
        yield Request(first_size + '&Quantity=1&format=ajax', self.get_sku_attribute_size, meta=meta_dict, dont_filter=True)

    def get_sku_attribute_size(self, response):
        length_urls = response.xpath("//ul[@class='swatch length']/li/a/@data-href").extract()
        if length_urls:
            first_length = length_urls[0]
            length_urls = length_urls[1:]
            lengths = response.xpath("//ul[@class='swatch length']/li/a/div/text()").extract()
            meta_dict = response.meta
            meta_dict['length_urls'] = length_urls
            meta_dict['lengths'] = lengths
            yield Request(first_length + '&Quantity=1&format=ajax', self.fill_sku_attributes, meta=meta_dict)
        else:
            yield Request(response.url, self.fill_sku_attributes, meta=response.meta, dont_filter=True)

    def fill_sku_attributes(self, response):
        available = response.xpath("//a[@id='add-to-cart']").extract()
        if available:
            price = response.xpath("//div[@class='sticky-price__content']/em/text()").extract_first()[1:].strip()
            was_price = response.xpath("//div[@class='sticky-price__content']/del/text()").extract_first()
            lengths = response.meta.get('lengths')
            sizes = response.meta.get('sizes')
            if lengths:
                yield from self.fill_sku_length(response, price, was_price)
            else:
                if sizes:
                    yield from self.fill_sku_sizes(response, price, was_price)
        else:
            length_urls = response.meta.get('length_urls')
            color_urls = response.meta.get('color_urls')
            size_urls = response.meta.get('size_urls')
            sizes = response.meta.get('sizes')
            meta_dict = response.meta
            if length_urls:
                lengths = response.meta.get('lengths')
                next_length = length_urls[0]
                length_urls = length_urls[1:]
                meta_dict['length_urls'] = length_urls
                meta_dict['lengths'] = lengths
                yield Request(next_length + '&Quantity=1&format=ajax', self.fill_sku_attributes, meta=meta_dict, dont_filter=True)
            else:
                if size_urls:
                    next_size = size_urls[0]
                    size_urls = size_urls[1:]
                    sizes = sizes[1:]
                    meta_dict['size_urls'] = size_urls
                    meta_dict['sizes'] = sizes
                    yield Request(next_size + '&Quantity=1&format=ajax', self.get_sku_attribute_size, meta=meta_dict, dont_filter=True)
                else:
                    if color_urls:
                        next_color = color_urls[0]
                        color_urls = color_urls[1:]
                        meta_dict['color_urls'] = color_urls
                        yield Request(next_color + '&Quantity=1&format=ajax', self.get_sku_attribute_color, meta=meta_dict, dont_filter=True)
                    else:
                        product = response.meta.get('product')
                        product['skus'] = response.meta.get('skus')
                        yield product

    def fill_sku_length(self, response, price, was_price):
        lengths = response.meta.get('lengths')
        length_urls = response.meta.get('length_urls')
        skus = response.meta.get('skus')
        color = response.meta.get('color')
        sizes = response.meta.get('sizes')
        size_urls = response.meta.get('size_urls')
        color_urls = response.meta.get('color_urls')
        currency = response.meta.get('currency')
        size = sizes[0]
        length = lengths[0]
        lengths = lengths[1:]
        skus[color + '_' + size + '_' + length] = {'color':color,
         'size':size,
         'length':length,
         'price':price,
         'currency':currency}
        if was_price:
            skus[color + '_' + size + '_' + length]['was_price'] = was_price[1:].strip()
        meta_dict = response.meta
        if length_urls:
            next_length = length_urls[0]
            length_urls = length_urls[1:]
            meta_dict['skus'] = skus
            meta_dict['length_urls'] = length_urls
            meta_dict['lengths'] = lengths
            yield Request(next_length + '&Quantity=1&format=ajax', self.fill_sku_attributes, meta=meta_dict, dont_filter=True)
        else:
            if size_urls:
                next_size = size_urls[0]
                size_urls = size_urls[1:]
                sizes = sizes[1:]
                meta_dict['size_urls'] = size_urls
                meta_dict['sizes'] = sizes
                yield Request(next_size + '&Quantity=1&format=ajax', self.get_sku_attribute_size, meta=meta_dict, dont_filter=True)
            else:
                if color_urls:
                    next_color = color_urls[0]
                    color_urls = color_urls[1:]
                    meta_dict['color_urls'] = color_urls
                    yield Request(next_color + '&Quantity=1&format=ajax', self.get_sku_attribute_color, meta=meta_dict, dont_filter=True)
                else:
                    product = response.meta.get('product')
                    product['skus'] = skus
                    yield product

    def fill_sku_sizes(self, response, price, was_price):
        sizes = response.meta.get('sizes')
        size_urls = response.meta.get('size_urls')
        size = sizes[0]
        color = response.meta.get('color')
        color_urls = response.meta.get('color_urls')
        skus = response.meta.get('skus')
        skus[color + '_' + size] = {'color':color,
         'size':size,
         'currency':response.meta.get('currency'),
         'price':price}
        if was_price:
            skus[color + '_' + size]['was_price'] = was_price[1:].strip()
        meta_dict = response.meta
        if size_urls:
            next_size = size_urls[0]
            size_urls = size_urls[1:]
            sizes = sizes[1:]
            meta_dict['size_urls'] = size_urls
            meta_dict['sizes'] = sizes
            yield Request(next_size + '&Quantity=1&format=ajax', self.get_sku_attribute_size, meta=meta_dict, dont_filter=True)
        else:
            if color_urls:
                next_color = color_urls[0]
                color_urls = color_urls[1:]
                meta_dict['color_urls'] = color_urls
                yield Request(next_color + '&Quantity=1&format=ajax', self.get_sku_attribute_color, meta=meta_dict, dont_filter=True)
            else:
                product = response.meta.get('product')
                product['skus'] = skus
                yield product

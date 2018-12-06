# -*- coding: utf-8 -*-

from scrapy import Spider, Request

from jackjone.items import JackjoneItem


class JackjoneComSpider(Spider):
    name = 'jackjones.com'
    start_urls = ['https://www.jackjones.com/gb/en/']

    custom_settings = {
        "ITEM_PIPELINES": {
            "jackjone.pipelines.FilterDuplicate": 300,
        }
    }

    item_link_attrib = "&Quantity=1&format=ajax"

    def parse(self, response):
        category_links = response.xpath(
            "//a[contains(@class, 'category-top-navigation__title')]/@href").extract()[:-2]

        for link in category_links:
            yield Request(link, self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath(
            "//a[contains(@class, 'thumb-link')]/@href").extract()

        for link in product_links:
            yield Request(link, self.parse_product_details, dont_filter=True)

        next_page_link = response.xpath(
            "//a[@rel='next']/@data-href").extract_first()

        if next_page_link:
            yield Request(next_page_link, self.parse_product_links, dont_filter=True)

    def parse_product_details(self, response):
        product = JackjoneItem()
        product['url'] = response.url
        product['pid'] = response.xpath(
            "//input[@id='pid']/@value").extract_first()
        product['article_number'] = response.xpath(
            '//form[@data-articlenumber]/@data-articlenumber').extract_first()
        product['name'] = response.xpath(
            "//h1[@class='product-name--visible']/text()").extract_first()
        category = response.xpath(
            "//div[@class='breadcrumb']/a/text()").extract()

        if category:
            product['category'] = category[0]
            product['subcategory'] = category[1:]

        product['description'] = response.xpath(
            "//meta[@name='description']/@content").extract_first()
        product['attributes'] = self.get_item_attributes(response)
        product['images'] = []
        color_urls = response.xpath("//ul[@class='swatch colorpattern']/li[@class='js-swatch-item"
                                    "swatch__item--selectable-colorpattern']/a/@data-href").extract()
        currency = response.xpath(
            "//meta[@property='og:price:currency']/@content").extract_first()
        meta = {
            'currency': currency,
            'product': product,
            'color_urls': color_urls,
            'skus': {}
        }
        yield Request(response.url, self.get_sku_attribute_color, meta=meta, dont_filter=True)

    def get_item_attributes(self, response):
        attributes = {}
        fabric = response.xpath(
            "//li[contains(@class,'pdp-description__text__value--fabric')]/text()").extract_first()

        if fabric:
            attributes['fabric'] = fabric.strip()

        care = response.xpath(
            "//li[@class='pdp-description__list__item']/text()").extract()

        if care:
            attributes['care'] = [c.strip() for c in care]

        return attributes

    def get_sku_attribute_color(self, response):
        color = response.xpath(
            "//li[contains(@class, 'swatch__item--selected-colorpattern')]/a/span/text()").extract_first()
        product = response.meta["product"]
        product['images'].extend(response.xpath(
            "//div[@class='product-images__thumbnails__underlay']/img/@data-src").extract())
        size_urls = response.xpath(
            "//ul[@class='swatch size']/li/a/@data-href").extract()
        sizes = response.xpath(
            "//ul[@class='swatch size']/li/a/div/text()").extract()
        first_size_url = size_urls[0]
        size_urls = size_urls[1:]
        meta = response.meta
        meta["product"] = product
        meta["size_urls"] = size_urls
        meta["sizes"] = sizes
        meta["color"] = color
        first_size_url = "{}{}".format(first_size_url, self.item_link_attrib)
        yield Request(first_size_url, self.get_sku_attribute_size, meta=meta, dont_filter=True)

    def get_sku_attribute_size(self, response):
        length_urls = response.xpath(
            "//ul[@class='swatch length']/li/a/@data-href").extract()
        if length_urls:
            first_length_url = length_urls[0]
            length_urls = length_urls[1:]
            lengths = response.xpath(
                "//ul[@class='swatch length']/li/a/div/text()").extract()
            meta = response.meta
            meta['length_urls'] = length_urls
            meta['lengths'] = lengths
            first_length_url = "{}{}".format(first_length_url, self.item_link_attrib)
            yield Request(first_length_url, self.fill_sku_attributes, meta=meta)
        else:
            yield from self.fill_sku_attributes(response)

    def fill_sku_attributes(self, response):
        available = response.xpath("//a[@id='add-to-cart']").extract()
        if available:
            price = response.xpath(
                "//div[@class='sticky-price__content']/em/text()").extract_first()[1:].strip()
            was_price = response.xpath(
                "//div[@class='sticky-price__content']/del/text()").extract_first()
            lengths = response.meta.get('lengths')
            sizes = response.meta.get('sizes')

            if lengths:
                yield from self.fill_sku_length(response, price, was_price)
            elif sizes:
                yield from self.fill_sku_sizes(response, price, was_price)

        else:
            yield from self.move_to_next_sku(response.meta)

    def fill_sku_length(self, response, price, was_price):
        lengths = response.meta["lengths"]
        skus = response.meta["skus"]
        color = response.meta["color"]
        sizes = response.meta["sizes"]
        currency = response.meta["currency"]
        size = sizes[0]
        length = lengths[0]
        lengths = lengths[1:]
        key = "{}_{}_{}".format(color, size, length)
        skus[key] = {
            'color': color,
            'size': size,
            'length': length,
            'price': price,
            'currency': currency
        }

        if was_price:
            skus[key]['was_price'] = was_price[1:].strip()

        meta = response.meta
        meta["lengths"] = lengths
        meta["skus"] = skus
        yield from self.move_to_next_sku(meta)

    def fill_sku_sizes(self, response, price, was_price):
        sizes = response.meta.get('sizes')
        size = sizes[0]
        color = response.meta.get('color')
        skus = response.meta.get('skus')
        key = "{}_{}".format(color, size)
        skus[key] = {
            'color': color,
            'size': size,
            'currency': response.meta.get('currency'),
            'price': price
        }

        if was_price:
            skus[key]['was_price'] = was_price[1:].strip()

        meta = response.meta
        meta["skus"] = skus
        yield from self.move_to_next_sku(meta)

    def move_to_next_sku(self, meta):
        length_urls = meta.get("length_urls")
        color_urls = meta["color_urls"]
        size_urls = meta["size_urls"]
        sizes = meta["sizes"]

        if length_urls:
            lengths = meta.get('lengths')
            next_length_url = length_urls[0]
            length_urls = length_urls[1:]
            meta['length_urls'] = length_urls
            meta['lengths'] = lengths
            next_length_url = "{}{}".format(next_length_url, self.item_link_attrib)
            yield Request(next_length_url, self.fill_sku_attributes, meta=meta, dont_filter=True)
        elif size_urls:
            next_size_url = size_urls[0]
            size_urls = size_urls[1:]
            sizes = sizes[1:]
            meta['size_urls'] = size_urls
            meta['sizes'] = sizes
            next_size_url = "{}{}".format(next_size_url, self.item_link_attrib)
            yield Request(next_size_url, self.get_sku_attribute_size, meta=meta, dont_filter=True)
        elif color_urls:
            next_color_url = color_urls[0]
            color_urls = color_urls[1:]
            meta['color_urls'] = color_urls
            next_color_url = "{}{}".format(next_color_url, self.item_link_attrib)
            yield Request(next_color_url, self.get_sku_attribute_color, meta=meta, dont_filter=True)
        else:
            product = meta.get('product')
            product['skus'] = meta.get('skus')
            yield product

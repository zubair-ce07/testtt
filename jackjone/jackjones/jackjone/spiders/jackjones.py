# -*- coding: utf-8 -*-

from scrapy import Spider, Request

from jackjone.items import JackjoneItem


class JackjoneComSpider(Spider):
    name = "jackjones.com"
    start_urls = ["https://www.jackjones.com/gb/en/"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "jackjone.pipelines.FilterDuplicate": 300,
        },
        "ROBOTSTXT_OBEY": False,
    }

    item_link_attrib = "&Quantity=1&format=ajax"

    def parse(self, response):
        category_links = response.css(".category-top-navigation__title::attr(href)").extract()[:-2]

        for link in category_links:
            yield Request(link, self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.css(".thumb-link::attr(href)").extract()

        for link in product_links:
            yield Request(link, self.parse_product_details, dont_filter=True)

        next_page_link = response.css("a[rel='next']::attr(data-href)").extract_first()

        if next_page_link:
            yield Request(next_page_link, self.parse_product_links, dont_filter=True)

    def parse_product_details(self, response):
        product = JackjoneItem()
        product["url"] = response.url
        product["pid"] = response.css("#pid::attr(value)").extract_first()
        product["article_number"] = response.css(
            "::attr(data-articlenumber)").extract_first()
        product["name"] = response.css(".product-name--visible::text").extract_first()
        category = response.css(".breadcrumb>a::text").extract()

        if category:
            product["category"] = category[0]
            product["subcategory"] = category[1:]

        product["description"] = response.css(
            "[name='description']::attr(content)").extract_first()
        product["attributes"] = self.item_attributes(response)
        product["images"] = []
        color_urls = response.css(".colorpattern>.js-swatch-item" \
                                ".swatch__item--selectable-colorpattern>a::attr(data-href)").extract()

        currency = response.css("[property='og:price:currency']::attr(content)").extract_first()
        meta = {
            "currency": currency,
            "product": product,
            "color_urls": color_urls,
            "skus": {}
        }
        return Request(response.url, self.sku_attribute_color, meta=meta, dont_filter=True)

    def item_attributes(self, response):
        attributes = {}
        fabric = response.css(".pdp-description__text__value--fabric::text").extract_first()

        if fabric:
            attributes["fabric"] = fabric.strip()

        care = response.css(".pdp-description__list__item::text").extract()

        if care:
            attributes["care"] = [c.strip() for c in care]

        return attributes

    def sku_attribute_color(self, response):
        color = response.css(".swatch__item--selected-colorpattern>a>span::text").extract_first()
        product = response.meta["product"]
        product["images"].extend(response.css(
                    ".product-images__thumbnails__underlay>img::attr(data-src)").extract())
        size_urls = response.css(".size a::attr(data-href)").extract()
        sizes = response.css(".size a>div::text").extract()
        first_size_url = size_urls.pop(0)
        meta = response.meta
        meta["product"] = product
        meta["size_urls"] = size_urls
        meta["sizes"] = sizes
        meta["color"] = color
        first_size_url = "{}{}".format(first_size_url, self.item_link_attrib)
        return Request(first_size_url, self.sku_attribute_size, meta=meta, dont_filter=True)

    def sku_attribute_size(self, response):
        length_urls = response.css(".length a::attr(data-href)").extract()

        if length_urls:
            first_length_url = length_urls.pop(0)
            lengths = response.css(".length a>div::text").extract()
            meta = response.meta
            meta["length_urls"] = length_urls
            meta["lengths"] = lengths
            first_length_url = "{}{}".format(first_length_url, self.item_link_attrib)
            return Request(first_length_url, self.fill_sku_attributes, meta=meta)
        
        return self.fill_sku_attributes(response)

    def fill_sku_attributes(self, response):
        available = response.css("#add-to-cart").extract()
        if available:
            price = response.css(".sticky-price__content>em::text").extract_first().strip("£ ")
            was_price = response.css(".sticky-price__content>del::text").extract_first()
            lengths = response.meta.get("lengths")
            sizes = response.meta.get("sizes")

            if lengths:
                return self.fill_sku_length(response, price, was_price)
            elif sizes:
                return self.fill_sku_sizes(response, price, was_price)

        else:
            return self.move_to_next_sku(response.meta)

    def fill_sku_length(self, response, price, was_price):
        lengths = response.meta["lengths"]
        skus = response.meta["skus"]
        color = response.meta["color"]
        sizes = response.meta["sizes"]
        currency = response.meta["currency"]
        size = sizes[0]
        length = lengths[0]
        key = "{}_{}_{}".format(color, size, length)
        skus[key] = {
            "color": color,
            "size": size,
            "length": length,
            "price": price,
            "currency": currency
        }

        if was_price:
            skus[key]["was_price"] = was_price.strip("£ ")

        meta = response.meta
        meta["skus"] = skus
        return self.move_to_next_sku(meta)

    def fill_sku_sizes(self, response, price, was_price):
        sizes = response.meta.get("sizes")
        size = sizes[0]
        color = response.meta.get("color")
        skus = response.meta.get("skus")
        key = "{}_{}".format(color, size)
        skus[key] = {
            "color": color,
            "size": size,
            "currency": response.meta.get("currency"),
            "price": price
        }

        if was_price:
            skus[key]["was_price"] = was_price.strip("£ ")

        meta = response.meta
        meta["skus"] = skus
        return self.move_to_next_sku(meta)

    def move_to_next_sku(self, meta):
        length_urls = meta.get("length_urls")
        color_urls = meta["color_urls"]
        size_urls = meta["size_urls"]
        sizes = meta["sizes"]

        if length_urls:
            next_length_url = meta["length_urls"].pop(0)
            meta["lengths"].pop(0)
            next_length_url = "{}{}".format(next_length_url, self.item_link_attrib)
            return Request(next_length_url, self.fill_sku_attributes, meta=meta, dont_filter=True)
        elif size_urls:
            next_size_url = meta["size_urls"].pop(0)
            meta["sizes"].pop(0)
            next_size_url = "{}{}".format(next_size_url, self.item_link_attrib)
            return Request(next_size_url, self.sku_attribute_size, meta=meta, dont_filter=True)
        elif color_urls:
            next_color_url = meta["color_urls"].pop(0)
            next_color_url = "{}{}".format(next_color_url, self.item_link_attrib)
            return Request(next_color_url, self.sku_attribute_color, meta=meta, dont_filter=True)
        else:
            product = meta.get("product")
            product["skus"] = meta.get("skus")
            return dict(product)

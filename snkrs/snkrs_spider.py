from copy import copy

from scrapy import Request
from scrapy.spiders import Spider
from snkrs.items import SnkrsItem, SnkrsSkuItem


class SnkrsSpider(Spider):
    lang = 'en'
    name = 'snkrsspider'
    possible_genders = ['Men', 'Women', 'Girl', 'Boy', 'Kids', 'Adults']
    start_urls = ['https://www.snkrs.com/en/']

    def parse(self, response):
        for url in response.css('.sf-menu a::attr(href)').extract():
            yield Request(url=url, meta={'trail': [self._parse_page_title(response)]},
                          callback=self.parse_product_url)

    def parse_product_url(self, response):
        trail = response.meta['trail']
        trail.append(self._parse_page_title(response))

        for url in response.css('.ajax_block_product .right-block a::attr(href)').extract():
            yield Request(url=url, meta={'trail': trail},
                          callback=self.parse_product)

        next_page = response.css('#pagination_next_bottom a::attr(href)').extract_first()
        if next_page:
            yield Request(url=response.urljoin(next_page), meta={'trail': trail},
                          callback=self.parse_product)

    def parse_product(self, response):
        snkrs_item = SnkrsItem()
        snkrs_item['name'] = self._parse_name(response)
        snkrs_item['retailer_sku'] = self._sku_id_generator(response)
        snkrs_item['retailer'] = self._parse_retailer(response)
        snkrs_item['category'] = self._parse_category(response)
        snkrs_item['brand'] = self._parse_brand(response)
        snkrs_item['care'] = self._parse_care(response)
        snkrs_item['description'] = self._parse_description(response)
        snkrs_item['image_urls'] = self._parse_image_urls(response)
        snkrs_item['gender'] = self._parse_gender(response).lower()
        snkrs_item['skus'] = self._parse_skus(response)
        trail = copy(response.meta['trail'])
        trail.append(self._parse_page_title(response))
        snkrs_item['trail'] = trail
        snkrs_item['lang'] = self.lang
        snkrs_item['url'] = response.url
        yield snkrs_item

    def _parse_page_title(self, response):
        return response.css('head title::text').extract()[0], response.url

    def _parse_name(self, response):
        return response.css('.pb-center-column h1::text').extract()[0]

    def _parse_retailer_sku(self, response):
        return response.css('#product_reference span::text').extract()[0]

    def _parse_retailer(self, response):
        return response.css('#header_logo a::attr(title)').extract()[0]

    def _parse_category(self, response):
        return response.css('ol.breadcrumb li a::text').extract()[1:]

    def _parse_care(self, response):
        return [c.replace('-', '').strip() for c in
                response.css('#short_description_content p:contains("%")::text').extract()] or []

    def _parse_gender(self, response):
        name = self._parse_name(response)
        categories = self._parse_category(response)
        descriptions = self._parse_description(response)

        for gender in self.possible_genders:
            if gender in name:
                return gender

            for category in categories:
                if gender in category.split(' '):
                    return gender

            for description in descriptions:
                if gender in description.split(' '):
                    return gender

        return ''

    def _parse_color(self, response):
        return response.css('#short_description_content p:contains("Color")::text').extract()[0].split(':')[1].strip()

    def _parse_brand(self, response):
        return response.css('#product_marques img::attr(alt)').extract()[0]

    def _parse_description(self, response):
        return response.css('#short_description_content p::text').extract()

    def _parse_image_urls(self, response):
        return response.css('#views_block #carrousel_frame li a::attr(href)').extract()

    def _parse_previous_price(self, response):
        return [p.split(' ')[0] for p in response.css('#old_price_display span::text').extract()]

    def _parse_price(self, response):
        return response.css('#our_price_display::attr(content)').extract()[0]

    def _parse_currency(self, response):
        return response.css('p.our_price_display meta::attr(content)').extract()[0]

    def _populate_sku_item(self, size, response):
        sku_item = SnkrsSkuItem()
        sku_item['size'] = size
        sku_item['color'] = self._parse_color(response)
        sku_item['price'] = self._parse_price(response)
        sku_item['currency'] = self._parse_currency(response)
        sku_item['sku_id'] = self._sku_id_generator(response)
        sku_item['previous_prices'] = self._parse_previous_price(response)
        return sku_item

    def _parse_skus(self, response):
        sizes_s = response.css('.attribute_list ul li span.units_container span:first-child::text').extract() or \
                  response.css('.attribute_list li span.units_container::text').extract()

        skus = []
        if sizes_s:
            skus = [self._populate_sku_item(size.strip(), response) for size in sizes_s]
        else:
            skus.append(self._populate_sku_item('One Size', response))

        return skus

    def _sku_id_generator(self, response):
        return ''.join([n[0] for n in self._parse_name(response).split(' ')])

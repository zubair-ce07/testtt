from scrapy import Request
from scrapy.spiders import Spider
from snkrs.items import SnkrsItem


class SnkrsSpider(Spider):
    lang = 'en'
    name = 'snkrsspider'
    possible_genders = ['men', 'women', 'girls', 'boys', 'unisex-kids', 'unisex-adults']
    start_urls = ['https://www.snkrs.com/en/']

    def parse(self, response):
        for url in response.css('.sf-menu a::attr(href)').extract():
            yield Request(url=url, meta={'trail': [self.make_trail(response)]},
                          callback=self.parse_product_url)

    def parse_product_url(self, response):
        trail = [*response.meta['trail'], self.make_trail(response)]

        for url in response.css('.ajax_block_product .right-block a::attr(href)').extract():
            yield Request(url=url, meta={'trail': trail},
                          callback=self.parse_product)

        next_page = response.css('#pagination_next_bottom a::attr(href)').extract_first()
        if next_page:
            yield Request(url=response.urljoin(next_page), meta={'trail': trail},
                          callback=self.parse_product)

    def parse_product(self, response):
        snkrs_item = SnkrsItem()
        snkrs_item['name'] = self.parse_name(response)
        snkrs_item['retailer_sku'] = self.parse_product_id(response)
        snkrs_item['retailer'] = self.parse_retailer(response)
        snkrs_item['category'] = self.parse_category(response)
        snkrs_item['brand'] = self.parse_brand(response)
        snkrs_item['care'] = self.parse_care(response)
        snkrs_item['description'] = self.parse_description(response)
        snkrs_item['image_urls'] = self.parse_image_urls(response)
        snkrs_item['skus'] = self.parse_skus(response)
        snkrs_item['trail'] = [*response.meta['trail'], self.make_trail(response)]
        snkrs_item['lang'] = self.lang
        snkrs_item['url'] = response.url

        gender = self.parse_gender(response)
        if gender:
            snkrs_item['gender'] = gender

        yield snkrs_item

    def make_trail(self, response):
        return response.css('head title::text').extract()[0], response.url

    def parse_name(self, response):
        return response.css('.pb-center-column h1::text').extract()[0]

    def parse_retailer_sku(self, response):
        return response.css('#product_reference span::text').extract()[0]

    def parse_retailer(self, response):
        return response.css('#header_logo a::attr(title)').extract()[0]

    def parse_product_id(self, response):
        return response.css('span.product_id::text').extract()[0]

    def parse_brand(self, response):
        return response.css('#product_marques img::attr(alt)').extract()[0]

    def parse_price(self, response):
        return response.css('#our_price_display::attr(content)').extract()[0]

    def parse_currency(self, response):
        return response.css('p.our_price_display meta::attr(content)').extract()[0]

    def parse_category(self, response):
        return response.css('ol.breadcrumb li a::text').extract()[1:-1]

    def parse_color(self, response):
        css = '#short_description_content p:contains("Color")::text'
        color = response.css(css).extract_first()
        return color.split(':')[1].strip() if color else ''

    def parse_description(self, response):
        return response.css('#short_description_content p::text').extract()

    def parse_image_urls(self, response):
        return response.css('#views_block #carrousel_frame li a::attr(href)').extract()

    def parse_previous_price(self, response):
        return [p.split(' ')[0] for p in response.css('#old_price_display span::text').extract()]

    def parse_care(self, response):
        css = '#short_description_content p:contains("%")::text'
        return [c.replace('-', '').strip() for c in response.css(css).extract()] or []

    def parse_gender(self, response):
        gender_candidates = [*self.parse_name(response).split(' '),
                             *[c for cs in self.parse_category(response) for c in cs.split(' ')],
                             *[d for ds in self.parse_description(response) for d in ds.split(' ')]]

        gender_candidates = [g.lower() for g in gender_candidates]
        output_gender = [gender for gender in self.possible_genders if gender in gender_candidates]

        return output_gender[0] if output_gender else 'unisex-adults'

    def parse_skus(self, response):
        span_css = '.attribute_list li span.units_container::text'
        inner_span_css = '.attribute_list ul li spanclear.units_container span:first-child::text'
        sizes_s = [size.strip() for size in response.css(inner_span_css).extract() or
                   response.css(span_css).extract()]

        skus = []
        for size in sizes_s or ['One Size']:
            sku = {
                'size': size,
                'price': self.parse_price(response),
                'currency': self.parse_currency(response)
            }

            color = self.parse_color(response)
            if color:
                sku['color'] = color

            previous_price = self.parse_previous_price(response)
            if previous_price:
                sku['previous_prices'] = previous_price

            sku['sku_id'] = f'{color}_{size}' if color else size
            skus.append(sku)

        return skus

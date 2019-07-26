from scrapy import Request
from scrapy.spiders import Spider
from snkrs.items import SnkrsItem


class SnkrsSpider(Spider):
    lang = 'en'
    name = 'snkrsspider'
    retailer = 'snkrs'
    genders = [
        ('women', 'women'), ('woman', 'woman'),
        ('girls', 'girls'), ('boys', 'boys'),
        ('kids', 'unisex-kids'), ('toy', 'unisex-kids'),
        ('adults', 'unisex-adults'), ('dynamic', 'unisex-adults'),
        ('guy', 'men'), ('guys', 'men'), ('jordan', 'men'), ('man', 'men'), ('men', 'men')
    ]
    start_urls = ['https://www.snkrs.com/en/']

    def parse(self, response):
        for url in response.css('.sf-menu a::attr(href)').getall():
            yield Request(url=url, meta={'trail': self.add_trail(response)},
                          callback=self.parse_listing)

    def parse_listing(self, response):
        trail = self.add_trail(response)

        css = '.ajax_block_product .right-block a::attr(href)'
        for url in response.css(css).getall():
            yield Request(url=url, meta={'trail': trail},
                          callback=self.parse_product)

        css = '#pagination_next_bottom a::attr(href)'
        next_page = response.css(css).get()
        if next_page:
            yield Request(url=response.urljoin(next_page), meta={'trail': trail},
                          callback=self.parse_product)

    def parse_product(self, response):
        snkrs_item = SnkrsItem()
        snkrs_item['lang'] = self.lang
        snkrs_item['url'] = response.url
        snkrs_item['retailer'] = self.retailer
        snkrs_item['trail'] = response.meta['trail']
        snkrs_item['skus'] = self.get_skus(response)
        snkrs_item['care'] = self.get_care(response)
        snkrs_item['name'] = self.get_name(response)
        snkrs_item['brand'] = self.get_brand(response)
        snkrs_item['gender'] = self.get_gender(response)
        snkrs_item['image_urls'] = self.get_image(response)
        snkrs_item['category'] = self.get_category(response)
        snkrs_item['description'] = self.get_description(response)
        snkrs_item['retailer_sku'] = self.get_product_id(response)
        yield snkrs_item

    def add_trail(self, response):
        trail = (response.css('head title::text').get(), response.url)
        return [*response.meta['trail'], trail] if response.meta.get('trail') else [trail]

    def get_name(self, response):
        return response.css('.pb-center-column h1::text').get()

    def get_product_id(self, response):
        return response.css('span.product_id::text').get()

    def get_brand(self, response):
        return response.css('#product_marques img::attr(alt)').get()

    def get_image(self, response):
        return response.css('#carrousel_frame li a::attr(href)').getall()

    def get_category(self, response):
        return response.css('ol.breadcrumb a::text').getall()[1:]

    def get_description(self, response):
        return response.css('#short_description_content p::text').getall()

    def get_care(self, response):
        css = '#short_description_content p:contains("%")::text'
        return [c.replace('-', '').strip() for c in response.css(css).getall()]

    def get_gender(self, response):
        gender_candidate = ' '.join([self.get_name(response)]
                                    + self.get_category(response)
                                    + self.get_description(response)
                                    ).lower()

        for tag, gender in self.genders:
            if f' {tag} ' in f' {gender_candidate} ':
                return gender

        return 'unisex-adults'

    def get_skus(self, response):
        sizes_css = 'span.units_container::text'
        sizes_inner_css = '.units_container span:first-child::text'
        sizes = [size.strip() for size in response.css(sizes_inner_css).getall() or
                 response.css(sizes_css).getall()]

        skus = []
        price_css = '#our_price_display::attr(content)'
        currency_css = 'p.our_price_display meta::attr(content)'
        for size in sizes or ['One Size']:
            sku = {
                'size': size,
                'price': response.css(price_css).get(),
                'currency': response.css(currency_css).get()
            }

            color_css = '#short_description_content p:contains("Color")::text'
            color = response.css(color_css).get()
            if color:
                color = color.replace('Color', '').replace(':', '').replace('-', '').strip()
                sku['color'] = color

            previous_price_css = '#old_price_display span::text'
            previous_prices = response.css(previous_price_css).getall()
            if previous_prices:
                sku['previous_prices'] = [p.split(' ')[0] for p in previous_prices]

            sku['sku_id'] = f'{color}_{size}' if color else size
            skus.append(sku)

        return skus

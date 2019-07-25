from scrapy import Request
from scrapy.spiders import Spider
from snkrs.items import SnkrsItem


class SnkrsSpider(Spider):
    lang = 'en'
    name = 'snkrsspider'
    retailer = 'snkrs'
    genders = {
        'women': ['woman', 'women'],
        'men': ['guy', 'guys', 'jordan', 'man', 'men'],
        'girls': ['girls'],
        'boys': ['boys'],
        'unisex-kids': ['kids', 'toy'],
        'unisex-adults': ['adults', 'dynamic']
    }
    start_urls = ['https://www.snkrs.com/en/']

    def parse(self, response):
        for url in response.css('.sf-menu a::attr(href)').extract():
            yield Request(url=url, meta={'trail': self.add_trail(response)},
                          callback=self.parse_listing)

    def parse_listing(self, response):
        trail = self.add_trail(response)

        for url in response.css('.ajax_block_product .right-block a::attr(href)').extract():
            yield Request(url=url, meta={'trail': trail},
                          callback=self.parse_product)

        next_page = response.css('#pagination_next_bottom a::attr(href)').extract_first()
        if next_page:
            yield Request(url=response.urljoin(next_page), meta={'trail': trail},
                          callback=self.parse_product)

    def parse_product(self, response):
        snkrs_item = SnkrsItem()
        snkrs_item['lang'] = self.lang
        snkrs_item['url'] = response.url
        snkrs_item['retailer'] = self.retailer
        snkrs_item['trail'] = response.meta['trail']
        snkrs_item['skus'] = self.extract_skus(response)
        snkrs_item['care'] = self.extract_care(response)
        snkrs_item['name'] = self.extract_name(response)
        snkrs_item['brand'] = self.extract_brand(response)
        snkrs_item['gender'] = self.extract_gender(response)
        snkrs_item['image_urls'] = self.extract_image(response)
        snkrs_item['category'] = self.extract_category(response)
        snkrs_item['description'] = self.extract_description(response)
        snkrs_item['retailer_sku'] = self.extract_product_id(response)
        yield snkrs_item

    def add_trail(self, response):
        trail = (response.css('head title::text').extract()[0], response.url)
        return [*response.meta['trail'], trail] if response.meta.get('trail') else [trail]

    def extract_name(self, response):
        return response.css('.pb-center-column h1::text').extract()[0]

    def extract_product_id(self, response):
        return response.css('span.product_id::text').extract()[0]

    def extract_brand(self, response):
        return response.css('#product_marques img::attr(alt)').extract()[0]

    def extract_image(self, response):
        return response.css('#carrousel_frame li a::attr(href)').extract()

    def extract_category(self, response):
        return response.css('ol.breadcrumb a::text').extract()[1:]

    def extract_description(self, response):
        return response.css('#short_description_content p::text').extract()

    def extract_care(self, response):
        css = '#short_description_content p:contains("%")::text'
        return [c.replace('-', '').strip() for c in response.css(css).extract()]

    def extract_gender(self, response):
        gender_candidate = ' '.join([self.extract_name(response)] + self.extract_category(response) +
                                    self.extract_description(response)).lower()

        for gender, tags in self.genders.items():
            output_gender = [gender for tag in tags if f' {tag} ' in f' {gender_candidate} ']
            if output_gender:
                return output_gender[0]

        return 'unisex-adults'

    def extract_skus(self, response):
        sizes_css = 'span.units_container::text'
        sizes_inner_css = '.units_container span:first-child::text'
        sizes = [size.strip() for size in response.css(sizes_inner_css).extract() or
                 response.css(sizes_css).extract()]

        skus = []
        for size in sizes or ['One Size']:
            sku = {
                'size': size,
                'price': response.css('#our_price_display::attr(content)').extract()[0],
                'currency': response.css('p.our_price_display meta::attr(content)').extract()[0]
            }

            color = response.css('#short_description_content p:contains("Color")::text').extract_first()
            if color:
                sku['color'] = color.split(':')[1].strip() or ' '.join(color.split(' ')[1:-1])

            previous_prices = response.css('#old_price_display span::text').extract()
            if previous_prices:
                sku['previous_prices'] = [p.split(' ')[0] for p in previous_prices]

            sku['sku_id'] = f'{color}_{size}' if color else size
            skus.append(sku)

        return skus

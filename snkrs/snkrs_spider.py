from scrapy import Request
from scrapy.spiders import Spider
from snkrs.items import SnkrsItem


class SnkrsSpider(Spider):
    lang = 'en'
    name = 'snkrsspider'
    retailer = 'snkrs'
    genders = [{'women': ['woman', 'women']},
               {'men': ['guy', 'guys', 'man', 'men']},
               {'girls': ['girls']},
               {'boys': ['boys']},
               {'unisex-kids': ['kids']},
               {'unisex-adults': ['adults']}]
    start_urls = ['https://www.snkrs.com/en/']

    def parse(self, response):
        for url in response.css('.sf-menu a::attr(href)').extract():
            yield Request(url=url, meta={'trail': self.make_trail(response)},
                          callback=self.parse_listing)

    def parse_listing(self, response):
        trail = self.make_trail(response)

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
        snkrs_item['trail'] = self.make_trail(response)
        snkrs_item['skus'] = self.extract_skus(response)
        snkrs_item['care'] = self.extract_care(response)
        snkrs_item['name'] = self.extract_name(response)
        snkrs_item['gender'] = self.extract_gender(response)
        snkrs_item['category'] = self.extract_category(response)
        snkrs_item['description'] = self.extract_description(response)
        snkrs_item['retailer_sku'] = response.css('span.product_id::text').extract()[0]
        snkrs_item['brand'] = response.css('#product_marques img::attr(alt)').extract()[0]
        snkrs_item['image_urls'] = response.css('#carrousel_frame li a::attr(href)').extract()
        yield snkrs_item

    def make_trail(self, response):
        trail = (response.css('head title::text').extract()[0], response.url)
        return [*response.meta['trail'], trail] if response.meta.get('trail') else [trail]

    def extract_name(self, response):
        return response.css('.pb-center-column h1::text').extract()[0]

    def extract_category(self, response):
        return response.css('ol.breadcrumb a::text').extract()[1:]

    def extract_color(self, response):
        css = '#short_description_content p:contains("Color")::text'
        color = response.css(css).extract_first()
        return color.split(':')[1].strip() if color else ''

    def extract_description(self, response):
        return response.css('#short_description_content p::text').extract()

    def extract_care(self, response):
        css = '#short_description_content p:contains("%")::text'
        return [c.replace('-', '').strip() for c in response.css(css).extract()]

    def extract_gender(self, response):
        gender_candidates = [*self.extract_name(response).split(' '),
                             *[c for cs in self.extract_category(response) for c in cs.split(' ')],
                             *[d for ds in self.extract_description(response) for d in ds.split(' ')]]

        gender_candidate = ' '.join(gender_candidates).lower()
        output_gender = [gender for g_map in self.genders for gender, tags in g_map.items() for tag in tags
                         if f' {tag} ' in f' {gender_candidate} ']

        return output_gender[0] if output_gender else 'unisex-adults'

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

            color = self.extract_color(response)
            if color:
                sku['color'] = color

            previous_price = [p.split(' ')[0] for p in response.css('#old_price_display span::text').extract()]
            if previous_price:
                sku['previous_prices'] = previous_price

            sku['sku_id'] = f'{color}_{size}' if color else size
            skus.append(sku)

        return skus

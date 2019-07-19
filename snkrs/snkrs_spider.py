from scrapy import Request
from scrapy.spiders import Spider

from snkrs.items import SnkrsItem, SnkrsSkuItem


class SnkrsSpider(Spider):
    name = 'snkrsspider'
    start_urls = ['https://www.snkrs.com/en/64-adidas',
                  'https://www.snkrs.com/en/185-adidas-performance',
                  'https://www.snkrs.com/en/192-adidas-skateboarding',
                  'https://www.snkrs.com/en/77-asics',
                  'https://www.snkrs.com/en/73-carhartt-wip',
                  'https://www.snkrs.com/en/176-chinatown-market',
                  'https://www.snkrs.com/en/175-crep-protect',
                  'https://www.snkrs.com/en/240-drake-cereal',
                  'https://www.snkrs.com/en/154-converse',
                  'https://www.snkrs.com/en/186-g-shock',
                  'https://www.snkrs.com/en/187-hypebeast',
                  'https://www.snkrs.com/en/65-jordan',
                  'https://www.snkrs.com/en/177-medicom-toy',
                  'https://www.snkrs.com/en/67-new-balance',
                  'https://www.snkrs.com/en/66-nike',
                  'https://www.snkrs.com/en/129-nike-sb',
                  'https://www.snkrs.com/en/150-polar',
                  'https://www.snkrs.com/en/68-puma',
                  'https://www.snkrs.com/en/69-reebok',
                  'https://www.snkrs.com/en/79-stussy',
                  'https://www.snkrs.com/en/178-the-new-order',
                  'https://www.snkrs.com/en/229-the-north-face',
                  'https://www.snkrs.com/en/120-tired',
                  'https://www.snkrs.com/en/70-vans',
                  'https://www.snkrs.com/en/182-snkrs',
                  'https://www.snkrs.com/en/226-91-denim']

    def parse(self, response):
        for url in response.css('.ajax_block_product .right-block a::attr(href)').extract():
            yield Request(url=url, meta={'trail_url': [response.request.url]}, callback=self.parse_product)

    def parse_product(self, response):
        snkrs_item = SnkrsItem()
        snkrs_item['name'] = self._parse_name(response)
        snkrs_item['retailer_sku'] = self._parse_retailer_sku(response)
        snkrs_item['lang'] = self._parse_language(response)
        snkrs_item['retailer'] = self._parse_retailer(response)
        snkrs_item['category'] = self._parse_category(response)
        snkrs_item['brand'] = self._parse_brand(response)
        snkrs_item['url'] = response.url
        snkrs_item['url_original'] = self._parse_url_orginal(response)
        snkrs_item['description'] = self._parse_description(response)
        snkrs_item['image_urls'] = self._parse_image_urls(response)
        snkrs_item['price'] = self._parse_price(response)
        snkrs_item['currency'] = self._parse_currency(response)
        snkrs_item['trail'] = [response.meta['trail_url'], [response.request.url]]
        snkrs_item['skus'] = self._parse_skus(response)
        yield snkrs_item

    def _parse_name(self, response):
        return response.css('.pb-center-column h1::text').extract_first()

    def _parse_retailer_sku(self, response):
        return response.css('#product_reference span::text').extract_first()

    def _parse_language(self, response):
        return response.css('html::attr(lang)').extract_first().strip()[:2]

    def _parse_retailer(self, response):
        return response.css('#header_logo a::attr(title)').extract_first()

    def _parse_category(self, response):
        return response.css('.breadcrumb li a::text').extract()[1:-1]

    def _parse_brand(self, response):
        return response.css('#product_marques img::attr(alt)').extract_first()

    def _parse_url_orginal(self, response):
        return response.css('#center_column meta::attr(content)').extract_first()

    def _parse_description(self, response):
        return response.css('#short_description_content p::text').extract()

    def _parse_image_urls(self, response):
        urls = response.css('.pb-left-column img#bigpic::attr(src)').extract()
        urls.extend(response.css('#views_block #carrousel_frame li a::attr(href)').extract())
        return urls

    def _parse_price(self, response):
        return response.css('#our_price_display::attr(content)').extract_first()

    def _parse_currency(self, response):
        return response.css('p.our_price_display meta::attr(content)').extract_first()

    def _parse_skus(self, response):
        size_types = [size_type.strip() for size_type in response.css('#view_sizes span:not(.hidden)::text').extract()]
        sizes_response = response.css('.attribute_list li:not(.hidden)')

        skus = []
        if sizes_response:
            for size_response in sizes_response:
                sku_item = SnkrsSkuItem()
                sku_item['size_type'] = size_types
                sku_item['size'] = [size_unit.strip()
                                    for size_unit in size_response.css('span span::text').extract() or
                                    size_response.css('span::text').extract()]
                sku_item['price'] = self._parse_price(response)
                sku_item['currency'] = self._parse_currency(response)
                sku_item['sku_id'] = self._parse_retailer_sku(response)
                skus.append(sku_item)
        return skus

import re
import copy
import scrapy

from scrapy.spiders import CrawlSpider

from schutzcrawler.items import ProductItem
from schutzcrawler.PriceExtractor import PriceExtractor
from schutzcrawler.mixins import Mixin


class ParseSpider(CrawlSpider, Mixin):
    name = f"{Mixin.name}-parse"
    price_extractor = PriceExtractor()

    def parse(self, response):
        product = ProductItem()
        product['brand'] = 'Schutz'
        product['care'] = self.care(response)
        product['category'] = self.category(response)
        product['description'] = self.description(response)
        product['name'] = self.product_name(response)
        product['image_urls'] = self.image_urls(response)
        product['retailer_sku'] = self.retailer_sku(response)
        product['sku'] = skus = self.skus(response)
        product['trail'] = response.meta.get('trail', [])
        product['url'] = response.url
        product['out_of_stock'] = self.is_out_of_stock(skus)

        yield product

    def image_urls(self, response):
        return response.css('div.is-slider-item > img::attr(src)').extract()

    def raw_description(self, response):
        description_text = '.sch-description-content p ::text'
        specifications = '.sch-description-list li'

        description = response.css(description_text).extract() or []
        for specification in response.css(specifications):
            spec_name = specification.css('span::text').extract_first()
            spec_value = specification.css('strong::text').extract_first()
            description.append(f"{spec_name}: {spec_value}")
        return description

    def description(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description if 'Material' not in rd]

    def color(self, response):
        raw_description = self.raw_description(response)
        color = [rd.split(':')[1] for rd in raw_description if 'Cor' in rd]
        return color[0] if color else ''

    def care(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description if 'Material' in rd]

    def category(self, response):
        categories = response.css('.clearfix a::text').extract()
        return categories[1:-1]

    def skus(self, response):
        skus = {}
        raw_prices = response.css('.sch-price ::text').extract()
        common_sku = self.price_extractor.prices(raw_prices)
        color = self.color(response)
        common_sku['color'] = color
        size_dropdown_css = '.sch-notify-form .sch-form-group-select select option'
        size_css = '.sch-sizes label'
        sizes = response.css(size_css) or response.css(size_dropdown_css)
        for size in sizes:
            sku = copy.deepcopy(common_sku)
            size_value = size.css(' ::text').extract_first()
            sku['size'] = size_value
            if size.xpath('self::*[not(contains(@class, "sch-avaiable"))]'):
                sku['out_of_stock'] = True
            skus[f"{color}{size_value}"] = sku

        if not skus:
            common_sku['size'] = 'One Size'
            if response.css('.sch-notify-form'):
                common_sku['out_of_stock'] = True
            skus['One Size'] = common_sku
        return skus

    def is_out_of_stock(self, sku):
        return not any('out_of_stock' not in v for v in sku.values())

    def retailer_sku(self, response):
        retailer_sku_css = '.sch-pdp::attr(data-product-code)'
        return response.css(retailer_sku_css).extract_first()

    def product_name(self, response):
        name_css = '.sch-sidebar-product-title::text'
        return response.css(name_css).extract_first()

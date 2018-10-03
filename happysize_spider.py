"""
This module scrapes products data from HappySize website
"""
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HappySizeSpider(CrawlSpider):
    name = 'happysize'
    allowed_domains = ['happy-size.de']
    start_urls = ['https://www.happy-size.de/damen/']
    allow = ('/damen', '/herren')
    rules = (
        Rule(LinkExtractor(restrict_css=['.categoryNavContainer'], allow=allow)),
        Rule(LinkExtractor(restrict_css=['.linkContainer'])),
        Rule(LinkExtractor(restrict_css=['.productBoxImage']), callback='parse_product')
    )

    def parse_product(self, response):
        product = {}
        product['name'] = response.css('.productName::text').extract_first()
        product['description'] = response.css(
            '.longDescriptionText span[itemprop="description"]::text').extract_first()
        product['currency'] = response.css(
            'meta[itemprop="priceCurrency"]::attr(content)').extract_first()
        product['composition'] = self.get_composition(response)
        product['care'] = self.get_care(response)
        product['bread-crumb'] = response.css('.breadcrumbsEntry span::text').extract()
        product['product_url'] = response.url
        product['brand'] = response.css('.brandName::text').extract_first().strip()
        product['image_urls'] = response.css('.overview a::attr(data-image)').extract()
        product['skus'] = self.skus_formation(response)
        return product

    def get_care(self, response):
        care_list = response.css(
            '.productAttributeFlexTable div .flex_Attribute.attribute__Value::text').extract()
        if care_list:
            return care_list[-1]
        return None

    def get_composition(self, response):
        composition_list = []
        raw_composition_list = response.css('.sellingPoints span::text').extract()
        if raw_composition_list:
            for composition in raw_composition_list:
                composition_list.append(composition.strip())
            return composition_list
        return None

    def skus_formation(self, response):
        sku_list = []
        color_list = response.css('.colorTile div::attr(title)').extract()
        size_list = response.css('.productSizes.tileContainer option::attr(value)').extract()
        price = response.css('meta[itemprop="price"]::attr(content)').extract_first()
        if color_list and size_list:
            for color in color_list:
                for size in size_list:
                    temp_dict = {
                        'color': color,
                        'size': size,
                        'price': price
                    }
                    sku_list.append(temp_dict)
            return sku_list
        return None


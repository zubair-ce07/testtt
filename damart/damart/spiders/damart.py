"""
This module crawls pages and gets data.
"""
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Damart(CrawlSpider):
    """This class crawls damart pages"""
    name = 'damart'
    allowed_domains = ['damart.co.uk']
    start_urls = ['https://www.damart.co.uk']
    rules = [
        Rule(LinkExtractor(
            restrict_css=['li'],),            ),
        Rule(LinkExtractor(
            restrict_css=['.k-product'],),
             callback='parse_item_detail'),
    ]

    def parse_item_detail(self, response):
        """This method crawls item detail information."""
        title = response.css('.product-data>h1::text').extract_first()
        product_id = response.css('.t-zone>p>span::text').extract_first()
        title_description = response.css(
            '.title_description_product>strong::text').extract_first()
        description = response.css(
            '.new_info-desc>.product-info>li::text').extract()
        more_description = response.css(
            '.new_info-desc>.para_hide::text').extract()
        full_price = response.css(
            '.no_promo::text').extract_first()
        if not full_price:
            # if item is on sale
            full_price = response.css(
                '.old-price>span::text').extract_first()
            sale_price = response.css(
                '.price.sale::text').extract_first()
            discount_upto = response.css(
                '.promotion_img>.rate::text').extract_first()
        else:
            discount_upto = '0'
            sale_price = full_price
        full_price = full_price + '00'
        sale_price = sale_price + '00'
        product_data = {
            'item_detail_url': response.url,
            'title': title.strip(),
            'product_id': product_id,
            'title_description': title_description,
            'description': description,
            'more_description': more_description,
            'full_price': full_price,
            'sale_price': sale_price,
            'discount_upto': discount_upto,
        }
        yield product_data


import json

class dataGetterClass(object):

    def __init__(self):
        pass
    
    def get_total_count(self, response):

        return int(''.join(
                        filter(
                            str.isdigit,
                            response.xpath(
                    '//div[contains(@class, "count-text")]/text()'
                    ).extract_first()
                )
            )
        )

    def get_care (self, response):
        return response.xpath(
                '//div[contains(@class, "garment-care")]//span/text()'
        ).extract()
        
    def get_category (self, response):
        return response.xpath(
            '//section[contains(@class, "breadcrumb")]//li/a//text()'
        )[-1].extract()

    def get_image_urls (self, response):
        return response.xpath(
            '//div[contains(@class, "productImages")]//img/@src'
        ).extract()

    def get_name (self, response):
        return response.xpath(
            '//div[contains(@class, "product-heading")]//h1/text()'
        ).extract_first()

    def get_color (self, response):
        return list(
            filter(None, response.xpath(
                '//div[contains(@class, "color-swatch")]//a/@title'
                ).extract()
            )
        )
    
    def get_currency (self, response):
        response.xpath(
            '//div[contains(@class, "price")]/span/text()'
        ).extract_first()

    def get_price (self, response):
        return response.xpath(
            '//div[contains(@class, "price")]/span/text()'
        ).extract_first()

    def get_size (self, response):
        return response.xpath(
            '//div[contains(@id, "sizeWrap")]/a/text()'
        ).extract_first()
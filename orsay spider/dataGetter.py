
import json

class DataGetterClass(object):
    
    def product_care(self, response):
        return response.xpath(
                '//div[contains(@class, "product-material")]/p/text()'
        ).extract()
        
    def product_category(self, response):
        return response.xpath(
            '//a[contains(@class, "breadcrumb-element-link")][last()]/span/text()'
        ).extract_first()

    def product_discription (self, response):
        return response.xpath(
            '//div[contains(@class,"with-gutter")]/text()'
        ).extract()

    def product_image_urls (self, response):
        return response.xpath(
            '//img[contains(@class,"productthumbnail")]/@src'
        ).extract()

    def product_name (self, response):
        return response.xpath(
                '//h1[contains(@class,"product-name")]/text()'
        ).extract_first()

    def product_color (self, response):
        color_list = []
        for item in response.xpath('//ul[contains(@class, "swatches color")]//a/@title').extract():
            color_list.append(item.split('-')[-1])
        
        return color_list

    def product_selected_color(self, response):
        return response.xpath(
                '//li[contains(@class, "attribute")]//span[contains(@class, "selected-value")]/text()'
        ).extract_first()
        

    def product_currency (self, response):
        return response.xpath(
                    '//div[contains(@class, "current")]'
                + '//span[contains(@class, "country-currency")]/text()'
            ).extract_first()

    def product_price (self, response):
        price = response.xpath(
                    '//div[contains(@class,"product-price")]/span/text()'
                ).extract_first()
        if price:
            return price.strip()
        return "N/A"

    def product_size (self, response):
        size = response.xpath(
                    '//ul[contains(@class, "swatches size")]'
                + '/li[contains(@class, "selected")]/a/text()'
                ).extract_first()
        
        if size:
            return (size.rstrip()).replace('\n','')
        return "One Size"
    
    def sku_id(self, response):
        data = response.xpath(
            '//div[contains(@class, "js-product-content-gtm")]/@data-product-details'
            ).extract_first()
        if data:
            data = json.loads(data)
            return data['idListRef12']
        else:
            return 'N/A'
    
    def product_id(self, response):
        data = response.xpath(
            '//div[contains(@class, "js-product-content-gtm")]/@data-product-details'
            ).extract_first()
        if data:
            data = json.loads(data)
            return data['idListRef6']
        else:
            return 'N/A'

    def shown_count(self, response):
        return int (
            response.xpath(
                '//div[contains(@class, "load-more-progress-label")]/span/text()'
                ).extract_first()
            )

    def next_count(self, response):
        return int (
                response.xpath(
                    '//div[contains(@class, "load-next-placeholder")]/@data-quantity'
                ).extract_first()
            )
    def product_url (self, response):
        return response.request.url

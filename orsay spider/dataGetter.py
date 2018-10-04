
import json
import scrapy
from .productclass import Product

class DataGetterClass(object):
    
    def product_care(self, response):
        xpath = '//div[contains(@class, "product-material")]/p/text()'
        return response.xpath(xpath).extract()
        
    def product_category(self, response):
        xpath = '//a[contains(@class, "breadcrumb-element-link")][last()]'\
                +'/span/text()'
        return response.xpath(xpath).extract_first()

    def product_discription (self, response):
        xpath = '//div[contains(@class,"with-gutter")]/text()'
        return response.xpath(xpath).extract()

    def product_image_urls (self, response):
        xpath = '//img[contains(@class,"productthumbnail")]/@src'
        return response.xpath(xpath).extract()
        
    def product_name (self, response):
        xpath = '//h1[contains(@class,"product-name")]/text()'
        return response.xpath(xpath).extract_first()

    def product_color (self, response):
        color_list = []
        xpath = '//ul[contains(@class, "swatches color")]//a/@title'
        
        for item in response.xpath().extract(xpath):
            color_list.append(item.split('-')[-1])
        
        return color_list

    def product_selected_color(self, response):
        xpath = '//li[contains(@class, "attribute")]'\
                +'//span[contains(@class, "selected-value")]/text()'
        return response.xpath(xpath).extract_first()
        

    def product_currency (self, response):
        xpath = '//div[contains(@class, "current")]'\
                + '//span[contains(@class, "country-currency")]/text()'
        return response.xpath(xpath).extract_first()

    def product_price (self, response):
        xpath = '//div[contains(@class,"product-price")]/span/text()'
        price = response.xpath(xpath).extract_first()

        if price:
            return price.strip()
        return "Out of Skock"

    def product_size (self, response):
        xpath = '//ul[contains(@class, "swatches size")]'\
                + '/li[contains(@class, "selected")]/a/text()'
        size = response.xpath(xpath).extract_first()
        
        if size:
            return (size.rstrip()).replace('\n','')
        return "One Size"
    
    def sku_id(self, response):
        xpath = '//div[contains(@class, "js-product-content-gtm")]'\
                +'/@data-product-details'
        data = response.xpath(xpath).extract_first()

        if data:
            data = json.loads(data)
            return data['idListRef12']
        else:
            return 'N/A'

    def product_colors_links(self, response):
        xpath = '//ul[contains(@class, "swatches color")]/'\
                'li[not(contains(@class, "selected"))]//a/@href'
        return response.xpath(xpath).extract()
    
    def product_id(self, response):
        xpath = '//div[contains(@class, "js-product-content-gtm")]'\
                +'/@data-product-details'
        data = response.xpath(xpath).extract_first()

        if data:
            data = json.loads(data)
            return data['idListRef6']
        else:
            return 'N/A'

    def shown_count(self, response):
        xpath = '//div[contains(@class, "load-more-progress-label")]/span/text()'
        count = response.xpath(xpath).extract_first()
        return int (count)

    def next_count(self, response):
        xpath = '//div[contains(@class, "load-next-placeholder")]/@data-quantity'
        count = response.xpath(xpath).extract_first()
        return int (count)

    def parse_product_details(self, response):
        product = Product(
            brand = 'orsay',
            care = self.product_care(response),
            category = self.product_category(response),
            discription = self.product_discription(response),
            image_urls = self.product_image_urls(response),
            retailer_skus = self.sku_id(response),
            name = self.product_name(response),
            skus = {
                self.sku_id(response) : self.get_sku(response)
            },
            url = response.url,
            color_links = self.product_colors_links(response)
        )   
        return self.next_color_link(product)

    def next_color_link(self, item):
        color_list_link = item['color_links']    
        if color_list_link:
            link = color_list_link.pop()
            req = scrapy.Request(url=link, callback=self.product_skus)
            req.meta['item'] = item
            yield req
        else:
            item.pop('color_links')
            yield item

    def product_skus(self, response):
        item = response.meta['item']
        item_details = self.get_sku(response)
        item['skus'][self.sku_id(response)] = item_details
        item['image_urls'] += self.product_image_urls(response)
        
        return self.next_color_link(item)

    def get_sku(self, response):
        return {
            'color' :self.product_selected_color(response),
            'price' : self.product_price(response),
            'currency' : self.product_currency(response),
            'size' : self.product_size(response)
        }
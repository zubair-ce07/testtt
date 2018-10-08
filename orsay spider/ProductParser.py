
import json
import scrapy

from .productclass import Product

class ProductParser():

    def parse_product_details(self, response):
        product = Product()

        product['brand'] = 'orsay',
        product['care'] = self.product_care(response),
        product['category'] = self.product_category(response),
        product['discription'] = self.product_discription(response),
        product['image_urls'] = self.product_image_urls(response),
        product['retailer_sku'] = self.product_id(response),
        product['name'] = self.product_name(response),
        product['skus'] = {self.sku_id(response) : self.product_sku(response)},
        product['url'] = response.url,
        product['color_requests'] = self.product_colors_links(response)

        return self.follow_color(product)

    def product_skus(self, response):
        item = response.meta['item']
        item_details = self.product_sku(response)
        item_skus = item['skus']
        item_skus.append({self.sku_id(response) : item_details})
        item['skus'] = item_skus
        item['image_urls'] += self.product_image_urls(response)
        
        return self.follow_color(item)

    def follow_color(self, item):
        color_list_link = item['color_requests']    
        if color_list_link:
            link = color_list_link.pop()
            req = scrapy.Request(url=link, callback=self.product_skus)
            req.meta['item'] = item
            yield req
        else:
            item.pop('color_requests')
            yield item

    def product_sku(self, response):
        sku = dict()
        
        sku.update({'color' :self.product_selected_color(response)})
        sku.update({'price' : self.product_price(response)})
        sku.update({'currency' : self.product_currency(response)})
        sku.update({'size' : self.product_size(response)})

        return sku

    def product_care(self, response):
        css = 'div[class*=product-material] > p::text'
        return response.css(css).extract()
        
    def product_category(self, response):
        css = 'div.breadcrumb > a:nth-last-child(2) > span::text'
        return response.css(css).extract_first()

    def product_discription (self, response):
        css = 'div[class*=with-gutter]::text'
        return response.css(css).extract()

    def product_image_urls (self, response):
        css = 'img[class*=productthumbnail]::attr(src)'
        return response.css(css).extract()
        
    def product_name (self, response):
        css = 'h1[class*=product-name]::text'
        return response.css(css).extract_first()

    def product_color (self, response):
        colors = []
        css = 'ul[class*=swatches color] a::attr(title)'
        
        for item in response.css().extract(css):
            colors.append(item.split('-')[-1])
        return colors

    def product_selected_color(self, response):
        css = 'span[class*=selected-value]::text'
        return response.css(css).extract_first()
        
    def product_currency (self, response):
        css = 'span[class*=country-currency]::text'
        return response.css(css).extract_first()

    def product_price (self, response):
        css = 'div[class*=product-price] > span::text'
        price = response.css(css).extract_first()
        return price.strip()

    def product_size (self, response):
        css = 'ul[class*=size] > li[class*=selected] > a::text'
        size = response.css(css).extract_first()
        
        if size:
            return (size.rstrip()).replace('\n','')
        return "One Size"
    
    def sku_id(self, response):
        css = 'div[class*=js-product-content-gtm]::attr(data-product-details)'
        data = response.css(css).extract_first()
        data = json.loads(data)
        return data['idListRef12']
            

    def product_colors_links(self, response):
        xpath = '//ul[contains(@class, "swatches color")]/'\
                'li[not(contains(@class, "selected"))]//a/@href'
        return response.xpath(xpath).extract()
    
    def product_id(self, response):
        css = 'div[class*=js-product-content-gtm]::attr(data-product-details)'
        data = response.css(css).extract_first()
        data = json.loads(data)
        return data['idListRef6']

    def shown_count(self, response):
        css = 'div[class*=load-more-progress-label] > span::text'
        count = response.css(css).extract_first()
        return int (count)

    def next_count(self, response):
        css = 'div[class*=load-next-placeholder]::attr(data-quantity)'
        count = response.css(css).extract_first()
        return int(count)

import re

from Woolrich.items import WoolrichItem


class WoolGeneral:
    product_ids = []

    def product(self, response, xpath):
        product_id = response.xpath(xpath).extract_first()
        if product_id in self.product_ids:
            return
        self.product_ids.append(product_id)
        product = WoolrichItem()
        product['product_id'] = product_id
        return product

    @staticmethod
    def next_action(product):
        if product['pending_requests']:
            request = product['pending_requests'].pop()
            request.meta['product'] = product
            return request
        return product

    @staticmethod
    def price(response, xpath):
        price = response.xpath(xpath).extract_first(default='')
        price = price.replace(',', '')
        return int(round(float(price) * 100))

    @staticmethod
    def previous_prices(response, xpath):
        previous_prices = response.xpath(xpath).extract()
        prices = []
        for price in previous_prices:
            price = price.replace(',', '')
            previous_price = int(round(float(re.search(r'\d+.\d+', price).group(0)) * 100))
            prices.append(previous_price)
        return prices

import re

class PriceExtractor:

    def clean_price_list(price_list):
        cleaned_price_list = []
        for prices in price_list:
            prices = re.findall('\d+', prices)
            if prices:
                cleaned_price_list.append(int(prices[0]) * 100)
        return cleaned_price_list
    
    @staticmethod
    def prices(response):
        price_list = response.css('.sch-price ::text').extract()
        price_list = set(PriceExtractor.clean_price_list(price_list))
        return sorted(price_list)

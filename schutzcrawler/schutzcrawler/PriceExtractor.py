import re

class PriceExtractor:
    currencies = {'R$':'BRL'}
    currency = ''

    def clean_price_list(self, prices):
        cleaned_prices = []
        for price in prices:
            for key, value in self.currencies.items():
                if key in price:
                    self.currency = value

            price = re.findall('\d+', price)
            if price:
                cleaned_prices.append(int(price[0]) * 100)
        return cleaned_prices
    
    def prices(self, prices): 
        sorted_prices = sorted(set(self.clean_price_list(prices)))
        previous_prices = sorted_prices[1:]
        prices = {'price':sorted_prices[0], 'currency':self.currency}
        if previous_prices:
            prices['previous_prices'] = previous_prices
        return prices

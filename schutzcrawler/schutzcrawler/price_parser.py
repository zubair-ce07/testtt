import re


class PriceParser:
    currencies = {'R$': 'BRL', 'EUR': 'EUR', '$': 'USD'}

    def clean_prices(self, prices):
        raw_prices = []
        for price in prices:
            price = ''.join(re.findall('\d+', price))
            if price:
                raw_prices.append(int(price))
        return raw_prices

    def currency(self, prices):
        for price in prices:
            for key, value in self.currencies.items():
                if key in price:
                    return value

    def prices(self, prices):
        raw_prices = sorted(set(self.clean_prices(prices)))
        currency = (self.currency(prices))
        previous_prices = raw_prices[1:]
        prices = {'price': raw_prices[0], 'currency': currency}
        if previous_prices:
            prices['previous_prices'] = previous_prices
        return prices

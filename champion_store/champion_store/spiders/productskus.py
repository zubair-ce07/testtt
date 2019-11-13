from .utils import VALUE_EXTRACTOR_FROM_KEY, product_currency, product_price


class ProductSku:

    def __init__(self):
        self.product_skus = []

    def collect_product_skus(self, response, raw_skus, sku_id):

        for sku in raw_skus:
            self.product_skus.append(
                {
                    "price": product_price(response, sku_id),
                    "currency": product_currency(response),
                    "previous_prices": [self.sku_previous_price(response, sku_id)],
                    "colour": self.sku_color(sku.get('Attributes')),
                    "size": self.sku_size(sku.get('Attributes')),
                    "sku_id": sku.get('catentry_id')
                }
            )
        return self.product_skus

    def clean_key_value(self, raw_key_value):
        return VALUE_EXTRACTOR_FROM_KEY.findall(raw_key_value)[0]

    def sku_color(self, raw_sku):
        if not raw_sku:
            return 'one'

        color_key = list(raw_sku.keys())[1]
        return self.clean_key_value(color_key)

    def sku_size(self, raw_sku):
        if not raw_sku:
            return 'one'

        size_key = list(raw_sku.keys())[0]
        return self.clean_key_value(size_key)

    def sku_previous_price(self, response, sku_id):
        raw_previous_price = response.css(f'#ProductInfoListPrice_{sku_id}::attr(value)').re_first(r'[\d.]+')
        return raw_previous_price.replace('.', '') if raw_previous_price else None

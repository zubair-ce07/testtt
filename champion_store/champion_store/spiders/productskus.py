from .utils import VALUE_EXTRACTOR_FROM_KEY


class ProductSku:

    def collect_product_skus(self, response, raw_skus, sku_id):
        product_skus = []

        for sku in raw_skus:
            sku_item = {}
            sku_item['previous_prices'] = [self.sku_previous_price(response, sku_id)]
            sku_item['colour'] = self.sku_color(sku.get('Attributes'))
            sku_item['size'] = self.sku_size(sku.get('Attributes'))
            sku_item['sku_id'] = sku.get('catentry_id')
            product_skus.append(sku_item)

        return product_skus

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
        selector = f'#ProductInfoListPrice_{sku_id}::attr(value)'
        raw_previous_price = response.css(selector).re_first(r'[\d.]+')
        return raw_previous_price.replace('.', '') if raw_previous_price else None

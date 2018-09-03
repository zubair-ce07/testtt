from itertools import product
from json import loads

from scrapy import Spider, FormRequest
from w3lib.url import urljoin
from scrapy.loader.processors import SelectJmes

from ..items import ProductItemLoader, SkuItemLoader


class WoolrichItemloaderParserSpider(Spider):
    name = 'woolrich_itemloader_parser'
    sku_base_url = "https://www.woolrich.com/remote/v1/product-attributes/"

    product_css_map = {
        "retailer_sku":  "strong:contains(Style)::text",
        "gender": ".breadcrumb-label::text",
        "category": ".breadcrumb-label::text",
        "name": ".productView-title::text",
        "description": "#details-content::text",
        "care": "#features-content >::text",
        "image_urls": ".zoom ::attr(src)"

    }

    def parse(self, response):
        product_loader = ProductItemLoader(response=response)
        product_loader.add_value("lang", "en")
        product_loader.add_value("trail", response.meta.get("trail", []))
        product_loader.add_value("brand", "Woolrich")
        product_loader.add_value("url", response.url)
        product_loader.add_value("market", "US")
        product_loader.add_value("url_original", response.url)

        for field, field_css in self.product_css_map.items():
            product_loader.add_css(field, field_css)

        product_item = product_loader.load_item()
        return self.prepare_request(self.sku_requests(response), product_item)

    def parse_sku(self, response):
        product_item = response.meta["product_item"]
        product_loader = ProductItemLoader(response=response, item=product_item)
        raw_sku = loads(response.text)

        sku_loader = SkuItemLoader(response=response)
        sku_loader.add_value("colour", response.meta["colour"])
        sku_loader.add_value("size", response.meta["size"])
        sku_loader.add_value("sku", SelectJmes("data.sku")(raw_sku))
        sku_loader.add_value("price", SelectJmes("data.price.without_tax.value")(raw_sku))
        sku_loader.add_value("previous_prices", SelectJmes("data.price.rrp_without_tax.value")(raw_sku))
        sku_loader.add_value("currency", "USD")
        sku_loader.add_value("out_of_stock", SelectJmes("data.instock")(raw_sku))

        product_loader.add_value("skus", sku_loader.load_item())
        product_item = product_loader.load_item()
        return self.prepare_request(response.meta["requests"], product_item)

    @staticmethod
    def prepare_request(requests, product_item):
        if requests:
            request = requests.pop()
            request.meta["product_item"] = product_item
            request.meta["requests"] = requests
            yield request
        else:
            yield product_item

    def sku_requests(self, response):
        raw_skus = self.raw_skus(response)
        product_id = response.css("[name='product_id']::attr('value')").extract_first()
        sku_url = urljoin(self.sku_base_url, product_id)
        requests = []

        for raw_sku in raw_skus:
            meta = {
                "colour": raw_sku["colour"],
                "size": raw_sku.get("size", "One size")
            }
            request = FormRequest(url=sku_url, formdata=raw_sku["form-data"],
                                  callback=self.parse_sku, meta=meta)
            requests.append(request)

        return requests

    @staticmethod
    def raw_skus(response):
        raw_skus_css = "[data-cart-item-add] [data-product-attribute='{}']"
        colour_title_css = "[for*='{}'] ::attr(title)"
        size_title_css = "[for*='{}'] >::text"
        attr_value_css = "::attr(value)"
        attr_name_css = "::attr(name)"
        form_input_css = "input[name]"

        raw_colour_s = response.css(raw_skus_css.format("swatch"))
        raw_size_s = response.css(raw_skus_css.format("set-rectangle"))
        raw_skus = []

        for colour_s in raw_colour_s.css(form_input_css):
            value = colour_s.css(attr_value_css).extract_first()
            raw_skus.append({
                "form-data": {colour_s.css(attr_name_css).extract_first(): value},
                "colour": raw_colour_s.css(colour_title_css.format(value)).extract_first()
            })

        for size_s in raw_size_s:
            skus = raw_skus.copy()
            raw_skus = []

            for raw_sku, size in product(skus, size_s.css(form_input_css)):
                sku = raw_sku.copy()
                form_data = sku["form-data"].copy()
                value = size.css(attr_value_css).extract_first()
                form_data[size.css(attr_name_css).extract_first()] = value
                sku["form-data"] = form_data
                title = raw_size_s.css(size_title_css.format(value)).extract_first()
                sku["size"] = "{}/{}".format(sku["size"], title) if "size" in sku else title
                raw_skus.append(sku)

        return raw_skus

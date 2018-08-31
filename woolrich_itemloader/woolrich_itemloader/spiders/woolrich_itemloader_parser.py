from itertools import product
from json import loads

from scrapy import Spider, FormRequest
from scrapy.loader.processors import Identity, MapCompose
from w3lib.url import urljoin

from ..items import ProductItemLoader, sku


class WoolrichItemloaderParserSpider(Spider):
    name = 'woolrich_itemloader_parser'
    sku_base_url = "https://www.woolrich.com/remote/v1/product-attributes/"

    def parse(self, response):
        product_loader = ProductItemLoader(response=response)
        product_loader.add_css("retailer_sku", "strong:contains(Style)::text")
        product_loader.add_value("lang", "en")
        product_loader.add_value("trail", response.meta.get("trail", []))
        product_loader.add_css("gender", ".breadcrumb-label::text")
        product_loader.add_css("category", ".breadcrumb-label::text")
        product_loader.add_value("brand", "Woolrich")
        product_loader.add_value("url", response.url)
        product_loader.add_value("market", "US")
        product_loader.add_value("url_original", response.url)
        product_loader.add_css("name", ".productView-title::text")
        product_loader.add_css("description", "#details-content::text")
        product_loader.add_css("care", "#features-content >::text")
        product_loader.add_css("image_urls", ".zoom ::attr(src)")
        product_item = product_loader.load_item()
        return self.prepare_request(self.sku_requests(response), product_item)

    def parse_sku(self, response):
        product_item = response.meta["product_item"]
        product_loader = ProductItemLoader(response=response, item=product_item)
        product_loader.add_value("skus", product_item.get("skus"), Identity())
        product_loader.add_value("skus", response, MapCompose(lambda resp: sku(resp)))
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

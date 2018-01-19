import scrapy
from sfera.items import SferaItem


class SferaParser(scrapy.Spider):
    name = "sfera_parser"
    start_urls = ["https://www.sfera.com/es/"]
    product_details_api = "https://www.sfera.com/one/mod/_lista_carga.php"
    genders = {
        "Mujer": "Women",
        "Hombre": "Men",
        "Niños & Bebés": "Baby Boys",
    }

    def gender(self, response):
        categories = response.xpath('//div[@id="cab_texto"]//h2/a/text()').extract()
        for category in categories:
            return self.genders.get(category) or 'Adults'

    def categories(self, raw_product):
        return raw_product["categorias"]

    def map_urlc(self, raw_product):
        return raw_product["mapa_urlc"].strip()[4:]

    def url_code(self, raw_product):
        return raw_product["urlc"].strip()

    def original_url(self, raw_product):
        refer_code = raw_product["reference_code"].strip()
        return '%s%s%s/%s' % (self.start_urls[0], self.map_urlc(raw_product),
                              self.url_code(raw_product), refer_code)

    def price(self, raw_product):
        price = raw_product["precio"]
        return int(price.replace('.', ''))

    def previous_price(self, raw_product):
        previous_price = raw_product["precio_ant"]
        return int(previous_price.replace('.', ''))

    def stock_exist_or_not(self, raw_product):
        return "available" if raw_product["stock"] == "1" else "out_of_stock"

    def color(self, raw_product):
        return raw_product["nomref"]

    def available_sizes(self, raw_product):
        sizes = raw_product["tallas"]
        return sizes.split(',') if raw_product["tallas"] else ["one_size"]

    def trails(self, raw_product):
        return [["", self.start_urls[0]], [self.categories(raw_product)[1],
                                           '%s%s' % (self.start_urls[0], self.map_urlc(raw_product))]]

    def skus(self, raw_product):
        skus = []
        for size in self.available_sizes(raw_product):
            skus_details = {}
            skus_details["size"] = size
            skus_details["price"] = self.price(raw_product)
            skus_details["previous_price"] = self.previous_price(raw_product)
            skus_details["stock"] = self.stock_exist_or_not(raw_product)
            skus_details["color"] = self.color(raw_product)
            skus_details["sku_id"] = raw_product["id"]
            skus_details["currency"] = "EUR"
            skus.append(skus_details)
        return skus

    def parse(self, response):
        item = response.meta["item"]
        products_text = response.xpath('//script[contains(text(),"lrefsver.push")]/text()').extract()
        for product_text in products_text:
            json_content = re.search('({.+})', product_text).group()
            raw_product = json.loads(json_content)
            item["description"] = raw_product["descripcion"]
            item["title"] = raw_product["nombre"]
            item["images"] = raw_product["lista_imgs"].split(',')
            item["categories"] = self.categories(raw_product)
            item["url_original"] = self.original_url(raw_product)
            item["skus"] = self.skus(raw_product)
            item["trails"] = self.trails(raw_product)
            item["retailer_sku"] = raw_product["id"]
            yield item

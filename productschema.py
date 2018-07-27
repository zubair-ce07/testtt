import json
import re


class Sku:
    def __init__(self, data):
        self.colour = data.get("color") if "color" in data else "one color"
        self.price = float(data.get("offers").get("price")) if "offers" in data else float(data.get("price"))
        self.currency = data.get("offers").get("priceCurrency") if "offers" in data else None
        self.size = re.search(r"\w{16}([\.\w\d]*)", data.get("mpn")).group(1) if "mpn" in data else "one size"
        self.size = self.size if self.size != "T.U." else "one size"
        self.previous_prices = []
        self.out_of_stock = False if "offers"not in data or "InStock"in data.get("offers").get("availability") else True
        self.sku_id = data.get("mpn") if "mpn" in data else data.get("id")


class Product:
    def __init__(self, url, selector):
        price = selector.css('span.price[id*="product-price"]::text').extract_first()
        json_string = selector.css('script[type="application/ld+json"]::text').extract_first()
        print(url)
        print(price)
        if re.search(r'"@type": *"Product"', json_string):
            json_string = self._validate_json(selector.css('script[type="application/ld+json"]::text').extract_first())
            print(json_string)
            data = json.loads(json_string)
            self.skus = {}
            for combo in data:
                sku = Sku(combo)
                if price:
                    sku.previous_prices.append(sku.price)
                    sku.price = float(re.search(r"\d+[\.|,]\d+", price).group().replace(",", "."))
                self.skus.update({sku.sku_id: sku})
            self.retailer_sku = combo.get("sku")
            self.category = re.search(r'"category": "+(.+)"', self._extract_json(selector)).group(1).split("/")
            self.brand = combo.get("brand").get("name")
            self.name = combo.get("name")
            self.description = combo.get("description").split(". ")
        else:
            data = json.loads(self._extract_json(selector))
            self.skus = {}
            product = data.get("detail").get("products").pop()
            sku = Sku(product)
            sku.currency = data.get("currencyCode")
            if price:
                price = selector.css('span.price[id*="old-price"]::text').extract_first()
                print(price)
                sku.previous_prices.append(float(re.search(r"\d+[\.|,]\d+", price).group().replace(",", ".")))
            self.skus.update({sku.sku_id: sku})
            self.retailer_sku = data.get("id")
            self.category = product.get("category").split("/")
            self.brand = 'LIUJO'
            self.name = product.get("name")
            self.description = selector.xpath('//div[@class="short-description-value"]//text()').extract()
            self.description = ''.join(''.join(self.description).strip().splitlines()).split(". ")
        self.gender = "girls"
        self.image_urls = selector.css(".slide>a>img::attr(data-more-views)").extract()
        self.care = []
        self.url = url

    def _extract_json(self, selector):
        for text in selector.css('script[type="text/javascript"]::text').extract():
            if "ecommerce" in text:
                return self._validate_name(re.search(r"ecommerce': (\{[\n\s\S]+][\n\s]+\})", text).group(1))

    @staticmethod
    def _validate_name(string):
        name = re.search(r"[\"|\']name[\"|\']: *\"(.*)", string).group(1)[0:-2]
        new_name = name.replace('"', '\\"')
        name = name.replace("'", '"')
        string = string.replace("'", '"')
        string = string.replace(name, new_name)
        return string

    def _validate_json(self, string):
        description = re.search(r"\"description\": *\"(.*)", string).group(1)[0:-2]
        new_description = description.replace('"', '\\"')
        description = description.replace("'", "\"")
        string = self._validate_name(string)
        string = string.replace(description, new_description)
        return string



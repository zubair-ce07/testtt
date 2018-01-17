import scrapy
import re
from urllib.parse import urljoin
import json
from sfera.items import SferaItem


class Sfera(scrapy.Spider):
    name = "sfera_crawler"
    start_urls = ["https://www.sfera.com/es/"]
    product_details_api = "https://www.sfera.com/one/mod/_lista_carga.php"

    def parse(self, response):
        categories_content = response.xpath('//div[@class="mac_obj_enlace"]/@onclick').extract()
        for sub_category_content in categories_content:
            sub_category_url = urljoin(response.url, re.search('\(.+\'', sub_category_content).group()[2:-1])
            yield scrapy.Request(url=sub_category_url, dont_filter=True, callback=self.parse_sub_categories)

    def form_data_detials(self, response):
        return response.xpath('//script[contains(text(),"fil1=new Array()")]/text()').extract_first()

    def form_data_castel_ids(self, response):
        ids_content = self.form_data_detials(response)
        form_data = {}
        castel_values = re.findall('\d{4}', ids_content)
        castel_keys = ["catsel1", "catsel2", "catsel3"]
        for castel_key, castel_value in zip(castel_keys, castel_values):
            form_data[castel_key] = castel_value
        return form_data

    def form_data_fil_id2(self, response):
        fil4b_details = self.form_data_detials(response)
        return re.search('fil4b=\d+', fil4b_details).group()[6:]

    def form_data_fil_id1(self, response):
        fil4a_details = self.form_data_detials(response)
        return re.search('fil4a=\d+', fil4a_details).group()[6:]

    def form_data_num_id(self, response):
        num_details = self.form_data_detials(response)
        return re.search('mite=\'\d+', num_details).group()[6:]

    def language(self, response):
        lang_details = self.form_data_detials(response)
        return re.search('lis_n1=\'\w+', lang_details).group()[8:]

    def gender(self, response):
        category = response.xpath('//div[@id="cab_texto"]//h2/a/text()').extract_first()
        genders = {
            "Mujer": "Women",
            "Hombre": "Men",
            "Niños & Bebés": "Baby Boys",
        }
        try:
            return genders[category]
        except KeyError:
            return "Adults"

    def brand(self, response):
        brand = response.xpath('//title/text()').extract_first().split('|')
        return brand[-1]

    def categories(self, response, item_details):
        return item_details["categorias"]

    def map_urlc(self, response, item_details):
        return item_details["mapa_urlc"].strip()[4:]

    def url_code(self, response, item_details):
        return item_details["urlc"].strip()

    def original_url(self, response, item_details):
        refer_code = item_details["reference_code"].strip()
        return '%s%s%s/%s' % (self.start_urls[0], self.map_urlc(response, item_details),
                              self.url_code(response, item_details), refer_code)

    def price(self, response, item_details):
        price = item_details["precio"]
        return int(price.replace('.', ''))

    def images(self, response, item_details):
        images_detail = item_details["lista_imgs"]
        return images_detail.split(',')

    def previous_price(self, response, item_details):
        previous_price = item_details["precio_ant"]
        return int(previous_price.replace('.', ''))

    def stock_exist_or_not(self, response, item_details):
        if item_details["stock"] == "1":
            return "available"
        else:
            return "out_of_stock"

    def color(self, response, item_details):
        return item_details["nomref"]

    def available_sizes(self, response, item_details):
        sizes = item_details["tallas"]
        if sizes:
            return sizes.split(',')
        return ["none"]

    def trails(self, response, item_details):
        return [["", self.start_urls[0]], [self.categories(response, item_details)[1],
                                           '%s%s' % (self.start_urls[0], self.map_urlc(response, item_details))]]

    def parse_sub_categories(self, response):
        item = SferaItem()
        item["gender"] = self.gender(response)
        item["brand"] = self.brand(response)
        form_data = self.form_data_castel_ids(response)
        form_data["numlimite"] = self.form_data_num_id(response)
        form_data["listaver"] = "2"
        form_data["ordenar"] = "0"
        form_data["numpag"] = "1"
        form_data["n1"] = self.language(response)
        form_data["fil4a"] = self.form_data_fil_id1(response)
        form_data["fil4b"] = self.form_data_fil_id2(response)
        form_data["nomargin"] = "1"
        form_data["tipolista"] = "0"
        form_data["esweb"] = "1"
        form_data["esficha"] = "0"
        form_data["verlista"] = "2"
        form_data["ancho"] = "1298"
        yield scrapy.FormRequest(url=self.product_details_api, meta={"item": item}, formdata=form_data,
                                 dont_filter=True, callback=self.parse_product)

    def skus(self, response, item_details):
        skus = []
        for size in self.available_sizes(response, item_details):
            skus_details = {}
            skus_details["size"] = size
            skus_details["price"] = self.price(response, item_details)
            skus_details["previous_price"] = self.previous_price(response, item_details)
            skus_details["stock"] = self.stock_exist_or_not(response, item_details)
            skus_details["color"] = self.color(response, item_details)
            skus_details["sku_id"] = self.color(response, item_details)
            skus_details["currency"] = "EUR"
            skus.append(skus_details)
        return skus
        
    def parse_product(self, response):
        item = response.meta["item"]
        products_text = response.xpath('//script[contains(text(),"lrefsver.push")]/text()').extract()
        for product_text in products_text:
            json_content = re.search('({.+})', product_text).group()
            item_details = json.loads(json_content)
            item["description"] = item_details["descripcion"]
            item["title"] = item_details["nombre"]
            item["images"] = self.images(response, item_details)
            item["categories"] = self.categories(response, item_details)
            item["url_original"] = self.original_url(response, item_details)
            item["skus"] = self.skus(response, item_details)
            item["trails"] = self.trails(response, item_details)
            item["retailer_sku"] = item_details["id"]
            yield item




import scrapy
import re
from urllib.parse import urljoin
import json
from sfera.items import SferaItem


class SferaParser(scrapy.Spider):
    start_urls = ["https://www.sfera.com/es/"]
    product_details_api = "https://www.sfera.com/one/mod/_lista_carga.php"
    genders = {
        "Mujer": "Women",
        "Hombre": "Men",
        "Niños & Bebés": "Baby Boys",
    }

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
        return re.findall('fil4b=\d+', fil4b_details)[0][6:]

    def form_data_fil_id1(self, response):
        fil4a_details = self.form_data_detials(response)
        return re.findall('fil4a=\d+', fil4a_details)[0][6:]

    def form_data_num_id(self, response):
        num_details = self.form_data_detials(response)
        return re.findall('mite=\'\d+', num_details)[0][6:]

    def language(self, response):
        lang_details = self.form_data_detials(response)
        return re.findall('lis_n1=\'\w+', lang_details)[0][8:]

    def gender(self, response):
        categories = response.xpath('//div[@id="cab_texto"]//h2/a/text()').extract()
        for category in categories:
            return self.genders.get(category) or 'Adults'

    def brand(self, response):
        return response.xpath('//div[@id="cab_ic_inicio"]//img/@alt').extract_first()

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

    def parse_product(self, response):
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


class SferaCrawler(SferaParser):
    name = "sfera_crawler"

    def parse(self, response):
        categories_content = response.xpath('//div[@class="mac_obj_enlace"]/@onclick').extract()
        for sub_category_content in categories_content:
            sub_category_url = response.urljoin(re.findall('\(.+\'', sub_category_content)[0][2:-1])
            yield scrapy.Request(url=sub_category_url, dont_filter=True, callback=self.parse_sub_categories)

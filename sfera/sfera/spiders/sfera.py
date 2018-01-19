import scrapy
import re
from scrapy.spiders import spiders
from urllib.parse import urljoin
import json
from sfera.items import SferaItem
from sfera.spiders.sfera_parser import SferaParser


class SferaCrawler(scrapy.Spider):
    name = "sfera_crawler"
    parse_spider = SferaParser()

    def parse(self, response):
        categories_content = response.xpath('//div[@class="mac_obj_enlace"]/@onclick').extract()
        for sub_category_content in categories_content:
            sub_category_url = response.urljoin(re.findall('\(.+\'', sub_category_content)[0][2:-1])
            yield scrapy.Request(url=sub_category_url, dont_filter=True, callback=self.parse_sub_categories)

    def form_data_detials(self, response):
        return response.xpath('//script[contains(text(),"fil1=new Array()")]/text()').extract_first()

    def brand(self, response):
        return response.xpath('//div[@id="cab_ic_inicio"]//img/@alt').extract_first()

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
                                 dont_filter=True, callback=self.parse_spider.parse)

# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response, open_in_browser
from ..items import ProdcutItemLoader


class CocooncenterRuleSpider(CrawlSpider):
    name = 'cocooncenter_rule'
    allowed_domains = ['cocooncenter.com']
    start_urls = ['http://cocooncenter.com/']

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "DOWNLOAD_DELAY": 0.5,
    }

    rules = (
        Rule(LinkExtractor(restrict_css=[".nav", "#pagination"]), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css=".bloc_nom"), callback="parse_product")
    )

    def parse_item(self, response):
        pass

    def parse_product(self, response):
        product_il = ProdcutItemLoader(response=response)
        product_il.add_xpath("category", "//*[contains(@itemtype, 'BreadcrumbList')]/"
                                         "span[@itemprop='itemListElement'][2]//span/text()")
        product_il.add_xpath("segment_1", "//*[contains(@itemtype, 'BreadcrumbList')]/"
                                          "span[@itemprop='itemListElement'][3]//span/text()")
        product_il.add_xpath("segment_2", "//*[contains(@itemtype, 'BreadcrumbList')]/"
                                          "span[@itemprop='itemListElement'][4]//span/text()")
        product_il.add_xpath("segment_3", "//*[contains(@itemtype, 'BreadcrumbList')]/"
                                          "span[@itemprop='itemListElement'][5]//span/text()")
        product_il.add_xpath("segment_4", "//*[contains(@itemtype, 'BreadcrumbList')]/"
                                          "span[@itemprop='itemListElement'][6]//span/text()")

        product_il.add_xpath("name", "//*[@class='titre_produit']//text()")

        product_il.add_xpath("brand", "//*[@itemprop='brand']//text()")

        product_il.add_xpath("form", "//*[@class='type_packaging_fiche_produit']//text()")

        product_il.add_xpath("price", "//*[@class='prix_fiche_produit']//"
                                      "*[contains(@id, 'prix_fiche_produit_')]//text()")

        eans_multi = response.xpath("//*[contains(@value, 'EAN')]/@id").extract()
        eans_single = response.xpath("//*[contains(text(), 'EAN')]/text()").re('EAN\s:\s(\d+)')
        if eans_single:
            # image_url = response.css("#div_image a::attr(href)").extract_first()
            product_il.add_value("ean", eans_single)
            product_il.add_css("image_urls", "#div_image a::attr(href)")

            yield product_il.load_item()

        if eans_multi:
            for ean_id in eans_multi:
                product_il_var = ProdcutItemLoader(item=product_il.load_item().copy(), response=response)
                product_il_var.add_xpath("ean", "//*[@id='{}']/@value".format(ean_id))
                product_il_var.add_xpath("variant", "//*[@id='{}']/@value".format(ean_id.replace("ean", "txt")))
                product_il_var.add_xpath("image_urls", "//*[@id='{}']/@value".format(ean_id.replace("ean", "img")))

                yield product_il_var.load_item()

        variant_request_body = ("id={}&type=produit&type_fiche=normal&liste_info_modif%5B2%5D=1"
                                "&liste_info_modif%5B3%5D=1&liste_info_modif%5B5%5D=1&liste_info_modif%5B6%5D="
                                "1&liste_info_modif%5B7%5D=1&liste_info_modif%5B11%5D=1&liste_info_modif%5B12%5D=1"
                                "&liste_info_modif%5Bcab%5D=0&id_pays=31")
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

        if not (eans_single or eans_multi):
                variant_ids = response.css('#cpd_res_selector_3 div[id^="cpd_pays_"]::attr(id)').re(r'\d+')[1:]
                variant_names = response.css('#cpd_res_selector_3 div[id^="cpd_pays_"]'
                                             ' .span_designation_attribut_selector::text').extract()
                for variant_id, variant_name in zip(variant_ids, variant_names):
                    yield scrapy.Request(url="https://www.cocooncenter.com/index/fiche/modifInfo",
                                         body=variant_request_body.format(variant_id),
                                         headers=headers,
                                         method="POST",
                                         callback=self.parse_variant,
                                         dont_filter=True,
                                         meta={"item": product_il.load_item(),
                                               "name": variant_name})

    def parse_variant(self, response):
        product_il = ProdcutItemLoader(item=response.meta["item"].copy(), response=response)
        data = json.loads(response.text)
        product_il.add_value("ean", data["information"]["ean"])
        product_il.add_value("variant", response.meta["name"])
        product_il.add_value("image_urls", data["zoom_img_url"])

        yield product_il.load_item()

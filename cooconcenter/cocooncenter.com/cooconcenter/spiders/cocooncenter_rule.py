# -*- coding: utf-8 -*-
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

        eans_multi = response.xpath("//*[contains(@value, 'EAN')]/@value").re('EAN\s:\s(\d+)')
        eans_single = response.xpath("//*[contains(text(), 'EAN')]/text()").re('EAN\s:\s(\d+)')

        if not eans_single:
            if not eans_multi:
                # inspect_response(response, self)
                yield {"url": response.url}
        product_il.add_value("ean", eans_single)
        product_il.add_value("ean", eans_multi)

        # yield product_il.load_item()

        # inspect_response(response, self)

# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from damall.items import Product


class DamallSpider(CrawlSpider):
    name = 'Damall'
    allowed_domains = ['damart.co.uk']
    start_urls = ['http://damart.co.uk/']
    rules = (
            Rule(LinkExtractor(
                allow=('\d'),
                restrict_css='.ss_menu_bloc'),
                callback='parse_listing',),
            )

    def parse_listing(self, response):
        product_urls = self.get_products_urls(response)
        next_page = self.get_next_page(response)
        for url in product_urls:
            yield Request(url=url, callback=self.parse_product)
        sublisting_urls = self.get_sublisting_urls(response)
        for url in sublisting_urls:
            yield Request(url=url, callback=self.parse_listing)
        if next_page:
            yield Request(url=next_page, callback=self.parse_listing)

    def parse_product(self, response):
        product = Product()
        product["Id"] = self.get_product_id(response)
        product["name"] = self.get_product_name(response)
        product["urls"] = [response.url]
        product["product_imgs"] = self.get_product_imgs(response)
        product["description"] = self.get_product_description(response)
        product["care"] = self.get_product_care(response)
        product["skus"] = {}
        product["brand"] = "DaMall"
        product["price"] = self.get_product_price(response)
        colors_names, colors_urls = self.get_product_colors(response)
        color_url = colors_urls[len(colors_urls)-1]
        colors_urls.pop()
        yield Request(color_url,
                      method='POST',
                      headers={'X-Requested-With': 'XMLHttpRequest'},
                      callback=self.get_product_variants,
                      dont_filter=True,
                      meta={
                          "product": product,
                          "c_names": colors_names,
                          "c_urls": colors_urls})
    
    def get_next_page(self, response):
        url = response.css(".next::attr(href)").extract_first()
        return response.urljoin(url)

    def get_sublisting_urls(self, response):
        urls = response.css(".ss_menu_bloc a::attr(href)").extract()
        return [response.urljoin(url) for url in urls]

    def get_products_urls(self, response):
        urls = response.css(".k-catalog a::attr(href)").extract()
        return [response.urljoin(url) for url in urls]

    def get_product_imgs(self, response):
        imgs = response.css(".thumblist a::attr(href)").extract()
        return [response.urljoin(img) for img in imgs]

    def get_product_id(self, response):
        return re.search(r'P-\d*', response.url).group(0)

    def get_product_name(self, response):
        return response.css(".product-data h1::text").extract_first()

    def get_product_description(self, response):
        desc = response.css(
            ".description p::text, .description ul::text").extract()
        return "".join(desc)

    def get_product_price(self, response):
        price = response.css(".no_promo::text, .no_promo span::text").extract()
        return "".join(price).strip()

    def get_product_colors(self, response):
        colors_names = response.css(".picto_color img::attr(alt)").extract()
        colors_urls = response.css(".picto_color a::attr(href)").extract()
        return colors_names, colors_urls

    def get_product_care(self, response):
        care = response.css(".description_frame div::text").extract()
        return "".join(care).strip()

    def get_product_sizes(self, response):
        raw = json.loads(response.body.decode('utf-8'))
        raw = raw['inits'][2]['initDDdSlickComponent'][0]["ddData"]
        sizes = []
        is_out_of_stock = []
        for raw_txt in raw:
            sizes.append(raw_txt["text"])
            if raw_txt["description"] == "Out of stock":
                is_out_of_stock.append(False)
            else:
                is_out_of_stock.append(True)
        return sizes, is_out_of_stock

    def get_product_variants(self, response):
        colors_names = response.meta["c_names"]
        colors_urls = response.meta["c_urls"]
        product = response.meta["product"]
        skus = self.get_product_skus(response)
        colors_names.pop()
        product["skus"].update(skus)
        if not colors_urls:
            yield product
        else:
            color_url = colors_urls[len(colors_urls)-1]
            colors_urls.pop()
            yield Request(color_url,
                          method='POST',
                          headers={'X-Requested-With': 'XMLHttpRequest'},
                          callback=self.get_product_variants,
                          dont_filter=True,
                          meta={
                            "product": product,
                            "c_names": colors_names,
                            "c_urls": colors_urls})

    def get_product_skus(self, response):
        colors_names = response.meta["c_names"]
        product = response.meta["product"]
        sizes, is_out_of_stock = self.get_product_sizes(response)
        skus = {}
        for itr, size in enumerate(sizes):
            skus.update({
                "{}_{}_{}".format(
                    product["Id"], size, colors_names[len(colors_names)-1]): {
                    "color": colors_names[len(colors_names)-1],
                    "currency": "EUR",
                    "price": product["price"],
                    "size": size,
                    "is_out_of_stock": is_out_of_stock[itr]
                }
            })
        return skus

# -*- coding: utf-8 -*-
import json
import scrapy
from fashionPakistan.items import FashionPakistan


class CrossstitchComSpider(scrapy.Spider):
    name = 'crossstitch.pk'
    my_public_ip = "116.58.62.58"       #used to set local currency
    start_urls = ['https://www.crossstitch.pk/Common/SetCurrencyByIp?ip='+my_public_ip]

    def parse(self, response):
        yield scrapy.Request("https://www.crossstitch.pk", self.crawl_crossstitch)
        

    def crawl_crossstitch(self, response):
        category_links = response.xpath(
            "//ul[@class='top-menu']/li/a/@href").extract()
        for link in category_links:
            yield scrapy.Request(response.urljoin(link)+"?pagenumber=1", self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath(
            "//div[@class='picture ']/a/@href").extract()
        for link in product_links:
            yield scrapy.Request(response.urljoin(link), self.parse_product_details, dont_filter=True)

        if product_links:
            pagenumber = int(response.url[response.url.find("=")+1:])
            pagenumber = pagenumber + 1
            yield scrapy.Request(response.urljoin("?pagenumber="+str(pagenumber)), self.parse_product_links)

    def parse_product_details(self, response):
        product = FashionPakistan()
        product["name"] = self.get_item_name(response)
        product["product_sku"] = self.get_item_sku(response)
        product["description"] = self.get_item_description(response)
        product["images"] = self.get_item_images(response)
        product["attributes"] = self.get_item_attributes(response)
        product["out_of_stock"] = self.is_out_of_stock(response)
        product["url"] = response.url
        product["skus"] = self.get_item_skus(response)
        sizes, sizes_keys = self.get_item_sizes(response)

        p_id = int(response.xpath("//div[@data-productid]/@data-productid").extract_first())
        sku_link = "https://www.crossstitch.pk/shoppingcart/productdetails_attributechange?productId={}&validateAttributeConditions=False&loadPicture=True".format(p_id)
        form_data = {
            "product_attribute_{}".format(p_id-29): sizes_keys[0]
        }
        def parse_price(response):
            nonlocal product, sizes, sizes_keys, sku_link, p_id
            json_resp = json.loads(response.text)
            product["skus"][sizes[0]+"_"+sizes_keys[0]]["price_now"] = json_resp["price"]
            sizes = sizes[1:]
            sizes_keys = sizes_keys[1:]
            if sizes:
                form_data = {
                    "product_attribute_{}".format(p_id-29): sizes_keys[0]
                }
                yield scrapy.FormRequest(sku_link, formdata=form_data, callback=parse_price)
            else:
                yield product

        yield scrapy.FormRequest(sku_link, formdata=form_data, callback=parse_price)

    def is_out_of_stock(self, response):
        p_id = response.xpath("//div[@data-productid]/@data-productid").extract_first()
        value = response.xpath("//input[@id='add-to-cart-button-{}']/@value".format(p_id))
        if value == "Out of Stock":
            return True
        else:
            return False

    def get_item_name(self, response):
        return response.xpath("//h1[@itemprop='name']/text()").extract_first().strip()

    def get_item_sku(self, response):
        return response.xpath("//span[@itemprop='sku']/text()").extract_first()

    def get_item_description(self, response):
        return response.xpath("//div[@itemprop='description']/p/text()").extract()

    def get_item_images(self, response):
        images = response.xpath("//div[@class='owl-carousel']//img/@src").extract()
        return images

    def get_item_attributes(self, response):
        attribute = response.xpath("//ul[@id='tabs']//a/text()").extract()
        attributes = {}
        for attrib in attribute:
            attributes[attrib] = [desc.strip() for desc in response.xpath("//div[@id='{}']/p/text()".format(attrib)).extract()]
        return attributes

    def get_item_sizes(self, response):
        sizes = response.xpath("//select[contains(@id, 'product_attribute_')]/option/text()").extract()
        size_keys = response.xpath("//select[contains(@id, 'product_attribute_')]/option/@value").extract()
        return sizes, size_keys

    def get_item_skus(self, response):
        available_sizes, size_keys = self.get_item_sizes(response)
        prev_price = response.xpath("//div[@class='old-product-price']/span/text()").extract_first()
        currency_code = response.xpath("//meta[@itemprop='priceCurrency']/@content").extract_first()
        color_scheme = {}
        if prev_price:
            for size, key in zip(available_sizes, size_keys):
                color_scheme[size+"_"+key]={
                    "prev_price": prev_price,
                    "size": size,
                    "currency_code": currency_code,
                }
            
        else:
            for size, key in zip(available_sizes, size_keys):
                color_scheme[size+"_"+key]={
                    "size": size,
                    "currency_code": currency_code,
                }
        return color_scheme
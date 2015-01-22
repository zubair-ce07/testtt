# -*- coding: utf-8 -*-
from galeria.items import GaleriaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import re
import requests


class GaleriaspiderSpider(CrawlSpider):
    name = "galeriaSpider"
    allowed_domains = ["www.galeria-kaufhof.de"]
    start_urls = (
        'http://www.galeria-kaufhof.de/',
    )
    # allowed categories
    shop_categories = [u"Damen", u"Herren", u"Kinder", u"Schuhe", u"Uhren", u"Wäsche", u"Taschen & Koffer"]
    product_categories = [u"Badehose", u"Badeschuhe", u"Badeshorts", u"BH", u"Bikini", u"Blusen",
                          u"Boots", u"Daypacks", u"Fleecejacken", u"Freizeithemden", u"Funktionsjacken",
                          u"Fußballschuhe", u"Geldbörsen", u"Handschuhe", u"Helme", u"Hemden", u"HosenJacken",
                          u"Joggingschuhe",
                          u"Kappen", u"Kleider", u"Kulturbeutel", u"Lange Unterhose", u"Leggings", u"Mäntel",
                          u"Multifunktionstücher",
                          u"Mützen", u"Pants", u"Pullover", u"Röcke", u"Shirtjacken", u"Shorts", u"Skihosen",
                          u"Skijacken",
                          u"Sneaker", u"Socken", u"Armbänder",
                          u"Armband mit Anhänger", u"Armreifen", u"Damenuhren", u"Ketten / Colliers",
                          u"Ketten mit Anhänger",
                          u"Ohrschmuck", u"Ringe", u"Sets", u"Sportbrillen", u"Sporthosen", u"Sporttaschen", u"Stiefel",
                          u"Sweatjacken",
                          u"Sweatshirts", u"Taschen", u"Taucherbrillen", u"Wellness-Hosen", u"Wellness-Jacken",
                          u"Wellness-Shirts",
                          u"Tops", u"Trainingsanzüge", u"Trainingsschuhe", u"Trikots", u"T-Shirts", u"Walkingschuhe",
                          u"Damendüfte",
                          u"Herrendüfte", u"Zierkissen", u"Wohndecke", u"Waschhandschuh", u"Topfhandschuhe",
                          u"Tischläufer",
                          u"Tischdecke", u"Teppich", u"Strandlaken", u"Stoffe", u"Spannbettlaken", u"Sitzgelegenheiten",
                          u"Servietten",
                          u"Seiflappen", u"Schürzen", u"Saunalaken", u"Saunakilt", u"Schulranzen", u"Platzsets",
                          u"Nackenstützkissen", u"Nackenrolle"]

    products_page_xpath = '(.//*[@id="puePage"]//*[@class="module_PUE3_1x1_3erKachel"]/a)[position()<4]'
    pagination_xpath = './/*[@id="puePage"]//a[@class="nextPage"]'
    main_menu_items_xpath = './/*[@id="navBar"]/li[position()!=10 and position()!=26 ]/a'
    sub_menu_items_xpath = './/*[@class="leftNavigation"]//ul/li//li/a'
    rules = [

        Rule(LinkExtractor(deny=['Wein-Genuss', 'Wein', 'Spielwaren'], restrict_xpaths=main_menu_items_xpath)),
        Rule(LinkExtractor(deny=['PLAY', 'Wein-Genuss', 'Wein', 'Spielwaren', 'Sport-Sportarten-Ausruestung',
                                 'Sport-Specials-Fitnessgeraete',
                                 'Spielwaren-Kategorien-Baby-Kleinkind', 'Haushalt-Heimtextilien-Schreibwaren',
                                 'Haushalt-Heimtextilien-Kleinelektro', 'Haushalt-Heimtextilien-Handarbeiten',
                                 'Haushalt-Heimtextilien-Essen-und-Trinken'],restrict_xpaths=products_page_xpath,
                           attrs='content'), callback='get_product_detail'),
        Rule(LinkExtractor(restrict_xpaths=sub_menu_items_xpath)),
        Rule(LinkExtractor(restrict_xpaths=pagination_xpath))
    ]

    def get_skus(self, size):
        skus = {}
        for result in size:
            arr = {}
            arr['currency'] = 'Euro'
            arr['colour'] = result[0]
            arr['available'] = result[2]
            arr['size'] = result[1]
            arr['Price'] = result[3]
            skus[arr['size'] + u'_' + arr['colour']] = arr
        return skus

    def getimages(self,json_response,product_images):
        for image in json_response:
            product_images.append(image['image']['url'])

    def get_title(self, response):
        title = response.xpath('.//*[@id="pdsPage"]//*[@class="productHeading"]/text()') \
            .extract()[0]
        return title.strip()

    def get_care(self, response):
        care = response.xpath('.//*[@class="blurbInfo"]//p//text()') \
            .extract()
        strip_care = [item.strip() for item in care]
        if not strip_care:
            strip_care = ['N/A']
        return strip_care

    def get_category(self, response):
        category = response.xpath('.//*[@id="breadCrump"]//span[position()>1]/a/@title') \
            .extract()
        strip_category = [item.strip() for item in category]
        return strip_category

    def get_description(self, response):
        description = response.xpath('.//*[@id="cmp_productdatasheet"]//td[not(contains(@class,"label"))]/text()') \
            .extract()
        strip_description = [item.strip() for item in description]
        return strip_description

    def get_price(self, response):
        new_price = response['product']['price']['shownPrice']
        old_price = response['product']['price']['crossPrice']
        currency_symbol = response['product']['price']['currencySign']
        if currency_symbol not in str(new_price):
            new_price = str(new_price) + currency_symbol
        if old_price:
            if currency_symbol not in str(old_price):
                old_price = str(old_price) + currency_symbol
                return {'new_price': new_price,
                        'old_price': old_price}
        else:
            return new_price

    def color_details(self, size_with_price, colors, product_images):
        for colourid in colors:
            request_url_ne = 'http://www.galeria-kaufhof.de/store/view/productdetail/' \
                             + colourid + '?channel=desktop'
            new_response = requests.get(request_url_ne)
            new_response.raise_for_status()
            json_response = new_response.json()
            if json_response['product']['variantAttributes']:
                new_attributes = json_response['product']['variantAttributes']
                if new_attributes[0] and new_attributes[0]['variantAttribute']['variantType'] == "COLOR":
                    for attributes_value in new_attributes[0]['variantAttribute']['values']:
                        if attributes_value['value']['available']:
                            if (attributes_value['value']['hybrisId'] == colourid):
                                colorname = attributes_value['value']['parameter']['marketingColorName']
                if new_attributes[1] and new_attributes[1]['variantAttribute']['label'] == u"Größe":
                    for size_attribute in new_attributes[1]['variantAttribute']['values']:
                        price = self.get_price(json_response)
                        size = size_attribute['value']['parameter']['viewText']
                        available = size_attribute['value']['available']
                        size_with_price.append(
                            [colorname, size, available, price])
                else:
                    price = self.get_price(json_response)
                    size = [u'OneSize']
                    available = True
                    size_with_price.append([colorname, size, available, price])
                self.getimages(json_response['product']['productImages'],product_images)
            else:
                price = self.get_price(json_response)
                self.getimages(json_response['product']['productImages'],product_images)

                size_with_price.append([u'', u'OneSize', True, price])


    def get_product_detail(self, response):
        shop_categoryResponse = response.xpath(
            '//tr[contains(descendant::td,"Shop-Kategorie")]/td[not(contains(text(),"Shop-Kategorie"))]/text()').extract()[
            0]
        product_categoryResponse = response.xpath(
            './/tr[contains(descendant::td,"Produktkategorie")]/td[not(contains(text(),"Produktkategorie"))]/text()').extract()[
            0]
        if (product_categoryResponse in self.product_categories) or (shop_categoryResponse in self.shop_categories):
            item = GaleriaItem()
            colors = []
            product_images = []
            size_with_price = []
            item['title'] = self.get_title(response)
            item['category'] = self.get_category(response)
            item['url'] = url = response.url
            item['spider_name'] = self.name
            item['retailer'] = 'galeria-kaufhof'
            item['description'] = self.get_description(response)
            item['care'] = self.get_care(response)
            if url:
                match = re.search("/(\d+)$", url)
                productid = match.group(1)
            request_url = 'http://www.galeria-kaufhof.de/store/view/productdetail/' + productid + '?channel=desktop'
            new_response = requests.get(request_url)
            new_response.raise_for_status()
            json_response = new_response.json()
            for attributes in json_response['product']['variantAttributes']:
                if attributes['variantAttribute']['variantType'] == "COLOR":
                    for attributes_value in attributes['variantAttribute']['values']:
                        if attributes_value['value']['available']:
                            colors.append(attributes_value['value']['hybrisId'])
                        else:
                            if json_response['product']['variantAttributes'][1]:
                                size_attribute = json_response['product']['variantAttributes'][1]
                                if size_attribute['variantAttribute']['label'] == u"Größe":
                                    for size_attribute_value in size_attribute['variantAttribute']['values']:
                                        price = self.get_price(json_response)
                                        color = attributes_value['value']['parameter']['marketingColorName']
                                        size = size_attribute_value['value']['parameter']['viewText']
                                        available = False
                                        size_with_price.append([color, size, available, price])
                            else:
                                price = self.get_price(json_response)
                                size = [u'OneSize']
                                available = True
                                size_with_price.append([color, size, available, price])
            if not colors:
                color = json_response['product']['hybrisId']
                colors = [color]
            self.color_details(size_with_price, colors, product_images)
            skus = self.get_skus(size_with_price)
            item['image_urls'] = product_images
            item['skus'] = skus
            yield item

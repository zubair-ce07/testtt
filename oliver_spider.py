# -*- coding: utf-8 -*-
import re
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
import logging
from scrapy.http import Request
import json


logging.basicConfig(level=logging.DEBUG,
                    format='(%(processName)-10s) %(message)s',  #: Output the Process Name just for checking purposes
                    )


class Mixin(object):
    retailer = 'oliverbonas'
    allowed_domains = ['www.oliverbonas.com']
    pfx = ['https://www.oliverbonas.com/api/category/fashion/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/jewellery/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/accessories/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/furniture/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/homeware/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/homeware/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/clothing/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/furniture/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/jewellery/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/fashion-accessories/verbosity/3']

    #: source : https://www.oliverbonas.com/js/app.min.js
    sizes = {'1127': '11" x 14"', '930': "120 x 60cm", '927': "120x170cm", '928': "140x200cm", '929': "160x230cm",
             '1068': "17mm", '931': "180x120cm", '1067': "19mm", '1076': "2-3 Year", '1124': '3" x 4"',
             '619': "32A", '612': "32B", '613': "32C", '614': "32D", '629': "34A", '615': "34B", '616': "34C",
             '617': "34D", '626': "36/37", '618': "36B", '610': "36C", '611': "36D", '627': "38/39",
             '1129': '4" x 4"', '1075': "4-7", '628': "40/41", '932': "44x74cm", '1126': '5" x 7"',
             '1125': '6" x 4"', '1128': '6" x 4"', '362': "One Size", '1065': "Size 6", '845': "Size 7",
             '1064': "Size 8", '1066': "Size 9", '119': "O/S", '503': '1', '400': '2', '502': '4', '497': '5',
             '522': "3-4", '519': "3-4", '520': "5-6", '521': "7-8", '501': "SML", '499': "SML", '500': "LGE",
             '389': "S/52", '390': "M/54", '391': "L/56", '518': '2" x 2"', '517': '3" x 5"', '129': '4"x4"',
             '120': '4"x6"', '130': '5"x7"', '131': '6"x4"', '466': '8"x10"', '186': "XS", '135': "S",
             '136': "M", '137': "L", '138': "XL", '363': "S/M", '364': "M/L", '218': "8/XS", '222': "10/S",
             '221': "12/M", '219': "14/L", '220': "16/XL", '146': "0-3 Mnth", '157': "3-6 Mnth",
             '116': "6-12 Mnth", '461': "6-18 Mnth", '442': "0-1 Year", '150': "1-2 Year", '883': "2-3 Year",
             '884': "3-4 Year", '174': '3', '498': '6', '166': '8', '172': '10', '365': '12', '366': '14',
             '208': '16', '209': '26', '196': '27', '197': '28', '210': '29', '212': '30', '213': '31',
             '585': '32', '431': '36', '205': '37', '432': '38', '433': '39', '434': '40', '436': '41',
             '435': '42', '430': '52', '429': '54', '428': '56', '251': "60X90", '401': "Small",
             '1043': "Medium", '361': "Large", '402': "Extra Large"}

    colors = {1081: "Apple", 451: "Aqua", 424: "Beige", 474: "Biscuit", 61: "Black", 437: "Blk/ivy",
              410: "Blossom", 58: "Blue", 489: "Bluetit", 463: "Bright Red", 441: "Bright red", 59: "Brown",
              457: "Camellia", 470: "Clear", 409: "Clover", 408: "Cobalt", 286: "Copper", 290: "Coral",
              476: "Cream", 411: "Crocus", 412: "Currant", 452: "Damson", 1140: "Dark Blue", 454: "Duckegg",
              453: "Duckegg Lemon", 413: "Dusk", 414: "Emerald", 526: "Fuchsia", 415: "Fuschia", 67: "Gold",
              450: "Granite", 523: "Graphite", 459: "Grass", 70: "Green", 60: "Grey", 1108: "Gunmetal",
              455: "Heather", 426: "Ivory", 407: "Jade", 456: "Lemongrass", 1141: "Light Blue",
              1121: "Light Pink", 1087: "Linen", 416: "Marine", 472: "Mink", 288: "Mint", 62: "Multi",
              425: "Navy", 289: "Neon", 468: "Neon Orange", 469: "Neon Pink", 524: "Noir", 417: "Ocean",
              65: "Orange", 525: "Pale Jade", 1083: "Pale Jade", 471: "Pastel", 427: "Peach", 1086: "Pebble",
              1084: "Petal", 69: "Pink", 1088: "Pistachio", 419: "Primrose", 66: "Purple", 473: "Raspberry",
              418: "Raven", 68: "Red", 490: "Robin", 625: "Rose Gold", 1082: "Saffron", 64: "Silver",
              406: "Slate", 284: "Tan", 1085: "Taupe", 475: "Taupe", 283: "Teal", 487: "Thrush",
              287: "Turquoise", 460: "Vermillion", 488: "Wagtail", 63: "White", 71: "Yellow", 458: "Zinnia",
              602: "Black", 506: "Blue", 603: "Brown", 600: "Clear", 594: "Gold", 595: "Green", 598: "Grey",
              592: "Multi", 591: "Orange", 601: "Pink", 596: "Purple", 599: "Red", 590: "Silver",
              597: "White", 593: "Yellow"}

    brands = {637: "50Fifty Gifts", 1135: "Alice Scott", 638: "Apples to Pears Gift LTD", 640: "Archivist Limited",
              1120: "Aroma Home", 646: "Artebene LTD", 648: "Auteur LTD", 656: "Bajo", 662: "Ballon Rouge",
              933: "Bando", 841: "Bath House", 667: "Best Years", 817: "Big Tomato Company", 1111: "Black & Blum",
              680: "BlackBlum", 683: "Broste", 697: "CanovaGifts", 700: "ChronicleStationery", 1146: "CicoBooks",
              704: "Coach House Antiques", 1100: "Container Group", 1093: "Corkcicle", 711: "Cubic", 715: "Doiy",
              1116: "Donkey", 716: "Donkey Products", 1143: "Electric Jelly", 1148: "Elisa Werbler", 717: "Firebox",
              1107: "Funtime", 1092: "Gamago", 1059: "Gift Republic", 1112: "Ginger Fox", 1113: "Graphique",
              1131: "Happy Jackson", 633: "Hey Holla", 1091: "Host", 719: "House of Marbles,Bovey Tracy", 721: "J-ME",
              720: "Jasmine Living", 723: "Kabloom", 1149: "Kakkoii", 1130: "Katie Leamon", 818: "Keep Cup LTD",
              1114: "Kikkerland", 733: "Kikkerland,Kikkerland Europe B", 1139: "KING & MCGAW LTD", 1102: "Knock Knock",
              735: "Korres Natural Products", 1117: "Lagoon", 1150: "Laurence King", 782: "Luckies", 780: "Mama Mio",
              1094: "Men's Society", 1095: "Men's Society", 1109: "Meri Meri", 1119: "Mustard",
              798: "Natural Products", 816: "Newgate Clocks", 1136: "Nineteen Seventy Three", 1030: "Olly B",
              842: "Orange Tree Toys", 1089: "Ototo", 821: "Outliving", 1101: "Paladone", 820: "Petit Jour",
              1151: "Pluto Produkter", 819: "Pols Potten", 822: "Pom Pom Galore", 823: "Present Time",
              1118: "Professor Puzzle", 1132: "Putinki Oy", 1133: "Raspberry Blossom", 824: "Rex International",
              826: "RiceA/S", 1145: "Ridley's Games Room", 825: "Root7", 1142: "Safari Life", 828: "Sew Heart Felt",
              827: "Sifcon", 830: "Sophie Arcari", 1057: "Spinning Hat", 829: "Sting in the Tail",
              1134: "Stop the Clock", 832: "Studio Roof", 1144: "SUCK UK", 831: "Suck UK", 907: "Sunnylife Australia",
              833: "Talking Tables", 834: "Taylors Eye Witness", 1115: "Te Neues", 835: "Temerity Jones",
              1147: "Thabto London", 1137: "The Art File", 839: "The Wrap Paper LTD", 838: "Trans Pacific LTD",
              837: "Uberstar", 836: "Vintage Playing Cards", 1058: "Viski", 1090: "Viski", 840: "Wildand Wolf",
              1110: "Wolfand Wolf", 256: "Oliver Bonas", 26: "Poem", 28: "Vero Moda", 280: "Vila", 586: "Bobble",
              25: "Emily & Fin", 496: "Fred & Friends", 511: "Jennie Maizels", 510: "LSA", 513: "Rogerlaborde",
              27: "Sugarhill Boutique", 514: "Suki", 507: "Temerity Jones of London", 279: "Zatchels"}


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = Mixin.pfx


class OliverBonasParseSpider(BaseParseSpider):

    image_url_t = " https://thumbor-gc.tomandco.uk/unsafe/fit-in/950x665/center/middle/smart" \
                  "/filters:fill(white)/www.oliverbonas.com//static/media/catalog/%s"

    #: Callback function
    def parse(self, response):

        if response.body == '[]':
            #: It means product don't has any data
            return None

        jsn = json.loads(response.body)
        product = jsn['product'][0]

        #: Initialize the garment object by giving it a unique id
        garment = self.new_unique_garment(str(product['id']))
        if garment is None:
            return

        self.boilerplate_minimal(garment, response)

        #: Setting parameters for a garment
        garment['price'] = clean(str(product['price']))
        garment['currency'] = "GBP"
        garment['spider_name'] = self.name
        garment['brand'] = self.product_brand(jsn)
        garment['image_urls'] = clean(self.image_urls(jsn))
        garment['name'] = product['meta']['title'].split(' - ')[0]
        garment['description'] = self.product_description(product)
        garment['category'] = self.product_category(product)
        garment['url_original'] = self.product_original_url(product)
        garment['care'] = self.product_care(product)
        if 'homeware' in response.url or 'furniture' in response.url:
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = "Women"

        #: Initializing skus Dictionary to avoid errors in further processing
        garment['meta'] = {'requests_queue': self.skus_requests(jsn)}
        garment['skus'] = {}

        return self.next_request_or_garment(garment)

    def parse_parent(self, response):
        garment = response.meta['garment']
        jsn = json.loads(response.body)
        #: Extract children_list of all skus
        children_list = ','.join(str(e) for e in jsn['product'][0]['options']['configurable']['children'])
        #: Form a URL
        url = "https://www.oliverbonas.com/api/product/" + children_list + "/verbosity/3"
        garment['meta']['requests_queue'] += [Request(url, callback=self.parse_skus)]

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        jsn = json.loads(response.body)
        #: Update the sku element of garment
        garment['skus'].update(self.skus(jsn))
        #: Now check their stock information
        url = re.sub('/[0-9]$', '/1', response.url).replace('product', 'stock')
        garment['meta']['requests_queue'] += [Request(url, callback=self.parse_oos)]

        return self.next_request_or_garment(garment)

    def skus(self, jsn):

        skus = {}
        for product in jsn['product']:
            #: Set Color
            color = self.colors.get(product.get('color')) or self.colors.get(product.get('colors', [''])[0]) or ''

            #: Set Size
            #: Check whether size exists or not
            if 'size' in product:
                size = self.sizes[str(product['size'])]
            else:
                size = self.one_size

            sku = {
                'price': product['price'],
                'currency': "GBP",
                'size': size,
                'colour': color,
            }
            if 'org_price' in product:
                sku['previous_price'] = product['org_price']

            skus[color + "_" + size] = sku

        return skus

    def parse_oos(self, response):
        garment = response.meta['garment']
        key_list = garment['skus'].keys()
        jsn = json.loads(response.body)
        for key, stock in zip(key_list, jsn['stock']):
            #: Updating sku
            garment['skus'][key]['out_of_stock'] = 'isOut' in stock

        return self.next_request_or_garment(garment)

    def product_care(self, product):
        return product.get('info')

    def product_category(self, product):
        return [label['label'] for label in product['breadcrumbs']]

    def product_original_url(self, product):
        return 'https://www.oliverbonas.com' + product["url"]

    def product_description(self, product):
        return clean([product['meta'].get('description'), product.get('short_description', '')])

    def image_urls(self, jsn):
        return [self.image_url_t % image['image'] for image in jsn['product'][0].get('media')]

    def product_brand(self, jsn):
        return self.brands[jsn['product'][0].get('brand', 256)]

    def skus_requests(self, json_data):
        queue = []
        product = json_data['product'][0]
        #: check for parent which has all related sku information
        if 'parent' in product:
            #: Go to parent to extract all sku information
            url = "https://www.oliverbonas.com/api/product/" + str(product['parent']) + "/verbosity/3"
            queue += [Request(url, callback=self.parse_parent)]

        elif product['options']:
            #: Check if it is the parent itself and has children children_list itself
            #: Extract children_list of all skus
            children_list = ','.join(str(e) for e in product['options']['configurable']['children'])
            #: Form a URL
            url = "https://www.oliverbonas.com/api/product/" + children_list + "/verbosity/3"
            queue += [Request(url, callback=self.parse_skus)]
        else:
            #: If a product does not have a parent nor a children
            #: It means a product has only one sku
            #: Form a URL
            url = "https://www.oliverbonas.com/api/product/" + str(product['id']) + "/verbosity/3"
            queue += [Request(url, callback=self.parse_skus)]

        return queue


class OliverBonasCrawlSpider(BaseCrawlSpider, Mixin):

    def parse_start_url(self, response):
        #: Updating the trail information
        trail_part = self.add_trail(response)
        jsn = json.loads(response.body)
        for product in jsn['category'][0]['products']:
            url = 'https://www.oliverbonas.com/api/product/' + str(product['id']) + '/verbosity/2'
            yield Request(url, callback=self.parse_urls,  meta={'trail': trail_part})

    def parse_urls(self, response):
        #: Updating the trail information
        trail_part = self.add_trail(response)
        jsn = json.loads(response.body)
        # Check product response is empty
        if jsn['product']:
            url = 'https://www.oliverbonas.com/api/product' + jsn['product'][0]['url'] + '/verbosity/3'
            yield Request(url, callback=self.parse_item,  meta={'trail': trail_part})

    def add_trail(self, response):
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        trail_part = response.meta.get('trail', []) + trail_part
        return trail_part


class OliverBonasUKParseSpider(OliverBonasParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class OliverBonasUKCrawlSpider(OliverBonasCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = OliverBonasUKParseSpider()



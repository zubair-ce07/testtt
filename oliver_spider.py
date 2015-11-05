# -*- coding: utf-8 -*-
import re
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import logging
from scrapy.http import Request
import json


logging.basicConfig(level=logging.DEBUG,
                    format='(%(processName)-10s) %(message)s',  #: Output the Process Name just for checking purposes
                    )


sizes = {'1127': {'11" x 14"'}, '930': {"120 x 60cm"}, '927': {"120x170cm"}, '928': {"140x200cm"}, '929': {"160x230cm"},
        '1068': {"17mm"}, '931': {"180x120cm"}, '1067': {"19mm"}, '1076': {"2-3 Year"}, '1124': {'3" x 4"'},
        '619': {"32A"}, '612': {"32B"}, '613': {"32C"}, '614': {"32D"}, '629': {"34A"}, '615': {"34B"}, '616': {"34C"},
        '617': {"34D"}, '626': {"36/37"}, '618': {"36B"}, '610': {"36C"}, '611': {"36D"}, '627': {"38/39"},
        '1129': {'4" x 4"'}, '1075': {"4-7"}, '628': {"40/41"}, '932': {"44x74cm"}, '1126': {'5" x 7"'},
        '1125': {'6" x 4"'}, '1128': {'6" x 4"'}, '362': {"One Size"}, '1065': {"Size 6"}, '845': {"Size 7"},
        '1064': {"Size 8"}, '1066': {"Size 9"}, '119': {"O/S"}, '503': {'1'}, '400': {'2'}, '502': {'4'}, '497': {'5'},
        '522': {"3-4"}, '519': {"3-4"}, '520': {"5-6"}, '521': {"7-8"}, '501': {"SML"}, '499': {"SML"}, '500': {"LGE"},
        '389': {"S/52"}, '390': {"M/54"}, '391': {"L/56"}, '518': {'2" x 2"'}, '517': {'3" x 5"'}, '129': {'4"x4"'},
        '120': {'4"x6"'}, '130': {'5"x7"'}, '131': {'6"x4"'}, '466': {'8"x10"'}, '186': {"XS"}, '135': {"S"},
        '136': {"M"}, '137': {"L"}, '138': {"XL"}, '363': {"S/M"}, '364': {"M/L"}, '218': {"8/XS"}, '222': {"10/S"},
        '221': {"12/M"}, '219': {"14/L"}, '220': {"16/XL"}, '146': {"0-3 Mnth"}, '157': {"3-6 Mnth"},
        '116': {"6-12 Mnth"}, '461': {"6-18 Mnth"}, '442': {"0-1 Year"}, '150': {"1-2 Year"}, '883': {"2-3 Year"},
        '884': {"3-4 Year"}, '174': {'3'}, '498': {'6'}, '166': {'8'}, '172': {'10'}, '365': {'12'}, '366': {'14'},
        '208': {'16'}, '209': {'26'}, '196': {'27'}, '197': {'28'}, '210': {'29'}, '212': {'30'}, '213': {'31'},
        '585': {'32'}, '431': {'36'}, '205': {'37'}, '432': {'38'}, '433': {'39'}, '434': {'40'}, '436': {'41'},
        '435': {'42'}, '430': {'52'}, '429': {'54'}, '428': {'56'}, '251': {"60X90"}, '401': {"Small"},
        '1043': {"Medium"}, '361': {"Large"}, '402': {"Extra Large"}}

colors = {1081: {"Apple"}, 451: {"Aqua"}, 424: {"Beige"}, 474: {"Biscuit"}, 61: {"Black"}, 437: {"Blk/ivy"},
          410: {"Blossom"}, 58: {"Blue"}, 489: {"Bluetit"}, 463: {"Bright Red"}, 441: {"Bright red"}, 59: {"Brown"},
          457: {"Camellia"}, 470: {"Clear"}, 409: {"Clover"}, 408: {"Cobalt"}, 286: {"Copper"}, 290: {"Coral"},
          476: {"Cream"}, 411: {"Crocus"}, 412: {"Currant"}, 452: {"Damson"}, 1140: {"Dark Blue"}, 454: {"Duckegg"},
          453: {"Duckegg Lemon"}, 413: {"Dusk"}, 414: {"Emerald"}, 526: {"Fuchsia"}, 415: {"Fuschia"}, 67: {"Gold"},
          450: {"Granite"}, 523: {"Graphite"}, 459: {"Grass"}, 70: {"Green"}, 60: {"Grey"}, 1108: {"Gunmetal"},
          455: {"Heather"}, 426: {"Ivory"}, 407: {"Jade"}, 456: {"Lemongrass"}, 1141: {"Light Blue"},
          1121: {"Light Pink"}, 1087: {"Linen"}, 416: {"Marine"}, 472: {"Mink"}, 288: {"Mint"}, 62: {"Multi"},
          425: {"Navy"}, 289: {"Neon"}, 468: {"Neon Orange"}, 469: {"Neon Pink"}, 524: {"Noir"}, 417: {"Ocean"},
          65: {"Orange"}, 525: {"Pale Jade"}, 1083: {"Pale Jade"}, 471: {"Pastel"}, 427: {"Peach"}, 1086: {"Pebble"},
          1084: {"Petal"}, 69: {"Pink"}, 1088: {"Pistachio"}, 419: {"Primrose"}, 66: {"Purple"}, 473: {"Raspberry"},
          418: {"Raven"}, 68: {"Red"}, 490: {"Robin"}, 625: {"Rose Gold"}, 1082: {"Saffron"}, 64: {"Silver"},
          406: {"Slate"}, 284: {"Tan"}, 1085: {"Taupe"}, 475: {"Taupe"}, 283: {"Teal"}, 487: {"Thrush"},
          287: {"Turquoise"}, 460: {"Vermillion"}, 488: {"Wagtail"}, 63: {"White"}, 71: {"Yellow"}, 458: {"Zinnia"},
          602: {"Black"}, 506: {"Blue"}, 603: {"Brown"}, 600: {"Clear"}, 594: {"Gold"}, 595: {"Green"}, 598: {"Grey"},
          592: {"Multi"}, 591: {"Orange"}, 601: {"Pink"}, 596: {"Purple"}, 599: {"Red"}, 590: {"Silver"},
          597: {"White"}, 593: {"Yellow"}}

brands = {637: "50FiftyGifts", 1135: "AliceScott", 638: "ApplestoPearsGiftLTD", 640: "ArchivistLimited",
          1120: "AromaHome", 646: "ArtebeneLTD", 648: "AuteurLTD", 656: "Bajo", 662: "BallonRouge",
          933: "Bando", 841: "BathHouse", 667: "BestYears", 817: "BigTomatoCompany", 1111: "Black&Blum",
          680: "BlackBlum", 683: "Broste", 697: "CanovaGifts", 700: "ChronicleStationery", 1146: "CicoBooks",
          704: "CoachHouseAntiques", 1100: "ContainerGroup", 1093: "Corkcicle", 711: "Cubic", 715: "Doiy",
          1116: "Donkey", 716: "DonkeyProducts", 1143: "ElectricJelly", 1148: "ElisaWerbler", 717: "Firebox",
          1107: "Funtime", 1092: "Gamago", 1059: "GiftRepublic", 1112: "GingerFox", 1113: "Graphique",
          1131: "HappyJackson", 633: "HeyHolla", 1091: "Host", 719: "HouseofMarbles,BoveyTracy", 721: "J-ME",
          720: "JasmineLiving", 723: "Kabloom", 1149: "Kakkoii", 1130: "KatieLeamon", 818: "KeepCupLTD",
          1114: "Kikkerland", 733: "Kikkerland,KikkerlandEuropeB", 1139: "KING&MCGAWLTD", 1102: "KnockKnock",
          735: "KorresNaturalProducts", 1117: "Lagoon", 1150: "LaurenceKing", 782: "Luckies", 780: "MamaMio",
          1094: "Men'sSociety", 1095: "Men'sSociety", 1109: "MeriMeri", 1119: "Mustard",
          798: "NaturalProducts", 816: "NewgateClocks", 1136: "NineteenSeventyThree", 1030: "OllyB",
          842: "OrangeTreeToys", 1089: "Ototo", 821: "Outliving", 1101: "Paladone", 820: "PetitJour",
          1151: "PlutoProdukter", 819: "PolsPotten", 822: "PomPomGalore", 823: "PresentTime",
          1118: "ProfessorPuzzle", 1132: "PutinkiOy", 1133: "RaspberryBlossom", 824: "RexInternational",
          826: "RiceA/S", 1145: "Ridley'sGamesRoom", 825: "Root7", 1142: "SafariLife", 828: "SewHeartFelt",
          827: "Sifcon", 830: "SophieArcari", 1057: "SpinningHat", 829: "StingintheTail",
          1134: "StoptheClock", 832: "StudioRoof", 1144: "SUCKUK", 831: "SuckUK", 907: "SunnylifeAustralia",
          833: "TalkingTables", 834: "TaylorsEyeWitness", 1115: "TeNeues", 835: "TemerityJones",
          1147: "ThabtoLondon", 1137: "TheArtFile", 839: "TheWrapPaperLTD", 838: "TransPacificLTD",
          837: "Uberstar", 836: "VintagePlayingCards", 1058: "Viski", 1090: "Viski", 840: "WildandWolf",
          1110: "WolfandWolf", 256: "OliverBonas", 26: "Poem", 28: "VeroModa", 280: "Vila", 586: "Bobble",
          25: "Emily&Fin", 496: "Fred&Friends", 511: "JennieMaizels", 510: "LSA", 513: "Rogerlaborde",
          27: "SugarhillBoutique", 514: "Suki", 507: "TemerityJonesofLondon", 279: "Zatchels"}

class Mixin(object):
    retailer = 'oliver'
    allowed_domains = ['www.oliverbonas.com']
    pfx = ['https://www.oliverbonas.com/api/category/fashion/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/jewellery/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/accessories/category/all/verbosity/3']

    '''pfx = ['https://www.oliverbonas.com/api/category/fashion/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/jewellery/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/accessories/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/furniture/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/homeware/category/all/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/homeware/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/clothing/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/furniture/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/jewellery/verbosity/3',
           'https://www.oliverbonas.com/api/category/sale/category/fashion-accessories/verbosity/3']'''


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = Mixin.pfx


class OliverParseSpider(BaseParseSpider):

    #: Callback function
    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        json_data = json.loads(response.body)

        #: Initialize the garment object by giving it a unique id
        garment = self.new_unique_garment(str(json_data['product'][0]['id']))
        if garment is None:
            return

        self.boilerplate_normal(garment, hxs, response)

        #: check for industry if homeware or furniture set it to homeware
        if 'homeware' in response.url or 'furniture' in response.url:
            garment['industry'] = 'homeware'

        #: Setting parameters for a garment
        garment['price'] = clean(str(json_data['product'][0]['price']))
        garment['currency'] = "GBP"
        garment['spider_name'] = self.name
        garment['gender'] = "Womens"
        garment['brand'] = self.product_brands(json_data)
        #: garment['brand'] = clean(json_data['product'][0]['meta']['title'].split(' - ')[2])
        garment['image_urls'] = clean(self.image_urls(json_data))
        queue = self.skus(json_data)
        #: Passing garment as meta data for each request
        queue = map(
            lambda x: x.replace(meta={'item': garment, 'dont_redirect': True}),
            queue)
        garment['meta'] = {}
        garment['meta']['requests_queue'] = queue

        garment['name'] = json_data['product'][0]['meta']['title'].split(' - ')[0]

        garment['description'] = [json_data['product'][0]['meta']['description']]

        if 'features' in json_data['product'][0]:
            garment['description'] += [json_data['product'][0]['features']]
        if 'short_description' in json_data['product'][0]:
            garment['description'] += [json_data['product'][0]['short_description']]
        if 'info' in ['product'][0]:
            garment['care'] = json_data['product'][0]['info']

        garment['category'] = []
        for label in json_data['product'][0]['breadcrumbs']:
            garment['category'].append(label['label'])

        original_url = re.sub('/verbosity/3', '', response.url)
        original_url = re.sub('/api/product', '', original_url)
        garment['url_original'] = original_url

        #: Initializing Image_urls list and skus Dictionary to avoid
        #: errors in further processing
        garment['skus'] = {}
        garment['meta']['key_list'] = []

        return self.next_request_or_garment(garment)

    def image_urls(self, json_data):
        images = json_data['product'][0]['media']
        list = []
        for image in images:
            image = image['image']
            list.append(" https://thumbor-gc.tomandco.uk/unsafe/fit-in/950x665/center/middle/smart"
                        "/filters:fill(white)/www.oliverbonas.com//static/media/catalog/" + image)
        return list

    def product_brands(self, json_data):
        brand_id = json_data['product'][0]['brand']
        brand = brands[brand_id]
        return brand

    def skus(self, json_data):
        queue = []
        #: check for parent which has all related sku information
        if 'parent' in json_data['product'][0]:

            logging.info("Condition 1")
            #: got to parent to extract all sku information
            url = "https://www.oliverbonas.com/api/product/" + str(json_data['product'][0]['parent']) + "/verbosity/3"
            queue += [Request(url, callback=self.parse_parent)]

        elif json_data['product'][0]['options']:
            logging.info("condition 2")
            #: Check if it is the parent itself and has children list itself
            #: Extract list of all skus
            list = ','.join(str(e) for e in json_data['product'][0]['options']['configurable']['children'])
            #: Form a URL
            url = "https://www.oliverbonas.com/api/product/"+ list + "/verbosity/3"
            req = Request(url, callback=self.parse_skus, priority=3000000)
            queue += [req]
        else:
            logging.info("condition 3")
            #: if a product does not have a parent nor a children
            #: It means a product has only one sku
            #: Form a URL
            url = "https://www.oliverbonas.com/api/product/"+ str(json_data['product'][0]['id']) + "/verbosity/3"
            req = Request(url, callback=self.parse_skus)
            queue += [req]

        return queue

    def parse_parent(self, response):

        garment = response.meta['item']
        json_data = json.loads(response.body)
        #: Extract list of all skus
        list = ','.join(str(e) for e in json_data['product'][0]['options']['configurable']['children'])
        #: Form a URL
        url = "https://www.oliverbonas.com/api/product/"+ list + "/verbosity/3"
        req = Request(url, callback=self.parse_skus, meta={'item': garment})

        garment['meta']['requests_queue'] += [req]
        return self.next_request_or_garment(garment)

    def parse_skus(self, response):

        logging.info("In parse_skus")
        garment = response.meta['item']
        json_data = json.loads(response.body)
        skus = {}

        for product in json_data['product']:
            if 'info' not in garment and 'info' in product:
                garment['care'] = product['info']

            logging.info("In loop")
            if 'color' in product:
                color = list(colors[product['color']])
            elif 'colors' in product:
                color = list(colors[product['colors'][0]])
            else:
                color = ['no_color_mentioned']

            color = color[0]
            #: check whether size exists or not
            if 'size' in product:
                size = list(sizes[str(product['size'])])[0]
            else:
                size = 'one-size'
            key = color + "_" + size
            sku = {
                'price': product['price'],
                'currency': "GBP",
                'size': size,
                'colour': color,
            }
            if 'org_price' in product:
                sku['previous_price'] = product['org_price']

            skus[key] = sku
            #: This list is needed in checking out_of_stock
            garment['meta']['key_list'] += [key]

        #: Update the sku element of garment
        garment['skus'].update(skus)

        #: Now check their stock information
        url = re.sub('/[0-9]$', '/1', response.url)
        url = re.sub('product', 'stock', url)
        logging.info(url)
        req = Request(url, callback=self.parse_stock, meta={'item': garment})

        garment['meta']['requests_queue'] += [req]
        return self.next_request_or_garment(garment)

    def parse_stock(self, response):

        logging.info("I am in parse_stock")
        logging.info(response.url)
        garment = response.meta['item']
        key_list = garment['meta']['key_list']
        json_data = json.loads(response.body)

        index = 1
        for key, stock in zip(key_list, json_data['stock']):
            #: Updating sku
            garment['skus'][key]['out_of_stock'] = 'isOut' in stock
            index += 1

        return self.next_request_or_garment(garment)

    def product_name(self, hxs):
        return None

    def product_description(self, hxs):
        return None

    def product_care(self, hxs):
        return None


class OliverCrawlSpider(BaseCrawlSpider, Mixin):


    def parse_start_url(self, response):

        #: Updating the trail information
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        trail_part = response.meta.get('trail', []) + trail_part

        ids = re.findall('"id":(\d*)', response.body)[1:]
        ids = ','.join(ids)
        url = 'https://www.oliverbonas.com/api/product/' + ids + '/verbosity/2'
        logging.info(url)
        req = Request(url, callback=self.parse_urls,  meta={'trail': trail_part})
        yield req

    def parse_urls(self, response):

        #: Reject all urls which are not under specified brands
        logging.info("In parse   urls   ")

        #: Updating the trail information
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        trail_part = response.meta.get('trail', []) + trail_part

        urls = re.findall('"url":"(.*?)"', response.body)
        urls = map(lambda x: 'https://www.oliverbonas.com/api/product' + x + '/verbosity/3', urls)
        urls = urls[-2:]
        for url in urls:
            yield Request(url, callback=self.parse_item,  meta={'trail': trail_part})


class OliverUKParseSpider(OliverParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class OliverUKCrawlSpider(OliverCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = OliverUKParseSpider()



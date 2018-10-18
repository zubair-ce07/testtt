# import scrapy
# import json
# import re
#
# from scrapy.selector import Selector
# from urllib.parse import urljoin, urlencode
#
# from ScrapyPractice.items import ProductItem
# from ScrapyPractice.items import SizeItem
# from ScrapyPractice.items import VariationItem
#
#
# class MangoSpider(scrapy.Spider):
#     # cmdarguement : {country}
#     name = "Mangospider"
#
#     def start_requests(self):
#         """
#         starts requests from the menu header with country code (take country code provided from command line)
#         the reponse to this request will be string in json format
#         :return:
#         """
#         start_url = 'https://shop.mango.com/services/menus/header/'
#         country_code = self.country
#
#         link = urljoin(start_url, country_code.upper())
#         yield scrapy.Request(link, callback=self.parse)
#
#     def parse(self, response):
#         """
#         take json string reponse convert it into dictionary and look up for menus
#         and sub menus for each category displayed on site and make request for each category
#         :param response: json object string containing header menus and submenus
#         :return:
#         """
#         menus = [menu for menu in json.loads(response.text)['menus'] if menu['type'] == 'BRAND' and menu['id'] == 'she']
#         # link = menus[1]['menus']['2'][8]['link']
#         # yield scrapy.Request(link, callback=self.parse_listings)
#         for menu in menus:
#             submenus = menu['menus']
#             if len(submenus) > 1:
#                 for listings in submenus.values():
#                     listings = listings[1:]
#                     for category in listings:
#                         if category['type'] in ['prendas', 'accesorios']:
#                             yield scrapy.Request(category['link'], callback=self.parse_listings)
#             else:
#                 age_category = submenus['1']
#                 for age_menu in age_category:
#                     age_submenus = age_menu['menus']
#                     for listings in age_submenus.values():
#                         listings = listings[1:]
#                         for category in listings:
#                             if category['type'] in ['prendas', 'accesorios']:
#                                 yield scrapy.Request(category['link'], callback=self.parse_listings)
#
#     def parse_listings(self, response):
#         """
#         find the params for the url that on request returns json for all products in that category
#         and put these params in url to make request
#         there params are in a viewObjectJson var in a script int he sourse page fo that category
#         :param response: html page for each category in listings
#         :return:
#         """
#         yield {
#             'res': response,
#         }
#         product_list_link = 'https://shop.mango.com/services/productlist/products/{}/{}/{}/'
#
#         site_response = response.xpath('//script[contains(text(),"viewObjectsJson")]/text()').extract()
#         if site_response:
#             script_text = site_response[0].strip()
#
#             data_dict_text = re.search('viewObjectsJson(.*)}}}', script_text).group(0)[18:]
#             data_dict = json.loads(data_dict_text)
#             if 'catalogParameters' in data_dict.keys():
#                 catalog_parameters = data_dict['catalogParameters']
#
#                 request_link = product_list_link.format(
#                     # 'GB',
#                     # 'she',
#                     # 'sections_she_NewNowEspecial_MidSeasonSale.prendas_she'
#                     catalog_parameters["isoCode"],
#                     catalog_parameters["idShop"],
#                     catalog_parameters['idSection'],
#                 )
#                 optionalparams = {}
#                 if 'optionalParams' in catalog_parameters:
#                     optional_parameters = catalog_parameters['optionalParams']
#                     if 'idSubSection' in optional_parameters:
#                         optionalparams['idSubSection'] = optional_parameters['idSubSection']
#                     if 'menu' in optional_parameters:
#                         optionalparams['menu'] = optional_parameters['menu'][0]
#
#                 if optionalparams:
#                     params = ''
#                     for key, value in optionalparams.items():
#                         params += key + '=' + value + '&'
#                     params = params[:-1]
#                     request_link += '?' + params
#
#                 # params='?idSubSection=vestidos_she&menu=familia;32'
#                 # request_link += '?' + params
#
#             #   yield scrapy.Request(request_link, callback=self.parse_products)
#
#     def parse_products(self, response):
#         """
#         takes json object string and look for each item int hat product list and collect required data.
#         then makes a requests to get stock-id that is required later to get breadcrumbs and description
#         of relative product
#         :param response: contains json object string for all the products int hat category
#         :return:
#         """
#         products_data = json.loads(response.text)
#
#         groups = products_data['groups']
#         if groups:
#             garments = groups[0]['garments']
#
#             for garment in garments.values():
#                 product_items = ProductItem()
#                 is_discounted = True if garment['price']['discountRate'] > 0 else False
#
#                 variations_list = []
#                 for color in garment['colors']:
#                     variations = VariationItem(display_color_name=color['label'], images_urls=color['images'])
#
#                     size_list = []
#                     for size in color['sizes']:
#                         size_item = SizeItem(size_name=size['label'])
#
#                         if size['stock'] > 0:
#                             size_item['is_available'] = True
#                         size_item['price'] = garment['price']['crossedOutPrices'][0][1:]
#                         size_item['is_discounted'] = is_discounted
#                         size_item['discounted_price'] = ''
#                         if is_discounted:
#                             size_item['discounted_price'] = garment['price']['salePriceNoCurrency']
#                         size_list.append(size_item)
#
#                     variations['sizes'] = size_list
#                     variations_list.append(variations)
#
#                 product_id = garment['garmentId']
#                 lang = garment['price']['locale']['language']
#                 country = garment['price']['locale']['country']
#                 product_url = garment['colors'][0]['linkAnchor']
#
#                 product_items['product_url'] = product_url
#                 product_items['store_keeping_unit'] = product_id
#                 product_items['title'] = garment['shortDescription']
#                 product_items['brand'] = garment['analyticsEventsData']['brand']
#                 product_items['locale'] = lang + '_' + country
#                 product_items['currency'] = garment['price']['currency']
#                 product_items['variations'] = variations_list
#
#                 stockid_url = 'https://shop.mango.com/services/stock-id'
#                 yield scrapy.Request(
#                     stockid_url,
#                     meta={'product': product_items},
#                     dont_filter=True,
#                     callback=self.parse_stockid,
#                 )
#
#     def parse_stockid(self, response):
#         """
#         collects the json dict for stock id and passes it on along with the product item to breadcrumbs request
#         :param response: contains json dictionary that have the stock-id
#         :return:
#         """
#         stockid = json.loads(response.text)['key']
#         product_items = response.meta['product']
#         product_id = product_items['store_keeping_unit']
#         headers = {
#             ":authority": "shop.mango.com",
#             ":method": "GET",
#             ":path": "/services/garments/{}/breadcrumb".format(product_id),
#             ":scheme": "https",
#             "stock-id": stockid,
#             "referer": product_items['product_url'],
#         }
#         breadcrumbs_url = 'https://shop.mango.com/services/garments/{}/breadcrumb'.format(product_id)
#
#         yield scrapy.Request(
#             breadcrumbs_url,
#             meta={'product': product_items, 'stockid': stockid},
#             headers=headers,
#             callback=self.parse_breadcrumbs
#         )
#
#     def parse_breadcrumbs(self, response):
#         """
#         takes json response and parse it to collect the breadcrumbs add them to product item and make
#         further request
#         :param response: json dictionary object string
#         :return:
#         """
#
#         data = json.loads(response.text)
#
#         product_items = response.meta['product']
#         product_items['breadcrumbs'] = data['breadcrumb']
#
#         product_id = product_items['store_keeping_unit']
#         stockid = response.meta['stockid']
#         description_url = 'https://shop.mango.com/services/garments/{}'.format(product_id)
#
#         headers = {
#             ":authority": "shop.mango.com",
#             ":method": "GET",
#             ":path": "/services/garments/{}".format(product_id),
#             ":scheme": "https",
#             "stock-id": stockid,
#             "referer": product_items['product_url'],
#         }
#         yield scrapy.Request(
#             description_url,
#             meta={'product': product_items, 'stockid': stockid},
#             headers=headers,
#             callback=self.parse_description,
#         )
#
#     def parse_description(self, response):
#         """
#         take json object dictionary and parse it to collect description collect it and add it to product item and then
#         yield product item
#         :param response: json object dictionary
#         :return:
#         """
#         data_dict = json.loads(response.text)
#         description = ''
#
#         for text in data_dict['details']['descriptions'].values():
#             if isinstance(text, list):
#                 description += ' '.join(text)
#             else:
#                 description += text
#             description += ' '
#
#         product_items = response.meta['product']
#         product_items['description'] = description
#
#         yield product_items

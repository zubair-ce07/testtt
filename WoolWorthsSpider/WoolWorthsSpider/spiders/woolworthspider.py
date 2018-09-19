# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import FormRequest
from WoolWorthsSpider.items import WoolworthsItem


class WoolworthspiderSpider(scrapy.Spider):
    name = 'woolworthspider'

    def start_requests(self):
        cat_url = (
            'https://www.woolworths.com.au/apis/ui/'
            'PiesCategoriesWithSpecials/'
        )
        yield scrapy.Request(url=cat_url, callback=self.parse_categories)

    def parse_categories(self, response):
        categories = json.loads(response.body)['Categories']
        for category in categories:
            request_url = (
                'https://www.woolworths.com.au/apis/ui/browse/category'
            )
            items_per_page = 36
            category_name = category['UrlFriendlyName']
            sub_categories = category['Children']
            for sub_category in sub_categories:
                sub_cat_name = sub_category['UrlFriendlyName']
                sub_cat_id = sub_category['NodeId']
                sub_cat_description = sub_category['Description']
                sub_cat_url = "shop/browse/{}/{}".format(
                    category_name,
                    sub_cat_name
                )
                item_count = int(sub_category['ProductCount'])
                total_pages = int(item_count/items_per_page) + 1
                for page_number in range(1, total_pages+1):
                    payload = {
                        "categoryId": sub_cat_id,
                        "pageNumber": page_number,
                        "sortType": "TraderRelevance",
                        "url": sub_cat_url,
                        "formatObject": json.dumps(
                            {"name": sub_cat_description}),
                    }
                    headers = {
                        'content-type': 'application/json;charset=UTF-8',
                    }

                    yield FormRequest(
                        request_url,
                        method='POST',
                        body=json.dumps(payload),
                        headers=headers,
                        callback=self.parse_items,
                    )

    def parse_items(self, response):
        data = json.loads(response.body)
        bundles = data['Bundles']
        for bundle in bundles:
            product = WoolworthsItem()
            item = bundle['Products'][0]
            attributes = item['AdditionalAttributes']

            product['name'] = item['Name']
            product['cup_price'] = item['CupPrice']
            product['price'] = item['Price']
            product['old_price'] = item['WasPrice']
            product['saving'] = item['SavingsAmount']
            product['is_new'] = item['IsNew']
            product['is_special'] = item['IsOnSpecial']
            product['brand'] = item['Brand']
            product['detail'] = attributes['description']
            product['ingredients'] = attributes['ingredients']
            product['allergens'] = attributes['allergencontains']

            energy = None
            carbohydrate = None
            fat = None
            protein = None
            sugar = None
            sodium = None
            nutrition_info = attributes['nutritionalinformation']
            if nutrition_info is not None:
                values = json.loads(nutrition_info)['Attributes']
                for index in range(len(values)):
                    if index == 0:
                        energy = values[index]['Value']
                    elif index == 1:
                        carbohydrate = values[index]['Value']
                    elif index == 2:
                        fat = values[index]['Value']
                    elif index == 3:
                        protein = values[index]['Value']
                    elif index == 4:
                        sugar = values[index]['Value']
                    elif index == 5:
                        sodium = values[index]['Value']

            product['nutrition'] = {
                'energy': energy,
                'carbohydrate': carbohydrate,
                'fat': fat,
                'protein': protein,
                'sugar': sugar,
                'sodium': sodium,
            }
            yield product

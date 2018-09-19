# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import FormRequest
from WoolWorthsSpider.items import WoolworthsItem


class WoolworthspiderSpider(scrapy.Spider):
    name = 'woolworthspider'
    start_urls = ['https://www.woolworths.com.au/']

    def parse(self, response):
        cat_url = (
            'https://www.woolworths.com.au/apis/ui/'
            'PiesCategoriesWithSpecials/'
        )
        yield scrapy.Request(url=cat_url, callback=self.parse_categories)

    def parse_categories(self, response):
        base_url = 'https://www.woolworths.com.au'

        cookies = (
            '__RequestVerificationToken=ZFU-G4yJxk9ylN0OGgp_b7H-xSbu1OIocg'
            'DLeE9vGSx0CLCKGfDKW37gam4egsbgY8ctCKmGBfibpPfq6m4Q8NuwWhzza9D'
            'tK0TatxAH6gG09Zu79XCcsOIHYZ65qYV_sZkD5yXeADzCJfqgOdHAWM0HPDop'
            'R_xR-ct8Yjzj93U1; ARRAffinity=c1bdc903bcd2227846e3946de8e3591'
            'de3913cbcd300c8f573c8b0c6bb6037fc; IR_gbd=woolworths.com.au; '
            'check=true; _ga=GA1.3.1852498160.1536846492; AMCVS_4353388057'
            'AC8D357F000101%40AdobeOrg=1; s_cc=true; aam_uuid=590557122718'
            '04846393009685998736373369; _gid=GA1.3.100108479.1537179903; '
            '_gcl_au=1.1.1843022315.1537234705; w-rctx=eyJhbGciOiJIUzI1NiI'
            'sInR5cCI6IkpXVCJ9.eyJuYmYiOjE1MzcyNTI1NDEsImV4cCI6MTUzNzI1NjE'
            '0MSwiaWF0IjoxNTM3MjUyNTQxLCJhdWQiOiJ3d3cud29vbHdvcnRocy5jb20u'
            'YXUiLCJzaWQiOiIwIiwidWlkIjoiNDUxOThjZmYtZTI4OC00NGNkLTg4NjQtY'
            'jQ4MDZjZGViMTA2IiwibWFpZCI6IjAiLCJhdXQiOiJTaG9wcGVyIiwiYXViIj'
            'oiMCIsImF1YmEiOiIwIn0.Ca_7WnLON8dh5jhOvXALE9Mchqvh6Ge82QvAzHe'
            'aisQ; AKA_A2=A; IR_7464=1537252547340%7C0%7C1537252547340; _g'
            'at_gtag_UA_38610140_9=1; AMCV_4353388057AC8D357F000101%40Adob'
            'eOrg=-330454231%7CMCIDTS%7C17792%7CMCMID%7C586023768533364781'
            '12982508739448463269%7CMCAAMLH-1537857348%7C6%7CMCAAMB-153785'
            '7348%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7'
            'CMCCIDH%7C315404628%7CMCOPTOUT-1537259748s%7CNONE%7CMCAID%7CN'
            'ONE%7CvVersion%7C3.1.2; AAMC_wfg_0=REGION%7C6%7CAMSYNCSOP%7C%'
            '7CAMSYNCS%7C; s_sq=%5B%5BB%5D%5D; rr_rcs=eF4FwbsNgDAMBcAmFbs8'
            'FP8SewPWCI4iUdAB83NXtvt7rrmTUAWZdDY2DQlDAFTePPJsc6V3rBEOpTbgw'
            'gZJi67p1Yh_bmERNw; utag_main=v_id:0165d33060530022909148dd10a'
            '002085001e07d00bd0$_sn:5$_ss:0$_st:1537254350001$vapi_domain:'
            'woolworths.com.au$ses_id:1537252545813%3Bexp-session$_pn:1%3B'
            'exp-session; mbox=PC#2b167ccf0378450bb61e50e46b393b6a.21_5#16'
            '00497350|session#5af387b2b6b840dc84fbca905c7e7ebd#1537254411;'
            ' ADRUM=s=1537252563255&r=https%3A%2F%2Fwww.woolworths.com.au%'
            '2Fshop%2Fbrowse%2Fspecials%2Fhalf-price%2Fmeat-seafood-deli%3F0'
        )
        user_agent = (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
            ' like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497'
            '.81 Safari/537.36'
        )
        request_key = (
            'gM5V8esLiOEpA-koCNGB70aVqZeycMVOMC1kdARHNNQxBltpp-_xxgaNKO'
            'cVxGFxFgdKSmNJ2R-sQXxDdielQmNFynsjBwR3XF8JFWxBU806Ct4MFrpX'
            'nzaPMrscm3Of37x67Je_4FUZbm2jLTxWjmN_maEFSH4PVoTLLIMFFFE1'
        )

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
                referrer_url = "{}/{}".format(base_url, sub_cat_url)
                item_count = int(sub_category['ProductCount'])
                total_pages = int(item_count/items_per_page) + 1
                for page_number in range(1, total_pages+1):
                    payload = {
                        "categoryId": sub_cat_id,
                        "pageNumber": page_number,
                        "pageSize": items_per_page,
                        "sortType": "TraderRelevance",
                        "url": sub_cat_url,
                        "location": sub_cat_url,
                        "formatObject": json.dumps(
                            {"name": sub_cat_description}),
                    }
                    headers = {
                        'origin': base_url,
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9',
                        'cookie': cookies,
                        'user-agent': user_agent,
                        'content-type': 'application/json;charset=UTF-8',
                        'accept': 'application/json, text/plain, */*',
                        'authority': 'www.woolworths.com.au',
                        'referer': referrer_url,
                        '__requestverificationtoken': request_key,
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

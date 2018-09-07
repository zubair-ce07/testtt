import scrapy
import json
import re
import ast

from scrapy import Request
from scrapy.selector import Selector

from ScrapyPractice.items import ProductItem, SizeItem, VariationItem


class DXLSpider(scrapy.Spider):
    name = "dxlspider"

    locale = ''
    currency = ''

    header_url = 'https://www.destinationxl.com/public/v1/currentUser/header'
    domain_url = 'https://www.destinationxl.com'
    site_url = 'https://www.destinationxl.com/mens-big-and-tall-store'
    # standard url format for getting product details, requires category_id and product_id
    urllink_to_product = "https://www.destinationxl.com/public/v1/dxlproducts/{}/{}"

    def start_requests(self):
        """
        start request with the header of website,
        Header contains currency and locale deatils and we will pass these down each request
        once parsed so we dont have to get them with each product
        :return: yield scrapy.Request Object
        """
        yield Request(
            url=self.header_url,
            callback=self.parse_locale,
        )

    def parse_locale(self, response):
        """
        Parses the locale information from website header, by making it into data dictionary,
        make a scrapy request to sites brands page to get all brands and call self.parse_menu_into_brands method to
        parse brands, also send locale information in meta
        :param response: json response against request
        :return: scrapy.Request object
        """
        # convert reponse.text into a data dictionary
        locale_data = json.loads(response.text)

        # url for brands page of website
        start_url = '{}/browse//mens-big-and-tall-store/brands/cat650032?format=json'.format(self.site_url)
        headers = {
            'referer': '{}/brands/cat650032'.format(self.site_url),
        }

        self.locale = 'en_' + locale_data['dxlCountry']
        self.currency = locale_data['dxlCurrency']

        yield Request(
            url=start_url,
            callback=self.parse_menu_into_brands,
            headers=headers,
        )

    def parse_menu_into_brands(self, response):
        """
        parses the json from menu into list of brands with brands names and brands links
        and call self.parse_brand method for each brand in the list
        :param response: json object
        :return:
        """
        response_dict = json.loads(response.text)
        html_for_brands = response_dict['contents'][0]['MainContent'][3]['content']
        html_for_brands = ''.join(html_for_brands.split())
        brands_list = re.search('brandName(.*)}];', html_for_brands).group(0)[10:-1]

        # convert string into a list object
        brands_list = ast.literal_eval(brands_list)

        # get the link of each brand in the list and make scrapy Request to that url,
        # Adding parameters Nrpp(number of record perpage)=10000 and format =json to scrape in callback method
        # Nrpp is set to 1000 because max allowed by website is 1000 this helps get most rec pr request
        # in case of more res than 1000 multiple requests will be made in next method
        for brand in brands_list:
            brand_url = brand['link']
            if 'search' in brand_url:
                request_url = '{}{}&Nrpp=10000&format=json'.format(self.domain_url, brand_url)
            else:
                request_url = '{}/browse/{}?Nrpp=10000&format=json'.format(self.site_url, brand_url)

            yield Request(
                url=request_url,
                callback=self.parse_brands,
            )

    def parse_brands(self, response):
        """
        get listings in each brand and make request for each product in listing one by one, according to need
        make a callback to parse_product for every item in listings
        :param response: json object
        :return: scrapy.Request object
        """

        products_list = []
        brand_details = json.loads(response.text)

        brand_url = brand_details.get('endeca:redirect', dict()).get('link', dict()).get('url', '')  # PX Clothing
        if brand_url:
            yield Request(
                url='{}{}&Nrpp=10000&format=json'.format(self.domain_url, brand_url),
                callback=self.parse_brands,
            )
            return

        main_content = brand_details.get('contents', [dict()])[0].get('MainContent', [])
        for content in main_content:
            details = content.get('contents', [dict()])[0]
            total_recs = details.get('totalNumRecs', -1)
            last_rec = details.get('lastRecNum', total_recs)
            if last_rec != total_recs:
                current_No = "No={}".format(last_rec)
                prev_No = 'No={}'.format(last_rec - 1000)
                if last_rec <= 1000:
                    url = '{}&{}'.format(response.request.url, current_No)
                else:
                    url = response.request.url.replace(prev_No, current_No)

                yield Request(
                    url=url,
                    callback=self.parse_brands,
                )
            products_list = details.get('records', [])
            if products_list:
                break

        if not products_list and main_content:
            html_for_brands = main_content[0].get('content', '')
            if html_for_brands:
                brands_records = Selector(text=html_for_brands).xpath(
                    './/img[@data-href]/@data-href').extract_first()

                query_params = '&Nrpp=10000&format=json'
                if '?' not in brands_records:
                    query_params = '?Nrpp=10000&format=json'

                url = '{}/browse/{}{}'.format(self.site_url, brands_records, query_params)
                yield Request(
                    url=url,
                    callback=self.parse_brands,
                )

        for product in products_list:
            category_id = product['attributes']['product.defaultCategoryId'][0]
            product_id = product['attributes']['product.repositoryId'][0]

            yield  Request(
                url= self.urllink_to_product.format(category_id, product_id),
                callback=self.parse_product,
            )

    def parse_product(self, response):
        """
        using json from response fill items of product and yield them
        :param response: json
        :return: yield ProductItem
        """
        product_details = json.loads(response.text)

        # object of product item with fields initallization
        product_item = ProductItem(
            product_url=self.site_url + product_details.get('webUrl', ''),
            store_keeping_unit=product_details.get('id', ''),
            title=product_details.get('description'),
            brand=product_details.get('brandName'),
            breadcrumbs=[
                crumb['name']
                for crumb in product_details.get('breadCrumbsItems', [])
                if crumb
            ],
            description=product_details.get('seoData', dict()).get('seoDesc'),
            locale=self.locale,
            currency=self.currency,
            variations=self.variation_info(product_details),
        )

        yield product_item

    def variation_info(self, product_details):
        size_item_list = self.size_info(product_details)

        variation_item_list = []
        # try getting color scheme if present add it and add size list into ti otherwise leave it empty

        colors = product_details.get('colorGroups', [])
        if colors:
            colors = colors[0].get('colors', [])

        if not colors:
            colors.append({
                'name': '',
                'swatchImageUrl': '',
            })

        for color in colors:
            variation_item = VariationItem(
                display_color_name=color['name'],
                images_urls=color['swatchImageUrl'],
                sizes=size_item_list,
            )
            variation_item_list.append(variation_item)

        return variation_item_list

    def size_info(self, product_details):
        size_item_list = []
        sizes = product_details.get('sizes', [])
        if sizes:
            sizes = sizes[0].get('values', [])

        if not sizes:
            sizes.append({
                'name': '',
                'available': True,
            })

        for size in sizes:
            size_item = SizeItem(
                size_name=size['name'],
                is_available=size['available'],
                price=product_details.get('price', dict()).get('originalPrice', ''),
                is_discounted=product_details.get('price', dict()).get('onSale', False),
                discounted_price="",
            )
            if size_item['is_discounted']:
                size_item['discounted_price'] = product_details['price']['salePrice']

            size_item_list.append(size_item)

        return size_item_list

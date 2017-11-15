import re
import json

import scrapy

from FirstScrapyTask.items import SkechersItem


class SkechersSpider(scrapy.Spider):

    name = 'skechers'
    start_urls = ['https://www.skechers.com/en-us/accessories?category=/accessories/watches',
                  'https://www.skechers.com/en-us/accessories?category=/accessories/bags',
                  'https://www.skechers.com/en-us/accessories?category=/accessories/sunglasses',
                  'https://www.skechers.com/en-us/accessories?category=/accessories/care-products',
                  'https://www.skechers.com/en-us/accessories?category=/accessories/socks',
                  'https://www.skechers.com/en-us/apparel',
                  'https://www.skechers.com/en-us/kids/all',
                  'https://www.skechers.com/en-us/women/all',
                  'https://www.skechers.com/en-us/men/all']
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        heading = 'https://www.skechers.com'
        product_urls = response.css('div::attr(data-clicked-style-url)').extract()
        api = self.get_api(response)
    #    api = 'https://www.skechers.com/en-us/api/html/products/apparel?bookmark='
        bookmark = self.get_bookmarks(response)

        for row in product_urls:
            url = '{}{}'.format(heading , row)
            request = scrapy.Request(url=url, callback=self.parse_three)
            yield request

        if bookmark:
            url = '{}{}'.format(api , bookmark)
            request = scrapy.Request(url=url, callback=self.parse_two , meta={'api' : api})
            yield request

    def parse_two(self, response):
        heading = 'https://www.skechers.com'
        api = response.meta['api']
        #api = 'https://www.skechers.com/en-us/api/html/products/apparel?bookmark='
        response_result = json.loads(response.text)
        product_urls = re.findall('\/en-us.*\s' ,response_result['stylesHtml'])

        for row in product_urls:
            url = '{}{}'.format(heading , row.split('"')[0])
            request = scrapy.Request(url=url, callback=self.parse_three)
            yield request

        if response_result['bookmark']:
            url = '{}{}'.format(api , response_result['bookmark'])
            request = scrapy.Request(url=url, callback=self.parse_two , meta={'api' : api})
            yield request

    def parse_three(self, response):

        product = SkechersItem()

        product['Style_Name'] = response.css('h1.product-title::text').extract_first()
        product['Style_URL'] = response.url
        product['Style_Price_Final'] = response.css('ins.price-final::text').extract_first()
        product['Style_Currency'] = product['Style_Price_Final'][0]
        product['Style_Color'] = response.css('div.product-label.js-color::text').extract_first()
        product['Style_Brand'] = 'Skechers'
        product['Style_Desc'] = response.css('div.toggle-expand.toggle-description div::text').extract_first()
        product['Style_More_Details'] = response.css('div.toggle-expand.toggle-description li::text').extract()
        product_style_one = response.css('span.pull-right.product-label::text').extract_first()
        product_style_two = response.css('span.js-color-code::text').extract_first()
        product['Style_Product_Code'] = '{}{}'.format(product_style_one , product_style_two)

        product['Style_Category'] = self.get_category(response)
        product['Style_Image_Urls'] = self.get_image_urls(response)
        product['Style_Sizes_Info'] = self.get_size(response)

        yield product

    def get_bookmarks(self , response):

        script_tag = response.css('div.js-listing.listing.droplet.styles-droplet.clearfix script').extract_first()

        bookmark_tag = re.findall('bookmark.*\s', str(script_tag))

        bookmark_tag = bookmark_tag[0]

        position = []

        for index, char in enumerate(bookmark_tag):
            if char == '\'':
                position.append(index)

        return bookmark_tag[position[0] + 1: position[1]]

    def get_image_urls(self, response):

        image_urls = response.css('img.responsiveImg::attr(src)').extract()
        image_path = image_urls[0].replace('.jpg' , '')
        product_info = self.get_json(response)

        img_count = int(product_info['products'][0]['numimages'])
        if img_count > 6:
            img_count = 6

        char_value = 66
        while img_count != 1:
            image_urls.append('{}{}{}{}'.format(image_path , '_' , chr(char_value) , '.jpg'))
            img_count = img_count - 1
            char_value = char_value + 1

        return image_urls

    def get_category(self , response):

        product_info = self.get_json(response)
        gender = product_info['gender']

        if gender == 'M':
            return 'Men'
        elif gender == 'W':
            return 'Women'
        elif gender == 'B':
            return 'Boys'
        elif gender == 'G':
            return 'Girls'
        else:
            return 'Men/Women/Accessories'

    def get_size(self, response):

        product_info = self.get_json(response)
        sizes = []

        for row in product_info['products'][0]['sizes']:
            sizes.append('{}{}{}{}'.format('Size: ' , row['size'] , ' In_Stock: ' , str(row['instock'])))

        if sizes:
            return sizes
        else:
            return 'N/A'

    def get_json(self , response):

        product_info = re.findall('{"stylecode.*\;', response.text)
        return json.loads(product_info[0].replace(';',''))

    def get_api(self , response):

        if 'women' in response.url:
            return 'https://www.skechers.com/en-us/api/html/products/styles/listing?genders=W&bookmark='

        elif 'men' in response.url:
            return 'https://www.skechers.com/en-us/api/html/products/styles/listing?genders=M&bookmark='

        elif 'apparel' in response.url:
            return 'https://www.skechers.com/en-us/api/html/products/apparel?bookmark='

        elif 'kids' in response.url:
            return 'https://www.skechers.com/en-us/api/html/products/styles/listing?genders=G,B&bookmark='

        elif 'socks' in response.url:
            return 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/socks&bookmark='

        elif 'bags' in response.url:
            return 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/bags&bookmark='

        elif 'watches' in response.url:
            return 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/watches&bookmark='

        elif 'sunglasses' in response.url:
            return 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/sunglasses&bookmark='

        elif 'care-products' in response.url:
            return 'https://www.skechers.com/en-us/api/html/products/accessories?category=/accessories/care-products&bookmark='
        else:
            return ''
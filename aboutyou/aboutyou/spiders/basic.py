import json
import scrapy

from aboutyou import country_currencies
from aboutyou.items import AboutyouItem
from urlparse import urljoin


class BasicSpider(scrapy.Spider):
    name = 'aboutyou'
    allowed_domains = ['www.aboutyou.at',
                       'api.aboutyou.at']
    start_url = 'https://www.aboutyou.at'

    def __init__(self):
        super(BasicSpider, self).__init__()
        self.depth = 1
        self.locale = None
        self.product_variants = ["brand",
                                 "defaultImage",
                                 "defaultVariant",
                                 "variants",
                                 "variants.images",
                                 "variants.sizes",
                                 "modelImage",
                                 "styles.defaultImage",
                                 "styles.modelImage",
                                 "styles.product-details.attributeGroups",
                                 "styles.product-details.images",
                                 "styles.product-details.model-information",
                                 "product-details.attributeGroups",
                                 "product-details.images",
                                 "product-details.model-information",
                                 ]

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.gender_switch)

    def gender_switch(self, response):
        genders = response.css('.styles__genderSwitch--3jvXr *::attr(href)').extract()
        for gender in genders:
            absolute_url = urljoin(self.start_url, gender)
            yield scrapy.Request(absolute_url, callback=self.parse_gender_state, meta={'gender': gender})

    def parse_gender_state(self, response):
        """
        Get the initial state of the website in a json format.
        """
        initial_state = response.xpath('//*[contains(text(), "window.__INITIAL_STATE__")]/text()').extract_first()
        initial_state = initial_state.replace('window.__INITIAL_STATE__=', '').rstrip(";")
        initial_state = json.loads(initial_state.encode('utf8'))
        self.locale = initial_state['urlManager']['locale']
        return self.crawl_categories(initial_state, response.meta['gender'])

    def crawl_categories(self, initial_state, user):
        all_active_categories = initial_state['entities']['categories']
        category_ids = self.get_category_ids(all_active_categories, user)
        category_products_api = 'https://api.aboutyou.at/products?filter[category]={id}'
        # Horizontal Crawling
        for ID in category_ids:
            yield scrapy.Request(category_products_api.format(id=ID), callback=self.parse_pages,
                                 meta={'category_id': ID})

    def parse_pages(self, response):
        """
        Determines the number of pages to be parsed and send requests to those pages to be scraped
        limit can be changed to read more pages
        """
        category_products_api = 'https://api.aboutyou.at/products?filter[category]={id}'
        id_ = response.meta['category_id']
        category_info = json.loads(response.body.encode('utf8'))
        total_pages = category_info['meta']['pagination']['total_pages']
        limit = 5
        pages = total_pages if total_pages < limit else limit
        print(pages)
        for page in range(1, pages+1):
            url = (category_products_api + "&page[number]={page}").format(id=id_, page=page)
            yield scrapy.Request(url, callback=self.parse_category_products)

    def get_category_ids(self, all_active_categories, user_url):
        """
        The method gets all the category IDs
        Depth determines the subcategory against each URL, for which data is to be retrieved
        Depth 0 : /frauen
        Depth 1 : /frauen/shoes, /frauen/clothes, ...
        Depth 2 : /frauen/shoes/new, /frauen/shoes/sneakers, ...
        """
        category_ids = []
        for category in all_active_categories:
            if all_active_categories[category]['url'] == user_url:  # Get starting point
                category_ids.append(category)
                break

        for _ in range(self.depth):
            children_ids = []
            for parent_id in category_ids:
                category_ids.remove(parent_id)
                children_ids += all_active_categories[parent_id]['childrenIds']
            category_ids += children_ids
        return category_ids

    def parse_category_products(self, response):
        products_details_api = 'https://api.aboutyou.at/products/{}?keyedIncludes=true&version=41&include=' \
                               + ','.join(self.product_variants)
        all_products = json.loads(response.body.encode('utf8'))
        # Vertical Scraping
        for product in all_products['data']:
            yield scrapy.Request(products_details_api.format(product['id']), callback=self.parse_product)

    def parse_product(self, response):
        item = AboutyouItem()
        product = json.loads(response.body.encode('utf8'))
        product_attributes = product['data']['attributes']
        product_relationships = product['data']['relationships']
        relationship_details = product['included']
        brand_name = self.get_brand_name(relationship_details, product_relationships['brand']['data']['id'])
        locale = self.locale

        item['product_url'] = urljoin(self.start_url, product_attributes['url'])
        item['store_keeping_unit'] = product['data']['id']
        item['title'] = product_attributes['name']
        item['brand'] = brand_name
        item['description'] = self.get_description(relationship_details, product['data']['id'])
        item['locale'] = locale
        item['currency'] = country_currencies.CURRENCIES_BY_COUNTRY_CODE[locale.split("_")[1]]
        item['variations'] = {}
        return self.get_variationitem(product_relationships, relationship_details, item)

    def get_variationitem(self, relationships, relationship_details, item):
        sizeitem_api = 'https://api.aboutyou.at/products/{}?keyedIncludes=true&version=41&' \
                       'include=defaultVariant,variants,variants.sizes'
        all_styles = relationships['styles']['data']
        colors_info = []

        for style in all_styles:
            style_details = relationship_details['styles:' + str(style['id'])]
            product_details_id = style_details['relationships']['product-details']['data']['id']
            product_details = relationship_details['product-details:' + str(product_details_id)]
            color_name_slug, color_name_website = self.get_color_details(style_details, relationship_details)
            images = self.get_images(product_details)
            item['variations'][color_name_slug] = {'color name': color_name_website, 'image urls': images}
            colors_info.append((style['id'], color_name_slug))

        color = colors_info.pop()
        yield scrapy.Request(sizeitem_api.format(color[0]), callback=self.parse_urls,
                             meta={'item': item, 'colors_info': colors_info, 'current_key': color[1]})

    def parse_urls(self, response):
        sizeitem_api = 'https://api.aboutyou.at/products/{}?keyedIncludes=true&version=41&' \
                       'include=defaultVariant,variants,variants.sizes'
        item = response.meta['item']
        colors_info = response.meta['colors_info']
        sizes = self.get_sizes(response)
        item['variations'][response.meta['current_key']]['sizes'] = sizes
        if colors_info:
            color = colors_info.pop()
            yield scrapy.Request(sizeitem_api.format(color[0]), callback=self.parse_urls,
                                 meta={'item': item, 'colors_info': colors_info, 'current_key': color[1]})
        else:
            yield item

    def get_sizes(self, response):
        color_size_details = json.loads(response.body.encode('utf8'))
        all_sizes = color_size_details['data']['relationships']['variants']['data']
        size_details = color_size_details['included']
        sizeitem = {}
        sizes = []
        for size in all_sizes:
            variant = size_details['variants:' + str(size['id'])]['attributes']
            sizeitem['size_name'] = ",".join(name for name in variant['sizes'].values() if name)
            sizeitem['is_available'] = [False, True][variant['quantity'] != 0]
            if variant['price']['reduction'] != 0:
                sizeitem['price'] = variant['price']['old']
                sizeitem['is_discounted'] = True
                sizeitem['discounted_price'] = variant['price']['current']
            else:
                sizeitem['price'] = variant['price']['current']
                sizeitem['is_discounted'] = False
                sizeitem['discounted_price'] = None
            sizes.append(sizeitem)
        return sizes

    def get_brand_name(self, data, id_):
        key = 'attributes:' + str(id_)
        if key not in data:
            return "aboutyou.to"
        else:
            return data[key]['attributes']['name']

    def get_color_details(self, style_details, r_details):
        color_id = style_details['attributes']['detailColors'].keys()
        key = 'attributes:' + str(color_id[0])
        if key not in r_details:
            return color_id, None
        else:
            return r_details[key]['attributes']['slug'], r_details[key]['attributes']['name']

    def get_images(self, product_details):
        images = []
        absolute_path = "http://cdn.aboutstatic.com/file/"
        images_data = product_details['relationships']['images']['data']
        for image_name in images_data:
            images.append(absolute_path + image_name['id'])
        return images

    def get_description(self, r_details, id_):
        product_details = r_details['product-details:' + str(id_)]
        group_attributes = product_details['relationships']['attributeGroups']['data']
        description = [product_details['attributes']['materials'][0]['composition']]
        for group_attribute in group_attributes:
            attr = r_details['attribute-groups:' + group_attribute['id']]['relationships']['attributes']['data']
            for item in attr:
                description.append(r_details['attributes:' + item['id']]['attributes']['name'])
        return description

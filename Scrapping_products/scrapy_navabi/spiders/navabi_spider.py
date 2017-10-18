import json
import scrapy


class NavabiProducts(scrapy.Spider):
    name = "navabi-uk-crawl"

    start_urls = ['https://www.navabi.co.uk/']

    care_words = ['bleach', 'dry', 'iron', 'clean', 'cycle']

    def is_care(self, sentence):
        sentence_lower = sentence.lower()
        return any(c in sentence_lower for c in self.care_words)

    def parse(self, response):
        trail_1st_page = ['landing_page', response.url]
        parameters = {'trail': [trail_1st_page], 'first_visit': True}

        new_products_link = response.css('ul.mainnav__ul a::attr(href)').extract_first()
        yield response.follow(url=new_products_link, callback=self.parse_products, meta=parameters)

    def parse_products(self, response):
        product_trail = response.meta['trail']
        is_first_visit = response.meta['first_visit']

        if is_first_visit:
            trail_page_name = response.css('ul.mainnav__ul span::text').extract_first()
            trail_current_page = [trail_page_name, response.url]
            product_trail.append(trail_current_page)

        parameters = {'trail': product_trail, 'first_visit': False}

        for next_product in response.css('a.ProductLink::attr(href)'):
            if next_product:
                yield response.follow(url=next_product, callback=self.parse_single_product, meta=parameters)

        for next_page in response.css('a[aria-label="Next"]::attr(href)'):
            if next_page:
                yield response.follow(url=next_page, callback=self.parse_products, meta=parameters)

    def parse_single_product(self, response):
        retailer_sku = response.css('div.mainContent input::attr(value)').extract_first()
        brand_name = response.css('section.col-12 h2 span a::text').extract_first()
        product_name = response.css('section.col-12 h3::text').extract_first()
        description = [response.css('div.more-details__accordion-content p::text').extract_first()]
        product_details = response.css('ul.details li::text').extract()

        product_fabric = response.css('div#materials p::text').extract()[1]
        product_fabric = product_fabric.strip(' \n\t')
        product_care = list()
        product_care.append(product_fabric)

        product_care += [product_detail for product_detail in product_details if self.is_care(product_detail)]
        description += [product_detail for product_detail in product_details if not self.is_care(product_detail)]

        category = list()
        categories = response.css('ol.breadcrumb a ::text').extract()

        for i in range(2, len(categories)):
            category.append(categories[i])

        trail = response.meta['trail']

        product_url = response.css('link[rel="alternate"]::attr(href)').extract_first()
        currency = response.css('span[itemprop="priceCurrency"]::attr(content)').extract_first()
        product_price = response.css('span[itemprop="price"]::attr(content)').extract_first()

        product_information = {
            'retailer_sku': retailer_sku,
            'brand': brand_name,
            'name': product_name,
            'category': category,
            'trail': trail,
            'gender': 'women',
            'description': description,
            'care': product_care,
            'url': product_url,
            'url_original': response.url,
            'currency': currency,
            'price': product_price,
            'market': 'UK',
            'retailer': 'navabi-uk',
            'spider_name': 'navabi-uk-crawl',
            'image_urls': [],
            'skus': []
        }

        parameters = {'product': product_information}
        color_code = response.css('input#current_colorcode::attr(value)').extract_first()
        product_link_pattern = 'https://www.navabi.co.uk/product-information/?item-id={}-{}'
        product_info_link = product_link_pattern.format(retailer_sku, color_code)

        yield scrapy.Request(url=product_info_link, callback=self.parse_product_response, meta=parameters)

    def parse_product_response(self, response):
        product = response.meta['product']

        product_response = json.loads(response.text)

        product_color_codes = product_response['colors'].keys()
        product_color_names = [product_response['colors'][colors_code]['name'] for colors_code in product_color_codes]

        size_color_detail = list()
        product_sizes = product_response['measurementInfo'].keys()

        for color in product_color_names:
            for size in product_sizes:
                size_detail = {
                    'price': product['price'],
                    'color': color,
                    'size': size,
                    'currency': product['currency'],
                    'sku_id': color + '_' + size
                }
                if float(product_response['saleprice']) > 0:
                    size_detail['previous_prices'] = [product_response['price']]
                size_color_detail.append(size_detail)

        product['skus'] = size_color_detail

        product_gallery = product_response['galleryImages']
        image_url_pattern = 'https://www.navabi.co.uk{}'
        product_image_urls = [image_url_pattern.format(image_url['big']) for image_url in product_gallery]
        product['image_urls'] = product_image_urls

        yield product

from scrapy.spiders import CrawlSpider

from ..items import OrsayItem


class OrsayExtractor:

    def parse_details(self, response):
        osray_details = OrsayItem()
        osray_details['retailer_sku'] = self.extract_sku(response)
        osray_details['gender'] = self.extract_gender()
        osray_details['category'] = self.extract_category(response)
        osray_details['brand'] = self.extract_brand()
        osray_details['url'] = self.extract_url(response)
        osray_details['name'] = self.extract_name(response)
        osray_details['description'] = self.extract_description(response)
        osray_details['care'] = self.extract_care(response)
        osray_details['img_urls'] = self.extract_img_url(response)
        osray_details['skus'] = self.extract_skus(response)
        return osray_details

    def extract_sku(self, response):
        return response.css('.product-sku::text').get().split()[-1]

    def extract_gender(self):
        return 'Female'

    def extract_category(self, response):
        return [category for category in response.css('.breadcrumb-element-link ::text').getall() if category.strip()]

    def extract_brand(self):
        return 'Oslay'

    def extract_url(self, response):
        return response.url

    def extract_name(self, response):
        return response.css('[itemprop="name"]::text').get()

    def extract_description(self, response):
        return response.css('.with-gutter::text').getall()

    def extract_care(self, response):
        return response.css('.js-material-container p::text').getall()

    def extract_img_url(self, response):
        return response.css('.productthumbnail::attr(src)').getall()

    def extract_price(self, response):
        if response.css('.price-standard').get():
            return response.css('.price-standard::text').get().split(' ')[0].strip()
        return response.css('.price-sales::text').get().split(' ')[0].strip()

    def extract_previous_price(self, response):
        if response.css('.price-standard').get():
            return response.css('.price-sales::text').get().split(' ')[0].strip()
        return ''

    def extract_currency(self, response):
        return response.css('.locale-item.current .country-currency::text').get()

    def extract_skus(self, response):
        price = self.extract_price(response)
        previous_price = self.extract_previous_price(response)
        currency = self.extract_currency(response)
        colours_list = response.css('.color a::attr(title)').getall()
        sizes_list = response.css('.size li')
        skus = []
        for color in colours_list:
            if not sizes_list:
                sku = {'Price': price,
                       'previous_price': previous_price,
                       'Currency': currency,
                       'Colour': color.split('-')[1].strip(),
                       'out_of_stock': 'False',
                       'size': '',
                       'sku_id': color.split('-')[1].strip()}
                skus.append(sku)
            for size_attr in sizes_list:
                size = size_attr.css('a::text').get().strip()
                out_of_stock = True if size_attr.css('.unselectable') else False
                sku = {'Price': price,
                       'previous_price': previous_price,
                       'Currency': currency,
                       'Colour': color.split('-')[1].strip(),
                       'out_of_stock': out_of_stock,
                       'size': size,
                       'sku_id': color.split('-')[1].strip() + "_" + size}
                skus.append(sku)
        return skus


class OrsaySpider(CrawlSpider):
    name = "orsay"
    allowed_domains = ['orsay.com']
    start_urls = [
        'https://www.orsay.com/',
    ]

    def parse(self, response):
        for category in response.css('.header-navigation a::attr(href)'):
            yield response.follow(category.get(), callback=self.parse_category)

    def parse_category(self, response):
        orsay_extraxtor = OrsayExtractor()
        if response.css('.js-next-load'):
            page_size = int(response.css('.load-more-progress-label span::text').get())
            max_pages = int(response.css('.load-more-progress::attr(data-max)').get()) // page_size
            for page in range(1, max_pages):
                url = response.url + '?prefn1=availableMarkets&sz=' + str(page_size) + '&start=' \
                      + str(page_size * page) + '&format=page-element&prefv1=de_DE'
                yield response.follow(url, callback=self.parse_category)
        for detail_url in response.css('.thumb-link::attr(href)'):
            yield response.follow(detail_url.get(), callback=orsay_extraxtor.parse_details)

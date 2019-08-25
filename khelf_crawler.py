from math import ceil
import itertools
from requests import post
from datetime import datetime
from os.path import splitext

from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import ccy


class KhelfCrawler(CrawlSpider):
    name = 'khelf'

    allowed_domains = ['khelf.com.br']
    start_urls = ['https://www.khelf.com.br/']

    listings_css = ['#nav > li > a']

    currency = 'BRL'
    retailer = 'khelf-br'

    link_category_map = {
        'https://www.khelf.com.br/feminino-1.aspx/c': 1,
        'https://www.khelf.com.br/masculino-3.aspx/c': 3,
        'https://www.khelf.com.br/acessorios-4.aspx/c': 4
    }

    colors_request_headers = {'X-AjaxPro-Method': 'DisponibilidadeSKU', 'Referer': 'https://www.khelf.com.br/'}

    rules = (
        Rule(LinkExtractor(allow=('feminino', 'masculino', 'acessorios'), restrict_css=listings_css), callback='parse'),
    )

    def parse(self, response):
        trail = response.meta.get('trail', [["", response.url]])
        for request in super().parse(response):
            request.meta['trail'] = trail + [[request.meta['link_text'].strip(), request.url]]
            yield request

        # pagination
        category = self.link_category_map.get(response.url)
        if category is not None:
            category_products_count = int(response.css('.filter-details strong:last-child::text').get())
            for page_number in range(1, ceil(int(category_products_count) / 21) + 1):
                link = (f'https://www.khelf.com.br/categoria/1/{category}/0//MaisRecente/Decrescente/21/{page_number}'
                        f'//0/0/.aspx')
                link_trail = trail + [['>', link]]
                yield response.follow(link, meta={'trail': link_trail})

        # products requests
        products_grid = response.css('#listProduct .hproduct')
        for product in products_grid:
            product_link = product.css('div.figure > a::attr("href")').get()
            product_color_codes = product.css('ul a::attr("color-code")').getall()
            yield response.follow(product_link, meta={'trail': trail, 'color_codes': product_color_codes},
                                  callback=self.parse_product)

    def parse_product(self, response):
        product = {}

        product['retailer_sku'] = self.extract_retailer_sku(response=response)
        product['trail'] = response.meta['trail']
        product['description'] = self.extract_description(response=response)
        product['gender'] = self.extract_gender(response=response)
        product['category'] = self.extract_category(trail=product['trail'])
        product['brand'] = self.extract_brand(response=response)
        product['url'] = self.extract_url(response=response)
        product['date'] = self.extract_date(response=response)
        product['price'] = self.extract_price(response=response)
        product['currency'] = self.currency
        product['market'] = self.extract_market()
        product['retailer'] = self.retailer
        product['url_original'] = response.url
        product['name'] = self.extract_name(response=response)
        product['care'] = self.extract_care(response=response)
        product['spider_name'] = self.name
        product['crawl_start_time'] = self.extract_crawl_start_time()

        product_id = response.css('meta[name="itemId"]::attr("content")').get()
        colors_information = {}
        for color_code in response.meta['color_codes']:
            data = (f'{{'
                    f'"ProdutoCodigo":"{product_id}",'
                    f'"CarValorCodigo1":"{color_code}",'
                    f'"CarValorCodigo2":"0",'
                    f'"CarValorCodigo3":"0",'
                    f'"CarValorCodigo4":"0",'
                    f'"CarValorCodigo5":"0"'
                    f'}}')
            colors_information[color_code] = post('https://www.khelf.com.br/ajaxpro/IKCLojaMaster.detalhes,Khelf.ashx',
                                                  headers=self.colors_request_headers, data=data).json()['value']

        product['image_urls'] = self.extract_image_urls(response=response, colors_information=colors_information)
        product['skus'] = self.extract_skus(price=product['price'], product_id=product_id,
                                            colors_information=colors_information)

        yield product

    def extract_retailer_sku(self, response):
        return response.css('#liCodigoInterno > span::text').get().strip()

    def extract_gender(self, response):
        genders = {
            'masculina': {'masculina', 'masculino'},
            'feminina': {'feminina', 'feminino'},
        }

        url_lowercase = response.url.lower()
        for gender in genders:
            if check_words_existence(genders[gender], url_lowercase):
                return gender
        return 'unisex'

    def extract_brand(self, response):
        brands = {'Moleskine': {'moleskine'},
                  'Fiever': {'fiever'},
                  'Converse': {'converse'},
                  'Casio / G-Shock': {'casio', 'g-shock'},
                  'Evoke': {'evoke'},
                  'Guess': {'guess'},
                  'Vert Shoes': {'vert'}
                  }
        url_lowercase = response.url.lower()
        for brand in brands:
            if check_words_existence(brands[brand], url_lowercase):
                return brand
        return ''

    def extract_category(self, trail):
        return [t[0] for t in itertools.islice(trail, 1, None)]

    def extract_url(self, response):
        return response.css('head link[rel="canonical"]::attr("href")').get()

    def extract_date(self, response):
        date = response.headers["Date"].decode('utf-8')
        return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%dT%H:%M:%S.%f')

    def extract_market(self):
        return ccy.currency(self.currency).default_country

    def extract_name(self, response):
        return response.css('h1.name::text').get().strip()

    def extract_description(self, response):
        return [data.strip() for data in response.css('#description > p::text').getall()]

    def extract_care(self, response):
        return [c.strip() for c in response.css('#panCaracteristica > p::text').getall()]

    def extract_image_urls(self, response, colors_information):
        image_urls = []
        for color_information in colors_information.values():
            color_images_information = color_information[1]

            # main image added
            image_urls.append(response.urljoin(color_images_information[14]))

            images_url_prefix, extension = splitext(image_urls[-1])
            gifs_index = [i for i in range(0, len(color_images_information), 2)
                          if color_images_information[i].endswith('.gif')]
            total_numbered_images = int((gifs_index[0] if gifs_index else 14) / 2) - 1
            for number in range(1, total_numbered_images):
                image_urls.append(''.join((images_url_prefix, str(number), extension)))
        return image_urls

    def extract_skus(self, price, product_id, colors_information):
        common_sku = {'price': price, 'currency': self.currency}

        skus = []
        for color_code, color_information in colors_information.items():
            color_images_information = HtmlResponse(url='example.com', body=color_information[3], encoding='utf-8')
            for size_tag in color_images_information.css('ul[class=""] > li'):
                sku = common_sku.copy()
                sku['size'] = size_tag.css('a::text').get()
                sku['out_of_stock'] = size_tag.css('li::attr("class")').get() == 'warn'
                sku['sku_id'] = f'{product_id}_{color_code}_{sku["size"]}'
                skus.append(sku)

        return skus

    def extract_price(self, response):
        return response.css('#lblPrecoPor > strong::text').get()

    def extract_crawl_start_time(self):
        return self.crawler.stats._stats['start_time'].strftime('%Y-%m-%dT%H:%M:%S.%f')


def check_words_existence(words, text):
    return any(word in text for word in words)
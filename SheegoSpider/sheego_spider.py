from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from OspraySpider.items import SheegoSpiderItem
from scrapy import Request
from urllib.parse import urlencode
import json


class SheegoSpider(CrawlSpider):
    name = "sheego"
    allowed_domains = ["sheego.de"]
    start_urls = ['https://www.sheego.de/inspiration/get-inspired/figurberatung/v-typ/'
                    , 'https://www.sheego.de/mode/damenmode/'
                    , 'https://www.sheego.de/damenwaesche/'
                    , 'https://www.sheego.de/waesche-bademode/night-homewear/'
                    , 'https://www.sheego.de/damen-bademode/'
                    , 'https://www.sheego.de/schuhe/schuhtypen/'
                    , 'https://www.sheego.de/inspiration/shoppen-nach-figurtyp/h-typ/'
                    , 'https://www.sheego.de/inspiration/get-inspired/figurberatung/v-typ/'
                    , 'https://www.sheego.de/inspiration/modeberatung/figurberatung/a-typ/'
                    , 'https://www.sheego.de/inspiration/modeberatung/figurberatung/x-typ/',
                  ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=(['a.cj-mainnav__entry-title', 'a.mainnav__link',
                                                    'a.js-next.at-pl-page-navi-next'])), follow=True),
        Rule(LinkExtractor(allow=(), restrict_css=('a.product__top.js-productlink.text-link--inherit',)),
             callback="parse_items"),
    )

    def parse_items(self, response):
        item = SheegoSpiderItem()
        item.setdefault('gender', 'female')
        item['brand'] = self.get_brand(response)
        item['category'] = self.get_category(response)
        item['care'] = self.get_care(response)
        item['description'] = [self.get_description(response)]
        item['image_urls'] = [self.get_image(response)]
        item['name'] = [self.get_product_name(response)]
        item['skus'] = self.get_skus(response)
        item['url'] = response.url
        item['url_original'] = response.url
        links = self.get_color_url_list(response)
        if links:
            url_dict = self.url_paramaters(response)
            url_dict['varselid[0]'] = links[0]
            item['retailer_sku'] = url_dict['anid']
            url = 'https://www.sheego.de/index.php?' + urlencode(url_dict)
            request = Request(url, callback=self.parse_additional_colors)
            request.meta['url_params'] = url_dict
            request.meta['item'] = item
            request.meta['links'] = links[1:]
            return request
        else:
            item['retailer_sku'] = self.url_paramaters(response)['anid']
            return item

    def parse_additional_colors(self, response):
        links = response.meta['links']
        item = response.meta['item']
        item['skus'].update(self.get_skus(response))
        item['image_urls'].append(self.get_image(response))
        if links:
            url_dict = response.meta['url_params']
            url_dict['varselid[0]'] = links[0]
            url = 'https://www.sheego.de/index.php?' + urlencode(url_dict)
            request = Request(url, callback=self.parse_additional_colors)
            request.meta['url_params'] = url_dict
            request.meta['item'] = item
            request.meta['links'] = links[1:]
            return request
        else:
            return item

    def get_skus(self, response):
        sizes = self.get_sizes(response)
        price = self.get_price(response)
        currency = self.get_currency(response)
        result = {}
        color = self.get_current_color(response)
        for size in sizes:
            stock_info = {}
            formatted_size = size.strip('Unavailable-')
            if 'Unavailable' in size:
                stock_info.update({'out_of_stock': True})
            sku_size_identifier = '{0}_{1}'.format(color, formatted_size)
            result[sku_size_identifier] = {
                'colour': color,
                'currency': currency,
                'price': price,
                'size': formatted_size
            }
            result[sku_size_identifier].update(stock_info)
        return result

    def get_care(self, response):
        result = []
        answer = ""
        temp = None
        for i in response.css('table.p-details__material td'):
            if i.css('span::text').extract_first():
                temp = ', {0}'.format(i.css('span::text').extract_first().strip())
            elif i.css('::text').extract_first():
                temp = ': {0}'.format(i.css('::text').extract_first().strip())
            if temp:
                answer += temp
        if answer:
            result.append(answer[2:])
        for care_symbol in response. \
                css('div.details__box--detailsAdd.js-article-ocv>div>div>div>div>template::text').extract():
            result.append(care_symbol.strip())
        return result

    def get_description(self, response):
        return [' '.join(i.strip() for i in response.css('div[itemprop="description"] p::text, b::text').extract())]

    def get_image(self, response):
        return response.css('#productMainImg::attr(href)').extract_first()

    def get_current_color(self, response):
        return response.xpath("//p[contains(span, 'Farbe')]/text()").extract()[1].strip()

    def get_color_url_list(self, response):
        result = []
        for color in response.css('span.colorspots__item'):
            if not color.css('.cj-active'):
                result.append(color.xpath("attribute::*[name()='data-varselid']").extract_first())
        return result

    def get_product_name(self, response):
        return response.css('h1[class="l-regular l-text-1 at-name"]::text').extract_first().strip()

    def get_price(self, response):
        return response.css('meta[itemprop="price"]::attr(content)').extract_first()

    def get_sizes(self, response):
        sizes = []
        for size in response.css('section.size option[data-varselid]'):
            size_keyword = ""
            if size.xpath('contains(text(),"nicht auf Lager")').extract_first() == '1':
                size_keyword += "Unavailable-"
            sizes.append('{0}{1}'.format(size_keyword, size.css('::text').extract_first().strip().split(' ')[0]))
        return sizes

    def url_paramaters(self, response):
        webtrends = response.xpath\
            ("//input[@class='js-webtrends-data']/attribute::*[name()='data-webtrends']").extract_first()
        webtrends_dict = json.loads(webtrends)
        anid = webtrends_dict['productId'].split('-')[1]
        aid = webtrends_dict['productSku'].split('-')[1]
        color = aid[15:20]
        name = webtrends_dict['productName']
        params = {'bShoppiless': True, 'anid': anid, 'aid': aid, 'promo': 'W5',
                   'farbid': color, 'parentid': anid, 'artNr': anid, 'artName': name,
                   'cl': 'oxwarticledetails', 'ajaxdetails': 'adsColorChange', 'render': 'colorChange'}

        return params

    def get_currency(self, response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    def get_category(self, response):
        result = response.css('span.breadcrumb__item>a>span::text').extract()
        if 'Start' in result:
            result.remove('Start')
        if 'zurück' in result:
            result.remove('zurück')
        return result

    def get_brand(self, response):
        for brand_name in response.css('section[class="p-details__brand at-brand"]'):
            if brand_name.css('a'):
                return brand_name.css('a::text').extract_first().strip()
            else:
                return brand_name.css('::text').extract_first().strip()

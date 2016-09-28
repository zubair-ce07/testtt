import datetime
import re
import scrapy
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import xml.etree.ElementTree as Article_Element
from sheego_scraper.items import SheegoScraperItem


class SheegoSpider(CrawlSpider):
    name = "sheego_spider"
    allowed_domains = ["sheego.de"]
    start_urls = ['https://www.sheego.de/', ]

    listing_x = ['//div[@id="mainnavigation"]', '//div[@id="sidebar"]', '//div[@class="info"]']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listing_x)),
        Rule(LinkExtractor(restrict_xpaths=['//div[contains(@class,"product__item")]']), callback='parse_product'))

    def parse_product(self, response):
        product = SheegoScraperItem()
        product['category'] = self.product_category(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['description'] = self.product_description(response)
        product['url_original'] = response.url
        product['brand'] = self.product_brand(response)
        product['image_urls'] = self.product_image_urls(response)
        product['date'] = str(datetime.datetime.now())
        product['lang'] = 'de'
        product['name'] = self.product_name(response)
        product['url'] = response.url
        product['gender'] = 'Women'
        product['skus'] = {}
        return self.check_out_of_stock_request(product, response)

    def product_retailer_sku(self, response):
        return response.css("input[name=aid]::attr(value)")

    def product_description(self, response):
        short_description = self.product_short_description(response)
        long_description = self.product_long_description(response)
        return short_description + long_description

    def product_long_description(self, response):
        description = response.css('div[itemprop=description]::text').extract()
        return self.clean(description)

    def product_short_description(self, response):
        short_description_x = '[class*=productDetail] > div.highlight ul li::text'
        description = response.css(short_description_x).extract()
        return self.clean(description)

    def product_brand(self, response):
        brand = response.css(".brand > a::text").extract() or response.css(".brand::text").extract()
        return brand[0].strip()

    def product_image_urls(self, response):
        return response.css('div.thumbs a::attr(data-zoom-image)').extract()

    def product_name(self, response):
        return response.css(".at-dv-itemName::text").extract()[0].strip()

    def product_price(self, response):
        price = response.css('.at-lastprice::text').extract()
        return self.clean(price)

    def product_prev_price(self, response):
        prev_price = response.css('sub[class*=at-wrongprice]::text').extract()
        return [repr(prev_price[0]).split('\\')[0]] if prev_price else None

    def product_category(self, response):
        return response.css('.breadcrumb a::text').extract()[1:]

    def check_out_of_stock_request(self, product, response):
        out_of_stock = self.get_xml_response(response)
        url = 'http://www.sheego.de/request/kal.php'
        headers = {"Content-Type": "application/xml; charset=UTF-8",
                   "Accept": "application/xml, text/xml, */*; q=0.  01",
                   "X-Requested-With": "XMLHttpRequest"}
        return Request(url=url, method="POST", headers=headers, body=out_of_stock,
                       meta={'product': product, 'url': response.url}, callback=self.parse_out_of_stock)

    def parse_out_of_stock(self, response):
        product = response.meta['product']
        url = response.meta['url']
        root = Article_Element.fromstring(response.body.decode("utf-8"))
        article_in_stock = {}
        article_out_of_stock = {}

        if root.findall('.//LocalError'):
            product['out_of_stock'] = True
            return product

        all_articles = root.findall('.//ArticleAvailability')

        for article in all_articles:
            item_no = article.find('.//CompleteCatalogItemNo').text
            article_in_stock[item_no] = []
            article_out_of_stock[item_no] = []

        for article in all_articles:
            item_code = article.find('.//CompleteCatalogItemNo').text
            if article.find('.//Stock').text == '1':
                article_in_stock[item_code].append(article.find('.//SizeAlphaText').text)
            else:
                article_out_of_stock[item_code].append(article.find('.//SizeAlphaText').text)

        color_codes = article_in_stock.keys()
        available_stock = list(article_in_stock.values())
        unavailable_stock = list(article_out_of_stock.values())
        return self.get_color_urls(product, color_codes, available_stock, unavailable_stock, url)

    def get_color_urls(self, product, color_codes, available_stock, unavailable_stock, url):
        color_request_urls = []
        for color_code in color_codes:
            promotion_id = color_code[6:]
            url_tokens = url.split('-')
            # these indexes are to make request-URLS for different
            # colors of same product
            url_tokens[-1] = promotion_id + re.findall('\w(.html)', url)[0]
            url_tokens[-2] = color_code[:6]
            color_request_urls.append('-'.join(url_tokens))
        return self.next_color_request(color_request_urls, available_stock,
                                       unavailable_stock, product)

    def next_color_request(self, color_request_urls, available_stock, unavailable_stock, product):
        if not color_request_urls:
            return product
        color_url = color_request_urls.pop(0)
        return Request(url=color_url, callback=self.parse_color_details,
                       dont_filter=True, meta={'color_links': color_request_urls, 'product': product,
                                               'available_stock': available_stock,
                                               'unavailable_stock': unavailable_stock})

    def get_size_variant(self, response):
        variant_x = "//select[contains(@class,'variants js-variantSelector')]/option[@selected='selected']/text()"
        return ' '.join(response.xpath(variant_x).extract())

    def get_article_id(self, response):
        return ' '.join(response.xpath('//input[contains(@name,"aid")]/@value').extract())

    def parse_color_details(self, response):
        product = response.meta['product']
        color_links = response.meta['color_links']
        available_stock = response.meta['available_stock']
        unavailable_stock = response.meta['unavailable_stock']
        sizes_unavailable = unavailable_stock.pop(0)

        for size in sizes_unavailable:
            size_variant = self.get_size_variant(response)
            if size_variant:
                size += '_' + size_variant
            colour = ' '.join(response.xpath("//a[contains(@class,'color-item active js-ajax')]/@title").extract())
            product['skus'][colour + '_' + size] = {'instock': False,
                                                    'currency': 'EUR',
                                                    'colour': colour,
                                                    'size': size,
                                                    'price': self.product_price(response),
                                                    'previous_price': self.product_prev_price(response)
                                                    }

        sizes_available = available_stock.pop(0)
        product['image_urls'].extend(self.product_image_urls(response))
        size_data = []
        if sizes_available:
            article_id = self.get_article_id(response)
            token_article_id = article_id.split('-')
            for size in sizes_available:
                token_article_id[-2] = size.split('/')[0]
                size_data.append('-'.join(token_article_id))
        return self.get_next_size_request(response, size_data,
                                          color_links, available_stock, unavailable_stock, product)

    def get_next_size_request(self, response, size_data, color_links, available_stock, unavailable_stock, product):
        if not size_data:
            return self.next_color_request(color_links, available_stock, unavailable_stock, product)
        aid = size_data.pop()
        sizeform = {}
        sizeform['anid'] = aid
        sizeform['artNr'] = re.findall('\d+-(\d+)', response.url)[0]
        sizeform['varselid[0]'] = response.xpath('//input[contains(@name,"varselid[0]")]/@value').extract()[0]

        if response.xpath('//div[contains(@id,"variants")]/div/select/option/text()').extract():
            sizeform['varselid[1]'] = response.xpath('//input[contains(@name,"varselid[1]")]/@value').extract()[0]
        return scrapy.FormRequest.from_response(response,
                                                formdata=sizeform, callback=self.parse_size_request, formnumber=1,
                                                meta={'form_response': response, 'sizeform': sizeform,
                                                      'available_stock': available_stock,
                                                      'unavailable_stock': unavailable_stock, 'size_data': size_data,
                                                      'color_links': color_links,
                                                      'product': product})

    def parse_size_request(self, response):
        form_response = response.meta['form_response']
        size_data = response.meta['size_data']
        sizes_in_stock = response.meta['available_stock']
        sizes_out_of_stock = response.meta['unavailable_stock']
        product = response.meta['product']
        color_links = response.meta['color_links']
        skus = self.product_sku_common(response)
        product['skus'][skus['color'] + '_' + skus['size']] = skus
        return self.get_next_size_request(form_response, size_data, color_links,
                                          sizes_in_stock, sizes_out_of_stock, product)

    def get_xml_response(self, response):
        stock_info = ' '.join(response.xpath('//script[contains(text(), "setKALAvailability" )]/text()').extract())
        if stock_info:
            stock_info = re.search('String\(\'(.+)\',\d', stock_info).group(1).split(';')
            articles = Article_Element.Element('Articles')
            for colour_code, size in zip(stock_info[0::2], stock_info[1::2]):
                article = Article_Element.SubElement(articles, 'Article')
                Article_Element.SubElement(article, 'CompleteCatalogItemNo').text = colour_code
                Article_Element.SubElement(article, 'SizeAlphaText').text = size
                Article_Element.SubElement(article, 'Std_Promotion').text = colour_code[6:]
                Article_Element.SubElement(article, 'CustomerCompanyID').text = '0'
            kal_availability = Article_Element.Element('tns:KALAvailabilityRequest',
                                                       attrib={'xmlns:tns': "http://www.schwab.de/KAL",
                                                               'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                                                               'xsi:schemaLocation':
                                                                   "http://www.schwab.de/KAL "
                                                                   "http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd"
                                                               }
                                                       )
            kal_availability.append(articles)
            return Article_Element.tostring(kal_availability).decode("utf-8")

    def product_sku_common(self, response):
        skus = {}
        size = response.css('span[class*=at-dv-size]::text').extract()[0].strip('–').replace('–', ' ')
        color = response.xpath('//span[@class="at-dv-color"]/text()').extract_first().split(' ')[1]
        price = self.product_price(response)
        prev_price = self.product_prev_price(response)
        if prev_price:
            skus['previous_prices'] = prev_price
        skus = {'color': color, 'currency': 'EUR', 'price': price, 'size': size, 'instock': True,
                'previous_price': prev_price}
        return skus

    def clean(self, item_list):
        return [item.strip() for item in item_list if not item.isspace()]


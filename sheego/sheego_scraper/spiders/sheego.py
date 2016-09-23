import datetime
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
import scrapy
from scrapy.spiders import CrawlSpider, Rule
import xml.etree.ElementTree as et
from sheego_scraper.items import SheegoScraperItem
import re


class SheegoSpider(CrawlSpider):
    name = "sheego_spider"
    allowed_domains = ["sheego.de"]
    start_urls = [
        'http://www.sheego.de/',
    ]

    category_listing_x = ['//div[@id="mainnavigation"]', '//div[@id="sidebar"]', '//div[@class="info"]']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=category_listing_x)),
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
        product['care'] = self.product_care(response)
        product['lang'] = 'de'
        product['name'] = self.product_name(response)
        product['url'] = response.url
        product['gender'] = 'Women'
        product['skus'] = {}

        return self.check_outofstock_request(product, response)

    def product_category(self, response):
        return response.xpath("//ul[@class='breadcrumb']/li//a[not (@href='https://www.sheego.de/')]/text()").extract()

    def product_retailer_sku(self, response):
        return response.xpath('//input[@name="aid"]/@value').extract_first().split('-')[0]

    def product_description(self, response):
        short_description = self.product_short_description(response)
        long_description = self.product_long_description(response)
        complete_description = short_description + long_description
        return complete_description

    def product_long_description(self, response):
        description = response.xpath("//div[@itemprop = 'description']//text()").extract()
        return [item.strip() for item in description if not item.isspace()]

    def product_short_description(self, response):
        description = response.xpath(
            ".//*[contains(@class, 'productDetail')]/div[@class='highlight']//ul//li/text()").extract()
        return [item.strip() for item in description if not item.isspace()]


    def product_brand(self, response):
        brand = response.xpath('//div[contains(@class, "productDetailBox")]//div[@class="brand"]//text()').extract()
        return ''.join(brand).strip()

    def product_image_urls(self, response):
        return response.xpath('//div[@class="thumbs"]//a/@data-zoom-image').extract()

    def product_care(self, response):
        care = response.xpath('//div[@class="js-articledetails"]//dl[contains(@class,"articlequality")]//text()') \
            .extract()
        return filter(None, [characteristic.strip() for characteristic in care])

    def product_name(self, response):
        return response.xpath('//span[@itemprop="name"]//text()').extract_first().strip()


    def product_price(self, response):
        price = response.xpath('//span[contains(@class,"lastprice at-lastprice")]/text()').extract()
        return [item.strip() for item in price if not item.isspace()]


    def product_prev_price(self, response):
        prev_price = response.xpath('//sub[contains(@class,"at-wrongprice")]//text()').extract()
        return [repr(prev_price[0]).split('\\')[0]] if prev_price else None

    def check_outofstock_request(self, product, response):
        oos = self.get_xml_response(response)
        url = 'http://www.sheego.de/request/kal.php'
        headers = {"Content-Type": "application/xml; charset=UTF-8",
                   "Accept": "application/xml, text/xml, */*; q=0.01",
                   "X-Requested-With": "XMLHttpRequest"}
        product_url = response.url
        return Request(url=url, method="POST", headers=headers, body=oos,
                       dont_filter=True, meta={'product': product, 'url': product_url},
                       callback=self.parse_outofstock)

    def parse_outofstock(self, response):
        product = response.meta['product']
        url = response.meta['url']
        root = et.fromstring(response.body.decode("utf-8"))
        article_inSTock = {}
        article_outofSTock = {}
        if root.findall('.//LocalError'):
            product['out_of_stock'] = True
            return product
        all_articles = root.findall('.//ArticleAvailability')
        for article in all_articles:
            item_no = article.find('.//CompleteCatalogItemNo').text
            article_inSTock[item_no] = []
            article_outofSTock[item_no] = []
        for article in all_articles:
            item_code = article.find('.//CompleteCatalogItemNo').text
            if article.find('.//Stock').text == '1':
                article_inSTock[item_code].append(article.find('.//SizeAlphaText').text)
            else:
                article_outofSTock[item_code].append(article.find('.//SizeAlphaText').text)
        color_codes = article_inSTock.keys()
        available_stock = list(article_inSTock.values())
        unavailable_stock = list(article_outofSTock.values())
        return self.get_color_urls(product, color_codes, available_stock, unavailable_stock, url)

    def get_color_urls(self, product, color_codes, available_stock, unavailable_stock, url):
        color_request_urls = []
        for color_code in color_codes:
            promotion_id = color_code[6:]
            url_tokens = url.split('-')
            url_tokens[-1] = promotion_id + re.search('\w(.html)', url).group(1)
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

    def get_text(self, response, xpath):
        return ' '.join(response.xpath(xpath).extract())


    def sku_colour(self, response):
        return ' '.join(response.xpath("//a[contains(@class,'color-item active js-ajax')]/@title").extract())


    def get_size_variant(self, response):
        variant = ' '.join(response.xpath(
            '//select[contains(@class,'
            '"variants js-variantSelector js-moreinfo-variant js-sh-dropdown")]'
            '/option[contains(@selected,"selected")]/text()').extract())
        return variant

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
                size = size + '_' + size_variant
            colour = self.sku_colour(response)
            product['skus'][colour + '_' + size] = {'instock': False,
                                                    'currency': 'EUR',
                                                    'Colour': colour,
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
        sizeform['artNr'] = re.search('\d+-(\d+)', response.url).group(1)
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
        if response.xpath('//div[contains(@id,"articlenotfound")]').extract():
            pass
        if not response.xpath('//div[contains(@id,"articlenotfound")]').extract():
            skus = self.product_sku_common(response)
            product['skus'][skus['color'] + '_' + skus['size']] = skus
            return self.get_next_size_request(form_response, size_data,
                                              color_links, sizes_in_stock, sizes_out_of_stock, product)

    def get_xml_response(self, response):
        stock_info = ' '.join(response.xpath('//script[contains(text(), "setKALAvailability" )]/text()').extract())
        if stock_info:
            stock_info = re.search('String\(\'(.+)\',\d', stock_info).group(1).split(';')
            articles = et.Element('Articles')
            for colour_code, size in zip(stock_info[0::2], stock_info[1::2]):
                article = et.SubElement(articles, 'Article')
                et.SubElement(article, 'CompleteCatalogItemNo').text = colour_code
                et.SubElement(article, 'SizeAlphaText').text = size
                et.SubElement(article, 'Std_Promotion').text = colour_code[6:]
                et.SubElement(article, 'CustomerCompanyID').text = '0'
            kal_availability = et.Element('tns:KALAvailabilityRequest',
                                          attrib={'xmlns:tns': "http://www.schwab.de/KAL",
                                                  'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                                                  'xsi:schemaLocation':
                                                      "http://www.schwab.de/KAL "
                                                      "http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd"})
            kal_availability.append(articles)
            return et.tostring(kal_availability).decode("utf-8")

    def normalize_text(self, input_string):
        return ''.join(input_string.split())

    def product_sku_common(self, response):
        skus = {}
        size = self.normalize_text(
            self.get_text(response, '//span[contains(@class,"at-dv-size")]/text()').strip('–').replace('–', ' '))
        color = response.xpath('//span[@class="at-dv-color"]/text()').extract_first().split(' ')[1]
        price = self.product_price(response)
        prev_price = self.product_prev_price(response)
        if prev_price:
            skus['previous_prices'] = prev_price
        skus = {'color': color, 'currency': 'EUR', 'price': price, 'size': size, 'instock': True,
                'previous_price': prev_price}

        return skus
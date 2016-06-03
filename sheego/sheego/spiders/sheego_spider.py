import datetime
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from urlparse import urljoin
from scrapy.spiders import CrawlSpider, Rule
import xml.etree.ElementTree as ET
from sheego.items import SheegoProduct


class SheegoSpider(CrawlSpider):
    name = "sheego_spider"
    allowed_domains = ["sheego.de"]
    start_urls = [
        'http://www.sheego.de/',
    ]

    listings_xpaths = ['//ul[contains(@class,"mainnav__ul")]/li',
                       '//ul[@id="categorysubtree"]//li']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_xpaths), follow=True, callback='parse_pagination'),
        Rule(LinkExtractor(restrict_xpaths=['//div[contains(@class,"paging")]//a[@rel="next"]']),
             callback='parse_pagination'),
        Rule(LinkExtractor(restrict_xpaths=['//div[contains(@class,"product__item")]']), callback='parse_product')
    )

    def parse_pagination(self, response):
        url = response.xpath('//div[contains(@class,"paging")]//a[@rel="next"]/@href').extract()
        if url:
            base_url = 'http://www.sheego.de'
            yield Request(url=urljoin(base_url, url[0]))

    def parse_product(self, response):
        product = SheegoProduct()
        product['category'] = self.product_category(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['description'] = self.product_description(response)
        product['url_original'] = response.url
        product['brand'] = self.product_brand(response)
        product['image_urls'] = []
        product['date'] = str(datetime.datetime.now())
        product['care'] = self.product_care(response)
        product['lang'] = 'de'
        product['name'] = self.product_name(response)
        product['url'] = response.url
        product['gender'] = 'Women'
        product['skus'] = {}
        product['oos_request'] = GenerateXML()
        product['requests'] = self.color_requests(response)
        yield self.next_color_requests(product)

    def product_category(self, response):
        return response.xpath('//ul[@class="breadcrumb"]/li[position()>1]/a/text()').extract()

    def product_retailer_sku(self, response):
        return response.xpath('//input[@name="aid"]/@value').extract_first().split('-')[0]

    def product_description(self, response):
        description = response.xpath('//div[@id="moreinfo-highlight"]/ul/li/text()'
                                     '| //div[@class="js-articledetails"]/div//text()'
                                     '| //div[@class="js-articledetails"]/table[@class="tmpArticleDetailTable"]//'
                                     'tr[position()<last()]//td//text()').extract()
        return filter(None, [desc.strip() for desc in description])

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
        return response.xpath('//meta[@itemprop="price"]/@content').extract_first()

    def product_prev_price(self, response):
        prev_price = response.xpath('//sub[contains(@class,"at-wrongprice")]//text()').extract()
        return [repr(prev_price[0]).split('\\')[0]] if prev_price else None

    def color_requests(self, response):
        requests = []
        colours = response.xpath('//div[contains(@class,"moreinfo-color")]//a/@href').extract()
        for color_url in colours:
            requests += [Request(url=color_url, callback=self.parse_colors)]
        return requests

    def parse_colors(self, response):
        product = response.meta['product']
        product['skus'].update(self.sku_details(response, product))
        product['image_urls'] += self.product_image_urls(response)
        yield self.next_color_requests(product)

    def sku_details(self, response, product):
        skus = {}
        sizes = response.xpath('//div[@data-toggle="buttons-checkbox"]/button')
        color = response.xpath('//span[@class="at-dv-color"]/text()').extract_first().split(' ')[1]
        price = self.product_price(response)
        sku_common = {'colour': color, 'currency': 'EUR', 'price': price}
        prev_price = self.product_prev_price(response)
        if prev_price:
            sku_common['previous_prices'] = prev_price
        for size in sizes:
            size_text = size.xpath('.//text()').extract_first()
            size_value = size.xpath('./@data-noa-size').extract_first()
            sku = {'size': size_text, 'colour': color}
            sku.update(sku_common)
            garment = product['oos_request']
            product['oos_request'] = self.check_stock_availability(size_value, response, garment)
            skus[self.get_complete_catalog_item_no(response) + '_' + size_value] = sku
        return skus

    def get_std_promotion(self, response):
        return response.xpath('//input[@name="artNr"]//@value').extract_first()[6:]

    def get_complete_catalog_item_no(self, response):
        return response.xpath('//input[@name="artNr"]//@value').extract_first()

    def check_stock_availability(self, size, response, garment=None):
        item_no = self.get_complete_catalog_item_no(response)
        promotion = self.get_std_promotion(response)
        article = Article(item_no, size, promotion)
        garment.generate_one_product(article)
        return garment

    def parse_oos(self, response):
        product = response.meta['product']
        root = ET.fromstring(response.body)
        for article in root.iter('Article'):
            stock = ET.tostring(article.findall('.//Stock')[0], method="text").strip() \
                if article.findall('.//Stock') else None
            if stock == '0':
                item_no = ET.tostring(article.findall('.//CompleteCatalogItemNo')[0], method="text").strip()
                size = ET.tostring(article.findall('.//SizeAlphaText')[0], method="text").strip()
                product['skus'][item_no + '_' + size]['out_of_stock'] = True
        product.pop('oos_request')
        return product

    def next_color_requests(self, product):
        if product['requests']:
            req = product['requests'].pop()
            req.meta['product'] = product
            return req
        else:
            product.pop('requests')
            return self.make_oos_request(product)

    def make_oos_request(self, product):
        body = product['oos_request'].get_xml()
        url = 'http://www.sheego.de/request/kal.php'
        headers = {"Content-Type": "application/xml; charset=UTF-8",
                   "Accept": "application/xml, text/xml, */*; q=0.01",
                   "X-Requested-With": "XMLHttpRequest"}
        return Request(url=url, method="POST", headers=headers, body=body, callback=self.parse_oos,
                       dont_filter=True, meta={'product': product})


class GenerateXML(object):
    def __init__(self):
        self.xml = ''
        self.append_static_elements()

    def generate_one_product(self, article):
        parent = self.xml.find('.//Articles')
        art = ET.SubElement(parent, 'Article')
        item = ET.SubElement(art, 'CompleteCatalogItemNo')
        item.text = str(article.complete_catalog_item_no)
        size = ET.SubElement(art, 'SizeAlphaText')
        size.text = str(article.size_alpha_text)
        promo = ET.SubElement(art, 'Std_Promotion')
        promo.text = article.std_promotion
        cust_id = ET.SubElement(art, 'CustomerCompanyID')
        cust_id.text = str(article.customer_company_id)

    def append_static_elements(self):
        a = ET.Element('tns:KALAvailabilityRequest')
        a.set("xmlns:tns", "http://www.schwab.de/KAL")
        a.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        a.set("xsi:schemaLocation",
              "http://www.schwab.de/KAL "
              "http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd")
        ET.SubElement(a, 'Articles')
        self.xml = a

    def get_xml(self):
        return ET.tostring(self.xml)


class Article(object):
    def __init__(self, complete_catalog_item_no='', size_alpha_text='', std_promotion='R', customer_company_id=0):
        self.complete_catalog_item_no = complete_catalog_item_no
        self.size_alpha_text = size_alpha_text
        self.std_promotion = std_promotion
        self.customer_company_id = customer_company_id

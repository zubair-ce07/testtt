import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sheego_spider.items import SheegoSpiderItem
import re
import xml.etree.ElementTree as ET
from scrapy.http import Request


class SheegoSpider(CrawlSpider):
    name = 'sheego_spider'
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths=['//ul[@class="mainnav__ul js-mainnav-ul"]',
                             '//ul[@class="navigation pl-side-box "]',
                             '//div[@class="js-product-list-paging paging"]'])),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="row product__list at-product-list"]']),
             callback='parse_item'))

    def parse_item(self, response):
        item = SheegoSpiderItem()
        item['gender'] = 'women'
        item['category'] = self.item_category(response)
        item['brand'] = self.item_brand(response)
        item['pid'] = re.search('(\d+)', response.url).group(1)
        item['image_urls'] = []
        item['description'], item['care'] = self.item_description_care(response)
        item['skus'] = {}
        item['name'] = self.item_name(response)
        item['url_original'] = response.url
        colour_links = [response.urljoin(x) for x in
                       response.xpath('//div[contains(@class,"moreinfo-color colors")]/ul/li/a/@href').extract()]
        kal_body = self.generate_xml(response)
        request = Request(url='https://www.sheego.de/request/kal.php',
                          method='POST',
                          callback=self.parse_kal,
                          headers={'Content-Type' : 'application/xml'},
                          body=kal_body)
        request.meta['item'] = item
        request.meta['url'] = colour_links[0]
        return request

    def generate_xml(self, response):
        kal_data = self.get_text(response, '//script[contains(text(), "setKALAvailability" )]/text()')
        kal_data = re.search('String\(\'(\w+;\w+(;\w+;\w+)+)', kal_data).group(1).split(';')
        articles = ET.Element('Articles')
        for colour_code, size in zip(kal_data[0::2], kal_data[1::2]):
            article = ET.Element('Article')
            item_no = ET.Element('CompleteCatalogItemNo')
            item_no.text = colour_code
            item_size = ET.Element('SizeAlphaText')
            item_size.text = size
            item_promotion = ET.Element('Std_Promotion')
            item_promotion.text = re.search('(\d{2}|[A-z])$', colour_code).group(1)
            item_id = ET.Element('CustomerCompanyID')
            item_id.text = '0'
            article.extend([item_no, item_size, item_promotion, item_id])
            articles.append(article)
        kal_availability = ET.Element('tns:KALAvailabilityRequest',
                                      attrib={'xmlns:tns':"http://www.schwab.de/KAL",
                                              'xmlns:xsi' : "http://www.w3.org/2001/XMLSchema-instance",
                                              'xsi:schemaLocation' : "http://www.schwab.de/KAL http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd"})
        kal_availability.append(articles)
        return ET.tostring(kal_availability).decode("utf-8")

    def parse_kal(self, response):
        item = response.meta['item']
        url = response.meta['url']
        colour_links = []
        root = ET.fromstring(response.body.decode("utf-8"))
        articles_available = {}
        articles_unavailable = {}
        if root.findall('.//LocalError'):
            item['skus'] = "out of stock"
            return item
        availablities = root.findall('.//ArticleAvailability')
        for availabity in availablities:
            item_code = availabity.find('.//CompleteCatalogItemNo').text
            articles_available[item_code] = []
            articles_unavailable[item_code] = []
        for availabity in availablities:
            item_code = availabity.find('.//CompleteCatalogItemNo').text
            if availabity.find('.//Stock').text == '1' or\
                            availabity.find('.//DeliveryDesignation').text == '2' or\
                            availabity.find('.//DeliveryDesignation').text == '0':
                articles_available[item_code].append(availabity.find('.//SizeAlphaText').text)
            else:
                articles_unavailable[item_code].append(availabity.find('.//SizeAlphaText').text)
        colour_codes = articles_available.keys()
        sizes_in_stock = list(articles_available.values())
        sizes_out_of_stock = list(articles_unavailable.values())
        for colour_code in colour_codes:
            promotion_id = re.search('(\d{2}|[A-z])$', colour_code).group(1)
            splitted_url = url.split('-')
            splitted_url[-1] = promotion_id + re.search('(\w.html)',url).group(1)
            splitted_url[-2] = colour_code.rstrip(promotion_id)
            colour_links.append('-'.join(splitted_url))
        return self.get_next_colour(colour_links, sizes_in_stock, sizes_out_of_stock, item)


    def get_next_colour(self, colour_links, sizes_in_stock, sizes_out_of_stock, item):
        if not colour_links:
            return item
        url = colour_links.pop(0)
        request = Request(url=url, callback=self.parse_colour, dont_filter=True)
        request.meta['colour_links'] = colour_links
        request.meta['item'] = item
        request.meta['sizes_in_stock'] = sizes_in_stock
        request.meta['sizes_out_of_stock'] = sizes_out_of_stock
        return request

    def parse_colour(self, response):
        item = response.meta['item']
        colour_links = response.meta['colour_links']
        sizes_in_stock = response.meta['sizes_in_stock']
        sizes_out_of_stock = response.meta['sizes_out_of_stock']
        sizes_unavailable = sizes_out_of_stock.pop(0)
        for size in sizes_unavailable:
            size_variant = self.get_text(response,
                                         '//select[contains(@class,"variants js-variantSelector js-moreinfo-variant js-sh-dropdown")]'
                                         '/option[contains(@selected,"selected")]/text()')
            if size_variant:
                size = size + '_' + size_variant
            colour = self.sku_colour(response)
            item['skus'][colour + '_' + size] = {'out_of_stock' : True, 'currency' : 'EUR', 'Colour' : colour, 'size' : size}
        sizes_available = sizes_in_stock.pop(0)
        item['image_urls'].extend(self.item_image_urls(response))
        size_data = []
        if sizes_available:
            aid = ' '.join(response.xpath('//input[contains(@name,"aid")]/@value').extract())
            for size in sizes_available:
                splitted_aid = aid.split('-')
                splitted_aid[-2] = size.split('/')[0]
                size_data.append('-'.join(splitted_aid))
        return self.get_next_size(response, size_data, colour_links, sizes_in_stock,sizes_out_of_stock, item)

    def item_image_urls(self, response):
        return response.xpath('//div[contains(@class,"thumbs")]//a/@data-image').extract()

    def get_next_size(self, response, size_data, colour_links, sizes_in_stock, sizes_out_of_stock, item):
        if size_data:
            aid = size_data.pop()
            formdata = {}
            formdata['anid'] = aid
            formdata['varselid[0]'] = response.xpath('//input[contains(@name,"varselid[0]")]/@value').extract()[0]
            if response.xpath('//div[contains(@id,"variants")]/div/select/option/text()').extract():
                formdata['varselid[1]'] = response.xpath('//input[contains(@name,"varselid[1]")]/@value').extract()[0]
            request = scrapy.FormRequest.from_response(response, formdata = formdata, callback=self.parse_size, formnumber=1)
            request.meta['form_response'] = response
            request.meta['formdata'] = formdata
            request.meta['sizes_in_stock'] = sizes_in_stock
            request.meta['sizes_out_of_stock'] = sizes_out_of_stock
            request.meta['size_data'] = size_data
            request.meta['colour_links'] = colour_links
            request.meta['item'] = item
            return request
        else:
            return self.get_next_colour(colour_links, sizes_in_stock, sizes_out_of_stock, item)

    def parse_size(self, response):
        form_response = response.meta['form_response']
        size_data = response.meta['size_data']
        sizes_in_stock = response.meta['sizes_in_stock']
        sizes_out_of_stock = response.meta['sizes_out_of_stock']
        item = response.meta['item']
        colour_links = response.meta['colour_links']
        if not (response.xpath('//div[contains(@id,"articlenotfound")]').extract()
                or response.xpath('//div[contains(@class,"searchagain")]/h2/text()').extract()):
            skus = self.item_sku(response)
            item['skus'][skus['colour'] + '_' + skus['size']] = skus
            return self.get_next_size(form_response, size_data, colour_links, sizes_in_stock,sizes_out_of_stock, item)
        else:
            return self.get_next_size(form_response, size_data, colour_links, sizes_in_stock,sizes_out_of_stock, item)

    def item_sku(self, response):
        skus = {}
        skus['price'], skus['previous_prices'] = self.sku_price(response)
        skus['currency'] = 'EUR'
        skus['colour'] = self.sku_colour(response)
        skus['size'] = self.sku_size(response)
        return skus

    def sku_price(self, response):
        price = self.normalize_string(
            self.get_text(response, '//span[contains(@class,"lastprice at-lastprice")]/text()'))
        previous_prices = [
            self.normalize_string(self.get_text(response, '//*[contains(@class, "wrongprice at-wrongprice")]//text()'))]
        return price, previous_prices

    def sku_colour(self, response):
        return ' '.join(response.xpath('//a[contains(@class,"color-item active js-ajax ")]/@title').extract())

    def sku_size(self, response):
        return self.normalize_string(self.get_text(response, '//span[contains(@class,"at-dv-size")]/text()'))

    def normalize_string(self, input_string):
        return ''.join(input_string.split())

    def get_text(self, response, xpath):
        return ' '.join(response.xpath(xpath).extract())

    def item_category(self, response):
        return response.xpath('//ul[contains(@class,"breadcrumb")]/li/a/text()').extract()[1:]

    def item_brand(self, response):
        return self.normalize_string(self.get_text(response,
                                                   '//div[contains(@class,"brand")]/text()'
                                                    ' | //div[contains(@class,"product-header visible-sm visible-xs")]//div[contains(@class,"brand")]/a/text()'))

    def item_name(self, response):
        return self.normalize_string(self.get_text(response,
                                                   '//div[contains(@class,"product-header visible-sm visible-xs")]//span[contains(@itemprop,"name")]/text()'))

    def item_description_care(self, response):
        care = []
        care_instructions = self.get_text(response,
                                          '//div[contains(@class,"js-articledetails")]//dl[contains(@class,"dl-horizontal articlecare")]/dt/text()')
        if care_instructions:
            care.append(care_instructions)
            care.append(' '.join(set(response.xpath(
                '//dl[contains(@class,"dl-horizontal articlecare")]//template[contains(@class,"js-tooltip-content")]/b/text()').extract())))
        description = response.xpath('//div[contains(@id,"moreinfo-highlight")]/ul/li/text()').extract()
        description.append(self.normalize_string
                           (' '.join(response.xpath('//div[contains(@id,"js-morearticles-desktop")]/following-sibling::div/div//text()').extract())))
        description_selectors = response.xpath\
            ('//div[contains(@class, "col-xs-12 visible-xs articledetails clearfix")]//div[contains(@class,"js-articledetails")]//tr')
        for description_selector in description_selectors:
            further_details = self.get_text(description_selector, './/text()')
            if 'Material' in further_details:
                care.append(further_details)
            else:
                description.append(further_details)
        description.append(self.normalize_string
                           (response.xpath('//div[contains(@class,"js-articledetails")]/dl[contains(@class,"dl-horizontal articlenumber")]//text()').extract()[0]))
        return description, care


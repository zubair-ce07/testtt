import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sheego_spider.items import SheegoSpiderItem
from lxml import etree
import re
import xml.etree.ElementTree as ET

class SheegoSpider(CrawlSpider):
    name = 'sheego_spider'
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths=['//ul[@class="mainnav__ul js-mainnav-ul"]', '//ul[@class="navigation pl-side-box "]',
                             '//div[@class="js-product-list-paging paging"]'])),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="row product__list at-product-list"]']),
             callback='parse_item'))

    def parse_item(self, response):
        item = SheegoSpiderItem()
        item['gender'] = 'women'
        item['category'] = self.item_category(response)
        item['brand'] = self.item_brand(response)
        item['image_urls'] = []
        item['description'], item['care'] = self.item_description_care(response)
        item['skus'] = {}
        item['name'] = self.item_name(response)
        item['url_original'] = response.url
        color_links = [response.urljoin(x) for x in
                       response.xpath('//div[@class="moreinfo-color colors"]/ul/li/a/@href').extract()]
        kal_body = self.generate_kal_body(response)
        request = scrapy.Request(url='https://www.sheego.de/request/kal.php', method='POST',callback=self.parse_kal,
                                 headers={'Origin' : 'https://www.sheego.de', 'Referer' : response.url, 'X-Requested-With' : 'XMLHttpRequest',
                                          'Content-Type' : 'application/xml', 'charset' : 'UTF-8', 'Host' : 'www.sheego.de'},
                                 body=kal_body)
        request.meta['item'] = item
        request.meta['url'] = color_links[0]
        return request

    def generate_kal_body(self, response):
        kal_data = self.get_text(response, '//script[@type="text/javascript" and contains(text(), "setKALAvailability" )]/text()')
        kal_data = re.search('String\(\'(\w+;\w+(;\w+;\w+)+)', kal_data).group(1).split(';')
        articles = etree.Element('Articles')
        while kal_data:
            article = etree.Element('Article')
            item_no = etree.Element('CompleteCatalogItemNo')
            color_code = kal_data.pop(0)
            item_no.text = color_code
            item_size = etree.Element('SizeAlphaText')
            item_size.text = kal_data.pop(0)
            item_promotion = etree.Element('Std_Promotion')
            item_promotion.text = re.search('(\d{2}|[A-z])$', color_code).group(1)
            item_id = etree.Element('CustomerCompanyID')
            item_id.text = '0'
            article.extend([item_no, item_size, item_promotion, item_id])
            articles.append(article)
        kal_start = '<?xml version="1.0" encoding="utf-8"?>' \
                    '<tns:KALAvailabilityRequest xmlns:tns="http://www.schwab.de/KAL" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
                    'xsi:schemaLocation="http://www.schwab.de/KAL http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd">'
        kal_end = '</tns:KALAvailabilityRequest>'
        return kal_start + etree.tostring(articles).decode("utf-8") + kal_end

    def parse_kal(self, response):
        item = response.meta['item']
        url = response.meta['url']
        colour_links = []
        root = ET.fromstring(response.body.decode("utf-8"))
        articles_available = {}
        if not root.findall('.//LocalError'):
            availablities = root.findall('.//ArticleAvailability')
            for availabity in availablities:
                if availabity.find('.//Stock').text == '1' or availabity.find('.//DeliveryDesignation').text == '2':
                    item_code = availabity.find('.//CompleteCatalogItemNo').text
                    if item_code in articles_available:
                        articles_available[item_code].append(availabity.find('.//SizeAlphaText').text)
                    else:
                        articles_available[item_code] = [availabity.find('.//SizeAlphaText').text]
            colour_codes = articles_available.keys()
            sizes_in_stock = list(articles_available.values())
            for colour_code in colour_codes:
                promotion_id = re.search('(\d{2}|[A-z])$', colour_code).group(1)
                splitted_url = url.split('-')
                splitted_url[-1] = promotion_id + re.search('(\w.html)',url).group(1)
                splitted_url[-2] = colour_code.rstrip(promotion_id)
                colour_links.append('-'.join(splitted_url))
            return self.get_next_colour(colour_links, sizes_in_stock, item)
        else:
            item['skus'] = "out of stock"
            return item

    def get_next_colour(self, colour_links, sizes_in_stock, item):
        if colour_links:
            url = colour_links.pop(0)
            request = scrapy.Request(url=url, callback=self.parse_colour, dont_filter=True)
            request.meta['colour_links'] = colour_links
            request.meta['item'] = item
            request.meta['sizes_in_stock'] = sizes_in_stock
            return request
        else:
            return item

    def parse_colour(self, response):
        item = response.meta['item']
        colour_links = response.meta['colour_links']
        sizes_in_stock = response.meta['sizes_in_stock']
        sizes = sizes_in_stock.pop(0)
        item['image_urls'].extend(self.item_image_urls(response))
        size_data = []
        if sizes:
            parentid = ' '.join(response.xpath('//input[@name="parentid"]/@value').extract())
            splitted_parentid = parentid.rsplit("-", 1)
            for size in sizes:
                aid = splitted_parentid[0] + '-' + size.split('/')[0] + '-' + splitted_parentid[1]
                aid = aid[:-1]  # the last letter of url (aid) is not needed in form request aid
                size_data.append(aid)
        return self.get_next_size(response, size_data, colour_links, sizes_in_stock, item)

    def item_image_urls(self, response):
        return response.xpath('//div[@class="thumbs"]//a/@data-image').extract()

    def get_next_size(self, response, size_data, colour_links, sizes_in_stock, item):
        if size_data:
            aid = size_data.pop()
            formdata = {}
            formdata['anid'] = aid
            formdata['varselid[0]'] = response.xpath('//input[@name="varselid[0]"]/@value').extract()[0]
            if response.xpath('//div[@id="variants"]/div/select/option/text()').extract():
                formdata['varselid[1]'] = response.xpath('//input[@name="varselid[1]"]/@value').extract()[0]
            request = scrapy.FormRequest.from_response(response, formdata = formdata, callback=self.parse_size, formnumber=1)
            request.meta['form_response'] = response
            request.meta['formdata'] = formdata
            request.meta['sizes_in_stock'] = sizes_in_stock
            request.meta['size_data'] = size_data
            request.meta['colour_links'] = colour_links
            request.meta['item'] = item
            return request
        else:
            return self.get_next_colour(colour_links, sizes_in_stock, item)

    def parse_size(self, response):
        form_response = response.meta['form_response']
        size_data = response.meta['size_data']
        sizes_in_stock = response.meta['sizes_in_stock']
        item = response.meta['item']
        colour_links = response.meta['colour_links']
        if not (response.xpath('//div[@id="articlenotfound"]').extract() or response.xpath('//div[@class="searchagain"]/h2/text()').extract()):
            skus = self.item_sku(response)
            item['skus'][skus['colour'] + '_' + skus['size']] = skus
            return self.get_next_size(form_response, size_data, colour_links, sizes_in_stock, item)
        else:
            return self.get_next_size(form_response, size_data, colour_links, sizes_in_stock, item)

    def item_sku(self, response):
        skus = {}
        skus['price'], skus['previous_prices'] = self.sku_price(response)
        skus['currency'] = 'EUR'
        skus['colour'] = self.sku_colour(response)
        skus['size'] = self.sku_size(response)
        return skus

    def sku_price(self, response):
        if response.xpath('//span[@class="lastprice at-lastprice"]/sub').extract():
            price = self.normalize_string(
                self.get_text(response, '//span[@class="lastprice at-lastprice"]/sub/following-sibling::text()'))
            previous_prices = [
                self.normalize_string(self.get_text(response, '//span[@class="lastprice at-lastprice"]/sub/text()'))]
        else:
            previous_prices = []
            price = self.normalize_string(
                self.get_text(response, '//span[@class="lastprice at-lastprice"]/text()'))
        return price, previous_prices

    def sku_colour(self, response):
        return ' '.join(response.xpath('//a[@class="color-item active js-ajax "]/@title').extract())

    def sku_size(self, response):
        return response.xpath('//span[@class="at-dv-size"]/text()').extract()[0].split(' ')[1]

    def normalize_string(self, input_string):
        return ''.join(input_string.split())

    def get_text(self, response, xpath):
        return ' '.join(response.xpath(xpath).extract())

    def item_category(self, response):
        return response.xpath('//ul[@class="breadcrumb"]/li/a/text()').extract()[1:]

    def item_brand(self, response):
        return self.normalize_string(self.get_text(response, '//div[@class="brand"]/text()')) or \
               self.normalize_string(self.get_text(response,
                                                   '//div[@class="product-header visible-sm visible-xs"]//div[@class="brand"]/a/text()'))

    def item_name(self, response):
        return self.normalize_string(self.get_text(response,
                                                   '//div[@class="product-header visible-sm visible-xs"]//span[@itemprop="name"]/text()'))

    def item_description_care(self, response):
        description = response.xpath('//div[@id="moreinfo-highlight"]/ul/li/text()').extract()
        description.append(' '.join(set(response.xpath('//div[@itemprop="description"]//text()').extract())))
        description_selectors = response.xpath('//div[@class="js-articledetails"]//tr')
        for description_selector in description_selectors:
            description.append(self.get_text(description_selector, './/text()'))
        description.append(self.normalize_string(self.get_text(response,
                                                               '//div[@class="js-articledetails"]/dl[@class="dl-horizontal articlenumber"]//text()')))
        care = []
        care_instructions = self.get_text(response,
                                          '//div[@class="js-articledetails"]//dl[@class="dl-horizontal articlecare"]/dt/text()')
        if care_instructions:
            care.append(care_instructions)
            care.append(' '.join(set(response.xpath(
                '//dl[@class="dl-horizontal articlecare"]//template[@class="js-tooltip-content"]/b/text()').extract())))
        item_content = self.get_text(response, '//div[@itemprop="description"]/br/following-sibling::text()')
        if item_content:
            material_content = self.normalize_string(' '.join(item_content))
            # in some cases the item content does not contain material composition
            if '%' in material_content:
                care.append(material_content)
        care.extend([s for s in description if 'Material' in s])
        # material description needs to be omitted becuase it will be a part of item_care
        return [s for s in description if 'Material' not in s], care


from scrapy import Request
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider, Rule
from scrapy import Spider
from sheego.items import SheegoItem
import re
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.etree.ElementTree as ET

key_sheegoItem = 'sheegoItem'
key_url_product = 'url'
key_urls = 'urls'

pid = 'pid'
url_original = 'url_original'
brand = 'brand'
name = 'name'
image_urls = 'image_urls'
description = 'description'
category = 'category'
skus = 'skus'
care = 'care'
gender = 'gender'
out_of_stock = 'out_os_stock'


def strip(obj):
    return ''.join(list(map(lambda x: x.strip(), ' '.join(obj))))


def parse_brand(response):
    brand_text = response.css('.brand a::text').extract() or response.css('.brand::text').extract()
    return strip(brand_text[0])


def parse_pid(response):
    return re.search('_(\d+)', response.url).group(1)


def parse_name(response):
    title = response.css(
        '.productDetailBox.productDetailBox--title .at-dv-itemName::text').extract()
    return strip(title)


def parse_image_urls(response):
    return response.css('#thumbslider a::attr(data-zoom-image)').extract()


def parse_description(response):
    small_description = response.css('#moreinfo-highlight li::text').extract()
    detail_selector = response.css('.js-articledetails.at-dv-itemDetails')
    detail_paragraph = detail_selector.css('.l-outsp-bot-10::text').extract()
    detail_table = detail_selector.css('.tmpArticleDetailTable tr')
    detail_table_data = list(map(lambda x: snap_detail_table_row(x), detail_table))
    article_no = detail_selector.css('.dl-horizontal.articlenumber')

    full_description = small_description + detail_paragraph + detail_table_data
    full_description.append(strip(article_no.css('dt::text, dd::text').extract()))

    return list(filter(lambda x: x.strip(), full_description))


def snap_detail_table_row(xcss):
    return strip(xcss.css('span::text').extract()) + strip(
        xcss.css('td:nth-child(2)::text').extract())


def parse_variant_urls(response):
    meta_data = response.meta
    root = ET.fromstring(response.body.decode('utf-8'))
    articles_available = {}

    for CCIN in set(map(lambda x: x.text, root.findall('.//CompleteCatalogItemNo'))):
        articles_available[CCIN] = []

    for article in root.findall('.//Article'):
        if not article.find('.//ArticleError') and article.find('.//DeliveryStatement').text != '0':
            articles_available[article.find('.//CompleteCatalogItemNo').text].append(
                article.find('.//SizeAlphaText').text)
    articles_available = {k: v for k, v in articles_available.items() if v}
    initial_url = re.search('(\S+)_\d+', meta_data[key_url_product]).group(0)
    urls = []
    url_format = '%s-%s-%s-%s.html'
    for CCIN, sizes in articles_available.items():
        urls = urls + list(map(lambda size:
                               (url_format % (initial_url, CCIN[:6], size, CCIN[6:]))
                               , sizes))
    return urls


def process_kal_response(response):
    urls = parse_variant_urls(response)
    if not urls:
        sheego_item = response.meta[key_sheegoItem]
        sheego_item[skus][out_of_stock] = 'True'
        yield sheego_item
    else:
        yield request_variant_detail(urls, response.meta[key_sheegoItem])


def parse_price(response):
    newprice = strip(response.css('.lastprice.at-lastprice::text').extract())
    oldprice = strip(response.css('.wrongprice.at-wrongprice.l-outsp-right-5::text').extract())
    color = strip(response.css('.color-item.active.js-ajax::attr(title)').extract())
    variant_head = response.css('.js-variantSelector.size.clearfix .title')
    variant = strip(variant_head.css('div:contains("Variante") span::text').extract())[1:]
    size = strip(variant_head.css('div:contains("Grösse") span::text').extract())[1:]

    price = {
        'price': newprice,
        'color': color,
        'currency': 'EUR'
    }
    if size:
        price['size'] = size
    if oldprice:
        price['previous_prices'] = oldprice

    variant_key = '_'.join(list(filter(lambda value: value, [color, variant, size])))
    return variant_key, price


def parse_variant(response):
    variant_key, price = parse_price(response)
    response.meta[key_sheegoItem][skus][variant_key] = price

    response.meta[key_sheegoItem][image_urls] = list(
        set(response.meta[key_sheegoItem][image_urls] + parse_image_urls(response)))

    if response.meta[key_urls]:
        yield request_variant_detail(response.meta[key_urls],
                                     response.meta[key_sheegoItem])
    else:
        yield response.meta[key_sheegoItem]


def request_variant_detail(urls, sheego_item):
    url = urls.pop()

    meta_data_n = {key_url_product: url, key_urls: urls, key_sheegoItem: sheego_item}
    return Request(url, callback=parse_variant, meta=meta_data_n)


def request_availabilities(response, sheego_item):
    return Request('https://www.sheego.de/request/kal.php', callback=process_kal_response,
                   method='POST', body=get_kal_params(response),
                   meta={key_url_product: response.url, key_sheegoItem: sheego_item})


def get_kal_params(response):
    kal_js = response.css('script:contains("kalrequest.articlesString")').extract()[0]
    kal_data = re.search('\'(\S+)\',\d', kal_js).group(1).split(';')

    CCINs = kal_data[0::2]
    SATs = kal_data[1::2]
    stdPs = list(map(lambda x: x[6:], CCINs))

    kal_param = Element('tns:KALAvailabilityRequest')
    kal_param.attrib = {'xmlns:tns': 'http://www.schwab.de/KAL',
                        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                        'xsi:schemaLocation': 'http://www.schwab.de/KAL http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd'}

    articles = SubElement(kal_param, 'Articles')
    for catalog_item_no, size, std in zip(CCINs, SATs, stdPs):
        article = SubElement(articles, 'Article')
        SubElement(article, 'CompleteCatalogItemNo').text = catalog_item_no
        SubElement(article, 'SizeAlphaText').text = size
        SubElement(article, 'Std_Promotion').text = std
        SubElement(article, 'CustomerCompanyID').text = '0'
    return tostring(kal_param)


class SheegoSpiderCrawler(CrawlSpider):
    name = "sheego_spider_crawler"
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de/']

    rules = (
        Rule(LinkExtractor(
            restrict_css=['.mainnav__entry.js-mainnav-entry', '.navigation.pl-side-box',
                          '.js-product-list-paging.paging .info'])),
        Rule(LinkExtractor(
            restrict_css='.product__item.js-product-box.js-unveil-plbox.at-product-box'),
            callback='parse_item'),
    )

    def parse_item(self, response):
        sheego_item = SheegoItem()
        sheego_item[url_original] = response.url
        sheego_item[pid] = parse_pid(response)
        sheego_item[name] = parse_name(response)
        sheego_item[brand] = parse_brand(response)
        sheego_item[image_urls] = parse_image_urls(response)
        sheego_item[description] = parse_description(response)
        sheego_item[gender] = 'women'
        sheego_item[skus] = {}

        yield request_availabilities(response, sheego_item)

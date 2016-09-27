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
    return ''.join(list(map(lambda x: x.strip(), ''.join(obj))))


def parse_brand(response):
    brand_text = response.css(".brand a::text").extract()
    if not brand_text:
        brand_text = response.css(".brand::text").extract()
    return strip(brand_text[0])


def parse_pid(response):
    splits = response.url.split("_", 1)
    return splits[1].split('-')[0]


def parse_name(response):
    title = response.css(
        '.productDetailBox.productDetailBox--title .at-dv-itemName::text').extract()
    return strip(title)


def parse_image_urls(response):
    return response.css("[id=thumbslider] a::attr(data-zoom-image)").extract()


def parse_description(response):
    startdesc = response.css("[id=moreinfo-highlight] li::text").extract()

    detail = response.css(".js-articledetails.at-dv-itemDetails")
    item_property = detail.css(".l-outsp-bot-10::text").extract()
    startdesc = startdesc + item_property
    detail_table = detail.css(".tmpArticleDetailTable tr")
    startdesc = startdesc + list(map(lambda x: ' '.join([x.css("span::text").extract()[0].strip(),
                                                         x.css("td:nth-child(2)::text").extract()[
                                                             0].strip()]), detail_table))
    artical_no = detail.css(".dl-horizontal.articlenumber")
    startdesc.append(strip(artical_no.css("dt::text").extract()))
    startdesc.append(strip(artical_no.css("dd::text").extract()))

    return list(filter(lambda x: x.strip(), startdesc))


def parse_variant_urls(response):
    meta_data = response.meta
    root = ET.fromstring(response.body.decode("utf-8"))
    articles_available = {}
    '''need to ask why does it not work'''
    # articles = list(filter(lambda x: x.find('.//ArticleAvailability'), root.findall('.//Article')))
    # print('Article', ET.tostring(articles, encoding='utf8', method='xml'))

    for CCIN in set(map(lambda x: x.text, root.findall('.//CompleteCatalogItemNo'))):
        articles_available[CCIN] = []

    for article in root.findall('.//Article'):
        if not article.find('.//ArticleError') and article.find('.//DeliveryStatement').text != '0':
            articles_available[article.find('.//CompleteCatalogItemNo').text].append(
                article.find('.//SizeAlphaText').text)
    articles_available = dict((k, v) for k, v in articles_available.items() if v)
    # articles_available = dict(filter(lambda x: x.v, articles_available.items()))
    splits = meta_data[key_url_product].split("_", 1)
    initial_url = splits[0]
    pid_no = splits[1].split('-')[0]
    urls = []

    for CCIN, sizes in articles_available.items():
        urls = urls + list(map(lambda size:
                               initial_url
                               + '_'
                               + '-'.join([pid_no, CCIN[:6], size, CCIN[6:]]) + '.html'
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
    variant = strip(response.css(
        '.variants.js-variantSelector.js-moreinfo-variant.js-sh-dropdown option::text').extract())
    size = strip(response.css('.js-sizeSelector.cover.js-moreinfo-size .active::text').extract())
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


def request_avalibilities(response, sheego_item):
    return Request('https://www.sheego.de/request/kal.php', callback=process_kal_response,
                   method='POST', body=get_kal_params(response),
                   meta={key_url_product: response.url, key_sheegoItem: sheego_item})


def get_kal_params(response):
    kal_js = response.css('script:contains("kalrequest.articlesString")').extract()[0]
    kal_data = re.search('String\(\'(.+)\',\d', kal_js).group(1).split(';')

    CCINs = kal_data[0::2]
    SATs = kal_data[1::2]
    stdPs = list(map(lambda x: x[6:], CCINs))

    kal_param = Element('tns:KALAvailabilityRequest')
    kal_param.attrib = {'xmlns:tns': "http://www.schwab.de/KAL",
                        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                        'xsi:schemaLocation': "http://www.schwab.de/KAL http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd"}

    articles = SubElement(kal_param, 'Articles')
    for catalog_item_no, size, std in zip(CCINs, SATs, stdPs):
        article = SubElement(articles, 'Article')
        SubElement(article, "CompleteCatalogItemNo").text = catalog_item_no
        SubElement(article, "SizeAlphaText").text = size
        SubElement(article, "Std_Promotion").text = std
        SubElement(article, "CustomerCompanyID").text = '0'
    return tostring(kal_param)


class SheegoSpiderCrawler(CrawlSpider):
    name = "sheego_spider_crawler"
    allowed_domains = ['sheego.de']
    start_urls = [
        'https://www.sheego.de/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=
                           ['.mainnav__entry.js-mainnav-entry'
                               , '.navigation.pl-side-box'
                               , '.js-product-list-paging.paging .info']
                           )
             ),
        Rule(LinkExtractor(restrict_css=
                           '.product__item.js-product-box.js-unveil-plbox.at-product-box')
             , callback='parse_item'),
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

        yield request_avalibilities(response, sheego_item)

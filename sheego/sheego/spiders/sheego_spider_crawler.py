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


def strip(obj):
    return ''.join(list(map(lambda x: x.strip(), ''.join(obj))))


def parse_brand(response):
    brand = response.css(".brand a::text").extract()
    if not brand:
        brand = response.css(".brand::text").extract()
    return strip(brand[0])


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

    description = response.css(".js-articledetails.at-dv-itemDetails")
    item_property = description.css(".l-outsp-bot-10::text").extract()
    for item in item_property:
        if (item.strip()):
            startdesc.append(item.strip())

    detail_table = description.css(".tmpArticleDetailTable tr")
    for detail in detail_table:
        startdesc.append(' '.join(
            [detail.css("span::text").extract()[0].strip(),
             detail.css("td:nth-child(2)::text").extract()[0].strip()]))

    artical_no = description.css(".dl-horizontal.articlenumber")
    startdesc.append(strip(artical_no.css("dt::text").extract()))
    startdesc.append(strip(artical_no.css("dd::text").extract()))

    return startdesc


def parse_variant_urls(response):
    meta_data = response.meta
    root = ET.fromstring(response.body.decode("utf-8"))
    articles_available = {}
    for CCIN in set(map(lambda x: x.text, root.findall('.//CompleteCatalogItemNo'))):
        articles_available[CCIN] = []

    for article in root.findall('.//Article'):
        articles_available[article.find('.//CompleteCatalogItemNo').text].append(
            article.find('.//SizeAlphaText').text)
    splits = meta_data[key_url_product].split("_", 1)
    initial_url = splits[0]
    pid = splits[1].split('-')[0]
    urls = []
    print(articles_available)
    for CCIN, sizes in articles_available.items():
        CIN = CCIN[6:]
        STDp = CCIN[:6]
        for size in sizes:
            url = '-'.join([pid, STDp, size, CIN])
            urls.append(initial_url + '_' + url + '.html')
    return urls


def process_kal_response(response):
    urls = parse_variant_urls(response)
    yield request_for_variant(urls, response.meta[key_sheegoItem])


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

    variant_key = color + '_' + variant + '_' + size
    return variant_key, price


def parse_variant(response):
    variant_key, price = parse_price(response)
    response.meta[key_sheegoItem][skus][variant_key] = price

    response.meta[key_sheegoItem][image_urls] = list(
        set(response.meta[key_sheegoItem][image_urls] + parse_image_urls(response)))

    if response.meta[key_urls]:
        yield request_for_variant(response.meta[key_urls],
                                  response.meta[key_sheegoItem])
    else:
        yield response.meta[key_sheegoItem]


def request_for_variant(urls, sheego_item):
    url = urls.pop()

    meta_data_n = {key_url_product: url
        , key_urls: urls
        , key_sheegoItem: sheego_item}
    return Request(url, callback=parse_variant, meta=meta_data_n)


def get_kal_params(response):
    kal_js = response.css('script:contains("kalrequest.articlesString")').extract()[0]
    kal_data = re.search('String\(\'(.+)\',\d', kal_js).group(1).split(';')

    CCINs = kal_data[0::2]
    SATs = kal_data[1::2]
    stdPs = list(map(lambda x: x[-1], CCINs))

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


class sheego_spider_crawler(CrawlSpider):
    name = "sheego_spider_crawler"
    allowed_domains = ['sheego.de']
    start_urls = [
        'https://www.sheego.de/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=
                           ['.mainnav__entry.js-mainnav-entry'
                               , '.navigation.pl-side-box']
                           )
             ),
        Rule(LinkExtractor(restrict_css=
                           '.product__item.js-product-box.js-unveil-plbox.at-product-box')
             , callback='parse_item'),
    )

    def parse_item(self, response):
        # class sheego_spider_crawler(Spider):
        #     name = "sheego_spider_crawler"
        #     allowed_domains = ["sheego.de"]
        #     start_urls = [
        #         # "https://www.sheego.de/sheego-kettenguertel-silber_421459234-652033-94p.html",
        #         # "https://www.sheego.de/sheego-trend-schmale-hose-schwarz_506378774-558545-Rp.html",
        #         'https://www.sheego.de/sheego-casual-suesses-shirtkleid-schwarz_243191760-541756-85p.html',
        #         # 'https://www.sheego.de/sheego-style-hose-grau_431500110-201657-94p.html',
        #         # 'https://www.sheego.de/lascana-strings-3-stueck-mit-spitze-cotton-made-in-africa-schwarz_313408932-442882-Yp.html',
        #         # 'https://www.sheego.de/tamaris-schnuerpumps-schwarz_526747825-516341-91p.html',
        #         # 'https://www.sheego.de/nuance-buegel-bh-fuer-perfekte-kurven-bunt_234435751-496590-Yp.html',
        #         # 'https://www.sheego.de/sheego-style-satinkleid-mit-spitze-grau_517798559-495573-91p.html'
        #     ]
        #
        #     def parse(self, response):
        sheego_item = SheegoItem()
        sheego_item[url_original] = response.url
        sheego_item[pid] = parse_pid(response)
        sheego_item[name] = parse_name(response)
        sheego_item[brand] = parse_brand(response)
        sheego_item[image_urls] = parse_image_urls(response)
        sheego_item[description] = parse_description(response)
        sheego_item[gender] = 'women'
        sheego_item[skus] = {}
        print(" -------------------------------------- URL : ", response.url)
        yield Request('https://www.sheego.de/request/kal.php'
                      , callback=process_kal_response
                      , method='POST'
                      , body=get_kal_params(response)
                      , meta={key_url_product: response.url,
                              key_sheegoItem: sheego_item})

import scrapy
import re
from sheego.items import Product
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


def clean_list(list):
    temp = []
    for item in list:
        temp.append(item.strip())
    return temp


def url(response, product):
    product['url'] = response.url.split('?')[0]


def brand(response, product):
    if response.css('.p-details__brand a'):
        product['brand'] = response.css('.p-details__brand a::text').extract_first().strip()
    else:
        product['brand'] = response.css('.p-details__brand::text').extract_first().strip()


def color(response, product):
    product['color'] = response.css('span.js-color-value::text').extract_first().lstrip('– ')


#

#
#


def details(response, product):
    product_details = {'bullets': response.css('div.at-dv-article-details ul li::text').extract()}
    if response.css('[itemprop=description] p'):
        description = response.css('[itemprop=description] p::text').extract_first()
    else:
        description = clean_list(response.css('[itemprop=description]::text').extract())
    product_details.update({'description': description})
    details_key = response.css('div.at-dv-article-details b::text').extract()
    details_value = response.css('div.at-dv-article-details p::text').extract()[1:]
    product_details.update(dict(zip(details_key, details_value)))
    product['details'] = product_details


def features(response, product):
    rows = response.css('table.p-details__material')[0].css('tr')
    desc = clean_list(rows.css('span::text').extract())
    values = list(filter(None, clean_list(rows.css('td::text').extract())))
    product['features'] = dict(zip(desc, values))


def material(response, product):
    if len(response.css('table.p-details__material')) > 1:
        rows = response.css('table.p-details__material')[1].css('tr')
    else:
        rows = response.css('table.p-details__material')[0].css('tr')
    desc = clean_list(rows.css('span::text').extract())
    values = list(filter(None, clean_list(rows.css('td::text').extract())))
    product['material'] = dict(zip(desc, values))


# def image_urls(response, product):
#     product['image_urls'] = response.css(
#         "div.product-image-gallery-thumbs.configurable *::attr(href)").extract()
#     # response.xpath("//div[@class='product-image-gallery-thumbs configurable']//@href").extract()
#
#
def name(response, product):
    product['name'] = response.css('h1[itemprop=name]::text').extract_first().strip()


#
#
# def color_urls(response, product):
#     product['color_urls'] = [n.strip() for n in response.css(
#         "ul.product-colors a::attr(href)").extract() if n != '#']
#     # [n.strip() for n in response.xpath("//ul[@class='product-colors']//a/@href").extract() if n != '#']
#
#
def retailer_id(response, product):
    product['retailer_id'] = response.css('.js-artNr::text').extract_first().strip().rstrip('W5')


#
#
# def skus(response, product):
#     sizes_list = list(filter(None, [n.strip() for n in response.css(
#         "div.sizebox-wrapper li::text").extract()]))
#     avail_list = response.css(
#         "div.sizebox-wrapper li::attr(data-qty)").extract()
#     # response.xpath("//div[@class='sizebox-wrapper']//li/@data-qty").extract()
#
#     for sizes in range(len(sizes_list)):
#         if int(avail_list[sizes]):
#             product['skus'].append({str(list(filter(None, response.css(
#                 "p.sku::text").re(r'(\d*)')))[0] + '_' + sizes_list[sizes]):
#                                         {'color': response.css("img.has-tip[title]::attr(title)").extract()[0],
#                                          'currency': response.css("script[type='application/ld+json']::text").re(
#                                              r'priceCurrency\":\"(\w*)')[0],
#                                          'price': ''.join(response.css("script[type='application/ld+json']::text").re(
#                                              r'price":(\d)*(\.\d*)?')),
#                                          'size': sizes_list[sizes]}})
#         else:
#             product['skus'].append({str(list(filter(None, response.css(
#                 "p.sku::text").re(r'(\d*)')))[0] + '_' + sizes_list[sizes]):
#                                         {'color': response.css("img.has-tip[title]::attr(title)").extract()[0],
#                                          'currency': response.css("script[type='application/ld+json']::text").re(
#                                              r'priceCurrency\":\"(\w*)')[0],
#                                          'price': ''.join(response.css("script[type='application/ld+json']::text").re(
#                                              r'price":(\d)*(\.\d*)?')),
#                                          'size': sizes_list[sizes], 'out_of_stock': 'true'}})


class SheegoSpider(CrawlSpider):
    name = 'sheego'
    allowed_domains = ['www.sheego.de']

    start_urls = [
        'https://www.sheego.de/damenschuhe/']
    rules = (
        # Rule(LinkExtractor(
        #     restrict_css="a.js-next")),
        Rule(LinkExtractor(
            restrict_css='a.product__top'), callback="parseprod"),)

    def parseprod(self, response):
        product = Product()
        # product['skus'] = []
        url(response, product)
        retailer_id(response, product)
        name(response, product)
        brand(response, product)
        details(response, product)
        features(response, product)
        material(response, product)
        color(response, product)
        # image_urls(response, product)

        # color_urls(response, product)

        # skus(response, product)
        yield product

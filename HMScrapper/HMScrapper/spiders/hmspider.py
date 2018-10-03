"""
HMSpider: A spider written to scrape all items of the H&M
brand's website from link https://kw.hm.com/en/ and store
the scrapped data.
"""
# -*- coding: utf-8 -*-
import json
import scrapy
from lxml import html
from HMScrapper.utilities import get, get_first
from HMScrapper.items import HmScrapperItem
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class HmSpider(CrawlSpider):
    """
    Spider class to scrape categories and follow callbacks to
    GET and POST requests to scrape all the items.
    """
    name = 'hmspider'
    allowed_domains = ['kw.hm.com']
    start_urls = ['https://kw.hm.com/en/']
    rules = [
        Rule(
            LinkExtractor(
                restrict_css="div[class *= 'field__item']",
                canonicalize=True,
                unique=True,
            ),
            callback="parse_item",
        ),
        Rule(
            LinkExtractor(
                restrict_css="li.pager__item",
                canonicalize=True,
                unique=True,
            ),
            follow=True,
        ),
        Rule(
            LinkExtractor(
                restrict_css="li[class *= 'menu--two__list-item']>div",
                canonicalize=True,
                unique=True,
            ),
            follow=True,
        ),
    ]

    def parse_item(self, response):
        """
        Callback for request to parse_item details from product page.
        :param response: response received by hitting the item-url
        :return: Yields item or request for
        scrapping the item-colors if present
        """
        description_path = "div.desc-value::text"
        discount_path = "div.price--discount::text"
        concept_path = "div.concept-value>ul>li::text"
        item_code_path = "div.content--item-code::text"
        care_info_path = "div.care-instructions-value::text"
        name_path = "div.content__title_wrapper>h1>span::text"
        price_path = "div.special--price span.price-amount::text"
        old_price_path = "div.has--special--price span.price-amount::text"
        comp_path = (
            'div.field__content-wrapper '
            'div.composition-value>ul>li::text'
        )

        hm_item = HmScrapperItem()
        discount = get_first(response, discount_path)
        if discount:
            discount = discount.split(" ")[1].split("%")[0]

        hm_item['color_skus'] = []
        hm_item['discount'] = discount
        hm_item['name'] = get_first(response, name_path)
        hm_item['composition'] = get(response, comp_path)
        hm_item['price'] = get_first(response, price_path)
        hm_item['concept'] = get_first(response, concept_path)
        hm_item['old_price'] = get_first(response, old_price_path)
        hm_item['care_info'] = get_first(response, care_info_path)
        hm_item['description'] = get_first(response, description_path)
        hm_item['item_code'] = get(response, item_code_path)[1].replace("\n", "")

        # get list of all colors for this item
        color_code_path = (
            "select[data-default-title *="
            " 'Color']>option+option::attr(value)"
        )
        sku_id_path = "div.content__sidebar article::attr(data-skuid)"
        form_id_path = (
            "form[class *= 'sku-base-form']"
            ">:nth-child(6)::attr(value)"
        )
        form_build_id_path = "button[class  *= 'cart']+input::attr(value)"
        color_codes = get(response, color_code_path)
        if not color_codes:
            yield hm_item
        else:
            # get data for post requests
            sku_id = get_first(response, sku_id_path)
            form_id = get_first(response, form_id_path)
            form_build_id = get_first(response, form_build_id_path)
            request_url = ('https://kw.hm.com/en/select-configurable-option'
                           '/{}?_wrapper_format=drupal_ajax').format(sku_id)
            form_data = {
                'configurables[article_castor_id]': color_codes[0],
                'sku_id': sku_id,
                'form_build_id': form_build_id,
                'form_id': form_id,
                '_triggering_element_name':
                    'configurables[article_castor_id]',
            }
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
            }
            request_meta = {
                'item': hm_item,
                'header': headers,
                'data': form_data,
                'color_codes': color_codes[1:],
            }
            yield scrapy.FormRequest(url=request_url,
                                     method='POST',
                                     callback=self.parse_color,
                                     headers=headers,
                                     meta=request_meta,
                                     formdata=form_data,
                                     dont_filter=True)

    def parse_color(self, response):
        """
        Callback function to scrape item color and size information.
        :param response: response received by POST request of an item.
        :return: yields the item after scrapping the color
        and size information of the item.
        """
        # get meta data from response
        hm_item = response.meta['item']
        header = response.meta['header']
        form_data = response.meta['data']
        color_codes = response.meta['color_codes']
        sizes_xpath = (
            "//select[contains(@name, 'size')]"
            "/option[not(@disabled)]/text()"
        )

        color_xpath = (
            "//select[contains(@name, 'castor_id')]"
            "/option[@selected]/text()"
        )

        # get sizes of current selected color from response body
        data = json.loads(response.body)
        for value in data:
            if 'replaceDynamicParts' in value.values():
                html_value = html.fromstring(value['args'][0]['replaceWith'])
                color_code = html_value.xpath(color_xpath)[0]
                sizes = html_value.xpath(sizes_xpath)
                color_sku = {
                    'color_code': color_code,
                    'sizes': sizes,
                }
                # append the color_sku to item
                hm_item['color_skus'].append(color_sku)
        # if more colors are left
        if color_codes:
            # update color code for next request
            form_data['configurables[article_castor_id]'] = color_codes[0]
            # create meta for next request
            meta = {
                'item': hm_item,
                'header': header,
                'data': form_data,
                'color_codes': color_codes[1:],
            }
            # yield request for next color
            yield scrapy.FormRequest(url=response.url,
                                     method='POST',
                                     callback=self.parse_color,
                                     headers=header,
                                     meta=meta,
                                     formdata=form_data,
                                     dont_filter=True)
        else:
            yield hm_item

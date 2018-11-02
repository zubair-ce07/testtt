"""
Helper functions for re-usability
"""
import json
import scrapy
from lxml import html


def get(response, path):
    """
    Returns the data fetched from response by using css selector
    :param response: response object to use by selector
    :param path: css selector path to use
    :return: list of data returned by css selector
    """
    return response.css(path).extract()


def get_first(response, path):
    """
    Returns the first element fetched from response
    by using css selector
    :param response: response object to use by selector
    :param path: css selector path to use
    :return: first item of list returned by css selector
    """
    return response.css(path).extract_first()


def parse_description(response):
    """
    parse the item description
    :param response: response object to parse detail from
    :return: description of item
    """
    description_path = "div.desc-value::text"
    return get_first(response, description_path)


def parse_discount(response):
    """
    parsing the discount of item
    :param response: response object to parse detail from
    :return: discount price of item
    """
    discount_path = "div.price--discount::text"
    discount = get_first(response, discount_path)
    if discount:
        discount = discount.split(" ")[1].split("%")[0]
    return discount


def parse_concept(response):
    """
    parsing the concept value of item
    :param response: response object to parse detail from
    :return: concept statement of item
    """
    concept_path = "div.concept-value>ul>li::text"
    return get_first(response, concept_path)


def parse_item_code(response):
    """
    parsing the item code
    :param response: response object to parse detail from
    :return: item code
    """
    item_code_path = "div.content--item-code::text"
    return get(response, item_code_path)[1].replace("\n", "")


def parse_care_info(response):
    """
    parsing the care instructions of the item
    :param response: response object to parse detail from
    :return: care instructions of item
    """
    care_info_path = "div.care-instructions-value::text"
    return get_first(response, care_info_path)


def parse_name(response):
    """
    parsing item name
    :param response: response object to parse detail from
    :return: item name
    """
    name_path = "div.content__title_wrapper>h1>span::text"
    return get_first(response, name_path)


def parse_price(response):
    """
    :param response: response object to parse detail from
    :return: item price
    """
    price_path = "div.special--price"
    if response.css(price_path) is None:
        # no discount, use simple value
        price_path = "div.content__title_wrapper span.price-amount::text"
    else:
        # discount given, use this path
        price_path = "{} span.price-amount::text".format(price_path)
    return get_first(response, price_path)


def parse_old_price(response):
    """
    :param response: response object to parse detail from
    :return: item old price
    """
    old_price_path = "div.has--special--price span.price-amount::text"
    return get_first(response, old_price_path)


def parse_composition(response):
    """
    :param response: response object to parse detail from
    :return: item composition information
    """
    comp_path = (
        'div.field__content-wrapper div.composition-value>ul>li::text'
    )
    return get(response, comp_path)


def parse_color_codes(response):
    """
    :param response: response object to parse detail from
    :return: color codes of item
    """
    color_code_path = (
        "select[data-default-title *= 'Color']>option+option::attr(value)"
    )
    return get(response, color_code_path)


def parse_sku_id(response):
    """
    :param response: response object to parse detail from
    :return: item sku id
    """
    sku_id_path = "div.content__sidebar article::attr(data-skuid)"
    return get_first(response, sku_id_path)


def parse_form_id(response):
    """
    :param response: response object to parse detail from
    :return: form id of item
    """
    form_id_path = (
        "form[class *= 'sku-base-form']>:nth-child(6)::attr(value)"
    )
    return get_first(response, form_id_path)


def parse_form_build_id(response):
    """
    :param response: response object to parse detail from
    :return: form build id
    """
    form_build_id_path = "button[class  *= 'cart']+input::attr(value)"
    return get_first(response, form_build_id_path)


def get_sizes_from_html(html_value):
    """
    :param html_value: html string to parse
    :return: sizes present in item sku
    """
    sizes_xpath = (
        "//select[contains(@name, 'size')]/option[not(@disabled)]/text()"
    )
    return html_value.xpath(sizes_xpath)


def get_color_from_html(html_value):
    """
    :param html_value: html string to parse
    :return: current selected color code of item
    """
    color_xpath = (
        "//select[contains(@name, 'castor_id')]/option[@selected]/text()"
    )
    return html_value.xpath(color_xpath)[0]


def prepare_parse_color_request(response, color_codes, hm_item):
    sku_id = parse_sku_id(response)
    form_id = parse_form_id(response)
    form_build_id = parse_form_build_id(response)
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
    return {
        'url': request_url,
        'meta': request_meta,
        'header': headers,
        'form_data': form_data,
    }

import asyncio
import json
import re

import lxml.html
import requests
from bs4 import BeautifulSoup


KITH_ITEMS = []


def soup_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def fetch_url(url):
    proxy = {"http": "http://116.12.51.238:8080"}
    response = requests.get(url, proxies=proxy)
    return response.text


async def parse_categories(html):
    soup = soup_url(html)
    category_links = []
    for anchor_tag in soup.find_all('a', attrs={'href': re.compile("https://kith.com/collections/.*")}):
        category_links.append(anchor_tag['href'])
    unique_links = list(set(category_links))
    for link in unique_links:
        asyncio.sleep(3)
        await parse_page_urls(link)
    with open('output_kith.json', 'w') as output:
        json.dump(KITH_ITEMS, output)


async def parse_page_urls(url):
    html = fetch_url(url)
    soup = soup_url(html)
    last_page_number, pagination_link = get_pages_number_link(soup)
    if pagination_link:
        for index in range(1, last_page_number + 1):
            if extract_item_urls(pagination_link + str(index)):
                await extract_item_urls(pagination_link + str(index))
    else:
        await extract_item_urls(html)


def get_pages_number_link(soup):
    page_numbers_links = []
    numbers = []
    for anchor_tag in soup.find_all('a', attrs={'href': re.compile("collections.*page.*")}):
        page_numbers_links.append(anchor_tag['href'])
    page_numbers = []
    for page in page_numbers_links:
        page_numbers.append(re.search('(?<=page=)\d+', page))
    for number in page_numbers:
        numbers.append(int(number.group(0)))
    if page_numbers:
        pagination_link = page_numbers_links[0]
        pagination_link = pagination_link[:-1]
        pagination_link = "https://kith.com{}".format(pagination_link)
        return max(numbers), pagination_link
    return 1, ""


def extract_item_urls(url):
    html = fetch_url(url)
    soup = soup_url(html)
    product_urls = []
    for anchor_tag in soup.find_all('a', attrs={'href': re.compile(".*/products/.*")}):
        product_urls.append("https://kith.com" + anchor_tag['href'])
    unique_urls = list(set(product_urls))
    for url in unique_urls:
        KITH_ITEMS.append(extract_item(url))


def extract_item(url):
    html = fetch_url(url)
    soup = soup_url(html)
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)
    item = {}
    item["name"] = parse_name(soup)
    item["price"] = parse_price(soup)
    item["product_id"], item["material"], item["description"] = parse_description(doc)
    item["color"] = parse_color(soup)
    item["img_urls"] = parse_img_urls(soup)
    item["sizes"] = parse_sizes(doc)
    item["url"] = url
    return item


def parse_sizes(doc):
    return doc.xpath('//div[contains(@class,"product-single-form-item")]/select/option/text()')


def parse_img_urls(soup):
    img_urls_regex = re.compile('js-super-slider-photo-img.*')
    img_details = soup.findAll("img", {"class": img_urls_regex})
    img_urls = []
    for image in img_details:
        img_urls.append(image['src'][2:])
    return img_urls


def parse_color(soup):
    color_regex = re.compile('product-header-title.*')
    color = soup.find("span", {"class": color_regex})
    return color.text.strip()


def parse_name(soup):
    name = soup.find("h1", {"class": "product-header-title"})
    return name.text.strip()


def parse_price(soup):
    price = soup.find("span", {"id": "ProductPrice"})
    return price.text.strip()


def cleanse_description(doc):
    description = doc.xpath('//div[contains(@class, "product-single-details-rte rte mb0")]/p/text()')
    info_list = filter(lambda name: name.strip(), description)
    info_list = filter(None, info_list)
    return info_list


def parse_description(doc):
    info_list = cleanse_description(doc)
    description_list = []
    product_id = ""
    material = ""
    for description in info_list:
        description = description.strip()
        sub_string_style = re.search(r'^Style: (.+?)$', description)
        sub_string_color = re.search(r'^Color: (.+?)$', description)
        sub_string_material = re.search(r'^Material: (.+?)$', description)
        if sub_string_style:
            product_id = sub_string_style.group(1)
        elif sub_string_color:
            pass
        elif sub_string_material:
            material = sub_string_material.group(1)
        else:
            description_list.append(description)
    if not description_list:
        description_list = doc.xpath('//div[contains(@class, "product-single-details-rte rte mb0")]/ul/li/text()')
    return product_id, material, description_list


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_categories(fetch_url("https://kith.com/")))


if __name__ == "__main__":
    main()

import scrapy
from scrapy.http import HtmlResponse
import requests
import re


class SheegoItem(scrapy.Item):
    fields_to_export = ['spiderName', 'category', 'url', 'retailer', 'image_url']
    spider_name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    retailer = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    product_urls = scrapy.Field()
    material = scrapy.Field()
    order_number = scrapy.Field()
    description = scrapy.Field()
    features = scrapy.Field()


class SheegoSpider(scrapy.Spider):
    name = "Sheego_Spider"
    start_urls = [
        'https://www.sheego.de/neu/alle-damenmode-neuheiten/',
        'https://www.sheego.de/damenmode/',
        'https://www.sheego.de/damen-waesche/',
        'https://www.sheego.de/bademode/',
        'https://www.sheego.de/damenschuhe/',
        'https://www.sheego.de/damenmode-sale/',
    ]

    def parse(self, response):
        for href in response.xpath("//a[contains(@class,'js-product__link')]/@href"):
            yield response.follow(href, self.scrap_item)
        next_page = response.xpath('//span[contains(@class,"paging__btn--next")]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def scrap_item(self, response):
        sheego_item = SheegoItem()
        sheego_item['url'] = response.url
        sheego_item['spider_name'] = "SheegoSpider"
        cateogries = list()
        for script_line in response.xpath("//div[contains(@class,'details__box--main')]/script/text()").extract():
            if "window.oTracking.data.productCategory" in script_line:
                category_regex = re.compile("'([^']*)'").search(script_line)
                category_regex = category_regex.group().replace("'", "")
                category_regex = category_regex + "/"
                for cateogry in re.split("/", category_regex):
                    cateogries.append(cateogry)
        sheego_item['category'] = cateogries
        sheego_item['retailer'] = "Sheego"

        image_urls = list()
        for url in response.xpath("//a[@id='magic']/@href"):
            image_urls.append(url.extract().strip())
        sheego_item['image_urls'] = image_urls

        order_number = response.xpath("//div[contains(@class,'cj-shCollapse__container__body')]"
                                      "/div[contains(@class,'l-mb-30')]")
        order_number = order_number.xpath("//span[contains(@class,'js-artNr')]/text()")
        sheego_item['order_number'] = order_number.extract_first().strip()
        sheego_item['description'] = response.xpath("//div[@itemprop='description']/text() "
                                                    "| //div[@itemprop='description']/p/text()").extract_first().strip()
        features = list()
        for feature in response.xpath("//div[contains(@class,'l-startext')]"
                                      "/div/ul[contains(@class,'l-list')]/li/text()"):
            features.append(feature.extract())
        sheego_item['features'] = features

        product_materials = response.xpath("//div[contains(@class,'cj-shCollapse__container__body')]"
                                           "/table[contains(@class,'p-details__material')]/tbody/tr")
        product_information_name = list()
        product_information_value = list()

        for product_material in product_materials:
            for information_name in product_material.xpath("//td/span/text()"):
                product_information_name.append(information_name.extract().strip())
            break

        for product_material in product_materials:
            for information_value in product_material.xpath("//td[2]/text()"):
                product_information_value.append(information_value.extract().strip())
            break
        product_additional_info = list()

        for index in range(0, len(product_information_name)):
            product_instruction = {product_information_name[index]: product_information_value[index]}
            product_additional_info.append(product_instruction)

        sheego_item['material'] = product_additional_info

        colors = response.xpath("//div[contains(@class,'cj-slider__slides')]/script/text()").extract_first().strip()
        colors = re.compile("\[([^\[\]]*)\]").search(colors)
        colors = colors.group()
        colors = colors.replace("[", "")
        colors = colors.replace("]", "")
        colors = colors.replace("'", "")
        colours = list()
        for color in re.split(",", colors):
            colours.append(color)
        main_page_url = response.url.split("?")[0] + "?color="
        urls = list()

        for color in colours:
            urls.append(main_page_url + color)
            sheego_item['product_urls'] = urls
            yield response.follow(main_page_url+color, self.scrap_sheego_item, meta={'sheego_item': sheego_item})

    def scrap_sheego_item(self, response):
        sheego_item = response.meta.get('sheego_item')
        urls = sheego_item['product_urls']
        sheego_skus_item = list()
        for url in urls:
            body_request = requests.get(url)
            response = HtmlResponse(url="url", body=body_request.content)
            sizes = response.xpath("//div[contains(@class,'c-sizespots')]")
            sizes_available = list()
            sizes_not_available = list()
            for size in sizes.xpath("//div[contains(@class,'at-dv-size-button')]/text()"):
                sizes_available.append(size.extract().strip())
            for size in sizes.xpath("//div[contains(@class,'sizespots__item--strike')]/text()"):
                sizes_not_available.append(size.extract().strip())

            product_color = response.xpath("//section[contains(@class,'p-details__variants')]")
            product_color = product_color.xpath("//section/p[contains(@class,'l-mb-5')]/text()").extract()

            price = response.xpath("//span[contains(@class,'product__price__current')][1]"
                                   "/text()").extract_first().strip()
            old_price = response.xpath("//span[contains(@class,'product__price__wrong')]/text()")

            if old_price.extract_first() is not None:
                old_price = old_price.extract_first().strip()
                price = {'old_price': old_price, 'new_price': price.strip()}

            for color in product_color:
                color = color.strip()
                if color != '':
                    product_color = color
                    break
            for size in sizes_available:
                name = size + "_" + product_color
                sheego_item_details = {"available": "true", "currency": "US", "colour": product_color,
                                       "price": price, "size": size}
                product_size_color = {name: sheego_item_details}
                sheego_skus_item.append(product_size_color)
            if len(sizes_not_available) > 0:
                for size in sizes_not_available:
                    name = size + "_" + product_color
                    sheego_item_details = {"available": "false", "currency": "US", "colour": product_color,
                                           "price": price, "size": size}
                    product_size_color = {name: sheego_item_details}
                    sheego_skus_item.append(product_size_color)
        sheego_item["skus"] = sheego_skus_item
        yield sheego_item


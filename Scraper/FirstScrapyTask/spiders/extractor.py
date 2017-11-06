import scrapy
import re

from scrapy.linkextractors import LinkExtractor


def extract_urls(response):
    allow_list = ['sneakers/', 'slides', 'casual', 'dress', 'boots', 'shoe-care', 'sandals', 'platforms', 'flats'
        , 'grade-school', 'youth', 'infant', 'baby']
    deny_list = ['pid']
    link = LinkExtractor(allow=allow_list, deny=deny_list)
    link_list = link.extract_links(response)

    url_list = []
    for row in link_list:
        url = str(row)
        url = re.search("(?P<url>https?://[^\s]+)", url).group("url")
        url_list.append(url[:-2])
    return url_list


def get_sizes(response):

        headings = response.css('ul#size-selector-desktop-tabs li a::text').extract()
        stock_size = response.css('div.col-sm-10 div#size-selector-tab-desktop-0 ul.list-inline li::attr(data-stock)').extract()
        sizes = {}
        for i in range(0, len(headings)):

            start_string = 'div.col-sm-10 div#size-selector-tab-desktop-'
            end_string = ' ul.list-inline a::text'
            number_string = str(i)
            complete_string = start_string + number_string + end_string
            complete_string = response.css(complete_string).extract()
            sizes[headings[i]] = complete_string
        sizes['Stock Status'] = stock_size
        return sizes


class HypeDcSpider(scrapy.Spider):

    name = "hypedc_spider"
    start_urls = ['https://www.hypedc.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):

        url_list = extract_urls(response)   # Extracting URL's using link extractor from the main website page

        for url in url_list:

            request = scrapy.Request(url=url, callback=self.parse_page2)
            yield request

    def parse_page2(self, response):
        all_urls = response.css('div.category-page-products div.item a::attr(href)').extract()

        # calling scrapy request for all the urls extracted from main page
        for url in all_urls:
            request = scrapy.Request(url=url, callback=self.parse_page3)
            yield request

        next_page = response.css('div.category-page-products div.next.col-xs-4 a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse_page2)

    def parse_page3(self, response):

        name = response.css('div.container div.col-sm-10 h1.product-name::text').extract_first()
        desc = response.css('div.product-description.std::text').extract_first()
        desc = desc.lstrip()
        desc = desc.rstrip()

        # Men Category
        category = response.css('div.container li.category4868 a::attr(title)').extract_first()

        # Women Category
        if not category:
            category = response.css('div.container li.category4893 a::attr(title)').extract_first()

        # Accessories Category
        if not category:
            category = response.css('div.container li.category4883 a::attr(title)').extract_first()

        # Kids Category With Sub Categories
        if not category:
            category = response.css('div.container li.category4919 a::attr(title)').extract_first()
            sub_category_1 = response.css('div.container li.category4920 a::attr(title)').extract_first()
            sub_category_2 = response.css('div.container li.category4921 a::attr(title)').extract_first()
            sub_category_3 = response.css('div.container li.category4922 a::attr(title)').extract_first()
            sub_category_4 = response.css('div.container li.category4923 a::attr(title)').extract_first()

            if sub_category_1:
                category = category + ' / ' + sub_category_1
            elif sub_category_2:
                category = category + ' / ' + sub_category_2
            elif sub_category_3:
                category = category + ' / ' + sub_category_3
            else:
                category = category + ' / ' + sub_category_4

        brand = response.css('div.container div.col-sm-10 h2.product-manufacturer::text').extract_first()
        color = response.css('div.container div.col-sm-10 h3.h4.product-colour::text').extract_first()
        color = color.rstrip()
        color = color.lstrip()
        product_code = response.css('div.container div.col-sm-10 div.product-code::text').extract_first()
        price = response.css('div.container div.col-sm-10 span.price-dollars::text').extract_first()
        price_c = response.css('div.container div.col-sm-10 span.price-cents::text').extract_first()
        url = response.url
        image_urls = response.css('div.slider-inner.col-sm-13.col-sm-offset-11 div.unveil-container img::attr(data-src)').extract()
        price_final = ''
        currency = ''
        sizes_info = get_sizes(response)

        # For Discounted Sale Price
        if not price:
            price_final = str(response.css('p.special-price span.price::text').extract_first())
            price_final = price_final.lstrip()
            price_final = price_final.rstrip()
            currency = price_final[0:1]

        # For Original Sale Price
        else:
            currency = price[0:1]
            price_final = price + price_c

        yield {'Name': name, 'Brand': brand, 'Category': category, 'URL': url, 'Product_id': product_code,
               'Price': price_final, 'Description': desc, 'Color': color, 'Currency': currency,
               'Image_URL s': image_urls , 'Sizes' : sizes_info}


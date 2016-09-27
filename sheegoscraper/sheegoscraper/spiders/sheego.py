from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import SheegoItem
from xml.etree.ElementTree import Element, SubElement, fromstring, tostring
import re
from scrapy.http import Request
from itertools import product


class SheegoSpider(CrawlSpider):
    name = "sheego"
    allowed_domains = ["sheego.de"]
    start_urls = ['https://www.sheego.de/']
    rules = [
        Rule(LinkExtractor(allow="sheego.de/", deny=["sheego.de/\?", "\?", "html"], restrict_css="#content"),
             follow=True),
        Rule(LinkExtractor(restrict_css=".product__item > div > div > .cj-active"),
             callback='parse_prodcut', follow=True),
        Rule(LinkExtractor(allow="sheego.de/", deny=["sheego.de/\?", "\.html"],
                           restrict_css=".next.js-next.btn.btn-next"))
    ]

    def parse_articles(self, response):
        articles = response.css("script:contains('articlesString')::text").extract()[0]
        articles_filtered = re.findall("([0-9A-Z]{3,8})\;([0-9]+)", articles)
        return articles_filtered

    def create_xml(self, response):
        root = Element('tns:KALAvailabilityRequest',
                       attrib={'xmlns:tns': "http://www.schwab.de/KAL",
                                'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                                'xsi:schemaLocation': "http://www.schwab.de/KAL "
                                "http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd"
                               })
        articles = SubElement(root, 'Articles')
        for article_id, size in self.parse_articles(response):
            article = SubElement(articles, 'Article')
            SubElement(article, "CompleteCatalogItemNo").text = article_id
            SubElement(article, "SizeAlphaText").text = size
            SubElement(article, "Std_Promotion").text = article_id[6:]
            SubElement(article, "CustomerCompanyID").text = '0'
        return tostring(root).decode("utf-8")

    def check_oos(self, response):
        request = Request(url='https://www.sheego.de/request/kal.php',
                          method='POST',
                          headers={'Content-Type': 'application/xml'},
                          callback=self.parse_oos,
                          body=self.create_xml(response))
        request.meta['item'] = response.meta['item']
        return request

    def parse_base_url(self, response):
        item = response.meta['item']
        return item['url_original'].split("_")[0] + "_" + item['product_id'] + "-{}-{}-{}.html"

    def parse_oos(self, response):
        item = response.meta['item']
        root = fromstring(response.body)
        urls = []
        skus = {}
        base_url = self.parse_base_url(response)
        for article in root.findall('.//Article'):
            size = article.find(".//SizeAlphaText").text
            stock = article.find(".//Stock").text
            catalog_id = article.find(".//CompleteCatalogItemNo").text
            sku_key = "{}_{}".format(catalog_id, size)
            if stock is '1':
                url = base_url.format(catalog_id[:6], size, catalog_id[6:])
                urls.append({"url": url, "sku_key": sku_key})
            else:
                skus[sku_key] = {}
                skus[sku_key]['oos'] = True
        if urls:
            request = Request(urls[0]['url'], callback=self.parse_sku)
            item['skus'] = skus
            request.meta['item'] = item
            request.meta['urls'] = urls
            return request
        else:
            item['skus']['oos'] = True
            return item

    def parse_sku(self, response):
        item = response.meta['item']
        urls = response.meta['urls']
        sku_key = urls.pop(0)['sku_key']
        sku = {}
        sku['color'] = self.parse_color(response)
        sku['price'] = self.parse_price(response)
        sku['previous_prices'] = self.parse_prev_price(response)
        sku['size'] = self.parse_size(response)
        sku['image_urls'] = self.parse_image_urls(response)
        sku['currency'] = 'EUR'
        item['skus'][sku_key] = sku
        if urls:
            request = Request(urls[0]['url'], callback=self.parse_sku)
            request.meta['item'] = item
            request.meta['urls'] = urls
            return request
        else:
            return item

    def parse_prodcut(self, response):
        item = SheegoItem()
        item['gender'] = 'Women'
        item['category'] = self.parse_category(response)
        item['url_original'] = response.url
        item['product_id'] = self.parse_product_id(response)
        item['name'] = self.parse_name(response)
        item['brand'] = self.parse_brand(response)
        item['care'] = self.parse_care(response)
        item['description'] = self.parse_description(response)
        item['skus'] = {}
        response.meta['item'] = item
        return self.check_oos(response)

    def parse_prev_price(self, response):
        prev_price = "".join(response.css(".at-wrongprice::text").extract())
        return ".".join(re.findall(r'\d+', prev_price))

    def parse_price(self, response):
        price = "".join(response.css(".at-lastprice::text").extract())
        return ".".join(re.findall(r'\d+', price))

    def parse_brand(self, response):
        brand = response.css(".brand > a::text").extract() or response.css(".brand::text").extract()
        return brand[0].strip()

    def parse_care(self, response):
        care = response.css(".articlecare > dd > div > template > b::text").extract()
        return care[0].strip() if care else ""

    def parse_description(self, response):
        descriptions = []
        for line in response.css(".at-dv-itemDetails > *::text").extract():
            if line.strip():
                descriptions.append(line.strip())
        return descriptions

    def parse_name(self, response):
        return response.css(".at-dv-itemName::text").extract()[0].strip()

    def parse_product_id(self, response):
        return re.findall("_([0-9A-Za-z]+)", response.url)[0]

    def parse_size(self, response):
        return response.css(".active::text").extract()[-1].replace('– ', '')

    def parse_color(self, response):
        return response.css(".at-dv-color::text").extract()[0].replace('— ', '')

    def parse_category(self, response):
        return response.css("meta[name*='z_breadcrumb']::attr(content)").extract()[0].split(">")[:-1]

    def parse_image_urls(self, response):
        return response.css(".imageThumb::attr(data-zoom-image)").extract()

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
        Rule(LinkExtractor(allow="sheego.de/", deny=["sheego.de/\?","\?", "html"], restrict_css="#content"),
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
        request.meta['size_codes'] = response.meta['size_codes']
        request.meta['item'] = response.meta['item']
        request.meta['anid'] = response.meta['anid']
        return request

    def parse_variants(self, response):
        variants = response.meta['variants']
        variant = variants.pop(0) if variants else ""
        size_codes = {}
        size_variants = product(self.parse_size_codes(response), [variant])
        size_codes.update(dict(zip(self.parse_sizes(response), size_variants)))
        size_codes.update(response.meta['size_codes'])
        response.meta['size_codes'] = size_codes
        if variants:
            url = "https://www.sheego.de/index.php?cl=oxwarticledetails&anid={}&varselid%5B1%5D={}"
            request = Request(url.format(response.meta['anid'][0], variants[0]), self.parse_variants)
            request.meta['variants'] = variants
            request.meta['item'] = response.meta['item']
            request.meta['anid'] = response.meta['anid']
            request.meta['size_codes'] = response.meta['size_codes']
            return request
        else:
            return self.check_oos(response)

    def parse_anid(self, response):
        anids = []
        for url in self.parse_color_urls(response):
            anids.append(re.split("_([A-Za-z0-9-]*)", url)[1])
        return anids

    def parse_color_urls(self, response):
        selected = response.css(".color-item[class*='active']::attr(href)").extract()
        not_selected = response.css(".color-item:not([class*='active'])::attr(href)").extract()
        return selected + not_selected

    def get_variants(self, response):
        selected = response.css(".js-variantSelector > option[selected]::attr(value)").extract()
        not_selected = response.css(".js-variantSelector > option:not([selected])::attr(value)").extract()
        return selected + not_selected

    def parse_oos(self, response):
        item = response.meta['item']
        root = fromstring(response.body)
        urls = []
        stock_keys = []
        sizes = []
        skus = {}
        for article in root.findall('.//Article'):
            size = article.find(".//SizeAlphaText").text
            stock = article.find(".//Stock").text
            catalog_id = article.find(".//CompleteCatalogItemNo").text
            stock_key = "{}_{}".format(catalog_id, size)
            if stock is '1':
                sizes.append(size)
                url = self.parse_sku_url(response, sizes, catalog_id)
                urls.append(url)
                stock_keys.append(stock_key)
            else:
                skus[stock_key] = {}
                skus[stock_key]['oos'] = True
        if urls:
            request = Request(urls.pop(), callback=self.parse_sku)
            request.meta['skus'] = skus
            request.meta['item'] = item
            request.meta['stock_keys'] = stock_keys
            request.meta['urls'] = urls
            return request
        else:
            item['skus']['oos'] = True
            return item

    def parse_sku_url(self, response, sizes, catalog_id):
        size_codes = response.meta['size_codes']
        anids = response.meta['anid']
        url = "https://www.sheego.de/index.php?cl=oxwarticledetails&" \
              "anid={}&artNr={}&varselid%5B0%5D={}&varselid%5B1%5D={}"
        current_size = size_codes[sizes[-1]]
        anid = sizes.count(sizes[-1]) - 1
        varsel_id0 = ""
        varsel_id1 = ""
        if len(current_size) is 2:
            varsel_id0, varsel_id1 = current_size
        else:
            varsel_id0 = current_size
        return url.format(anids[anid], catalog_id, varsel_id0, varsel_id1)

    def parse_sku(self, response):
        item = response.meta['item']
        urls = response.meta['urls']
        sku_keys = response.meta['stock_keys']
        sku_key = sku_keys.pop()
        sku = {}
        sku['color'] = self.parse_color(response)
        sku['price'] = self.parse_price(response)
        sku['previous_prices'] = self.parse_prev_price(response)
        sku['size'] = self.parse_size(response)
        sku['image_urls'] = self.parse_image_urls(response)
        sku['currency'] = 'EUR'
        item['skus'][sku_key] = sku
        if urls:
            request = Request(urls.pop(), callback=self.parse_sku)
            request.meta['item'] = item
            request.meta['stock_keys'] = sku_keys
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
        response.meta['anid'] = self.parse_anid(response)
        response.meta['item'] = item
        response.meta['size_codes'] = {}
        response.meta['variants'] = self.get_variants(response)
        return self.parse_variants(response)

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

    def parse_size_codes(self, response):
        return response.css(".js-sizeSelector > div > button::attr(data-selection-id)").extract()

    def parse_size(self, response):
        data_id = re.findall("=([0-9A-Za-z]+)", response.url)[2]
        return response.css(".at-dv-size::text".format(data_id)).extract()[-1].replace('– ', '')

    def parse_sizes(self, response):
        return response.css(".js-sizeSelector > div > button::attr(data-noa-size)").extract()

    def parse_color(self, response):
        color_id = re.findall("=([0-9A-Za-z-]+)", response.url)[-1]
        color = response.css(".js-variantSelector.color > .title > span::text".format(color_id))
        return color.extract()[0].replace('— ', '')

    def parse_category(self, response):
        return response.css("meta[name*='z_breadcrumb']::attr(content)").extract()[0].split(">")[:-1]

    def parse_image_urls(self, response):
        return response.css(".imageThumb::attr(data-zoom-image)").extract()

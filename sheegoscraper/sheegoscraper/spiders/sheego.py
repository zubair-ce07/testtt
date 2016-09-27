from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import SheegoItem
from xml.etree.ElementTree import Element, SubElement, fromstring, tostring
import re
from scrapy.http import Request


class SheegoSpider(CrawlSpider):
    name = "sheego"
    allowed_domains = ["sheego.de"]
    start_urls = ['https://www.sheego.de/']
    rules = [
        Rule(LinkExtractor(allow="sheego.de/", deny=["sheego.de/\?", "\?", "html"], restrict_css="#content"),
             follow=True),
        Rule(LinkExtractor(restrict_css=".cj-active"), callback='parse_product', follow=True),
        Rule(LinkExtractor(allow="sheego.de/", deny=["sheego.de/\?", "\.html"],
                           restrict_css=".next.js-next.btn.btn-next"))
    ]

    def articles(self, response):
        articles = response.css("script:contains('articlesString')::text").extract()[0]
        articles_filtered = re.findall("([0-9A-Z]{3,8})\;([0-9A-Za-z]{,4})", articles)
        articles_filtered = [(key, '0') if not size else (key, size) for key, size in articles_filtered]
        return articles_filtered

    def create_xml(self, response):
        root = Element('tns:KALAvailabilityRequest',
                       attrib={'xmlns:tns': "http://www.schwab.de/KAL",
                                'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                                'xsi:schemaLocation': "http://www.schwab.de/KAL "
                                "http://www.schwab.de/KAL/KALAvailabilityRequestSchema.xsd"
                               })
        articles = SubElement(root, 'Articles')
        for article_id, size in self.articles(response):
            article = SubElement(articles, 'Article')
            SubElement(article, "CompleteCatalogItemNo").text = article_id
            SubElement(article, "SizeAlphaText").text = size
            SubElement(article, "Std_Promotion").text = article_id[6:]
            SubElement(article, "CustomerCompanyID").text = '0'
        return tostring(root).decode("utf-8")

    def request_kal(self, response):
        request = Request(url='https://www.sheego.de/request/kal.php',
                          method='POST',
                          headers={'Content-Type': 'application/xml'},
                          callback=self.parse_kal,
                          body=self.create_xml(response))
        request.meta['item'] = response.meta['item']
        return request

    def base_url(self, response):
        item = response.meta['item']
        return item['url_original'].split("_")[0] + "_" + item['product_id'] + "-{}-{}-{}.html"

    def parse_kal(self, response):
        item = response.meta['item']
        root = fromstring(response.body)
        urls = []
        skus = {}
        base_url = self.base_url(response)
        for article in root.findall('.//Article'):
            size = article.find(".//SizeAlphaText").text
            stock = article.find(".//Stock").text
            catalog_id = article.find(".//CompleteCatalogItemNo").text
            sku_key = "{}_{}".format(catalog_id, size)
            if stock is '1':
                url = base_url.format(catalog_id[:6], size, catalog_id[6:])
                urls.append({"url": url, "sku_key": sku_key})
            else:
                skus[sku_key] = {'oos': True}
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
        sku = dict()
        sku['color'] = self.color(response)
        sku['price'] = self.price(response)
        sku['previous_prices'] = self.prev_price(response)
        sku['size'] = self.size(response)
        sku['image_urls'] = self.image_urls(response)
        sku['currency'] = 'EUR'
        item['skus'][sku_key] = sku
        if urls:
            request = Request(urls[0]['url'], callback=self.parse_sku)
            request.meta['item'] = item
            request.meta['urls'] = urls
            return request
        else:
            return item

    def parse_product(self, response):
        item = SheegoItem()
        item['gender'] = 'Women'
        item['category'] = self.category(response)
        item['url_original'] = response.url
        item['product_id'] = self.product_id(response)
        item['name'] = self.product_name(response)
        item['brand'] = self.brand(response)
        item['care'] = self.care(response)
        item['description'] = self.description(response)
        item['skus'] = {}
        response.meta['item'] = item
        return self.request_kal(response)

    def prev_price(self, response):
        prev_price = "".join(response.css(".at-wrongprice::text").extract())
        return ".".join(re.findall(r'\d+', prev_price))

    def price(self, response):
        price = "".join(response.css(".at-lastprice::text").extract())
        return ".".join(re.findall(r'\d+', price))

    def brand(self, response):
        brand = response.css(".brand > a::text").extract() or response.css(".brand::text").extract()
        return brand[0].strip()

    def care(self, response):
        return [s for s in self.description(response) if "%" in s]

    def description(self, response):
        descriptions = []
        for line in response.css(".at-dv-itemDetails > [itemprop='description'] *::text").extract():
            line_stripped = line.strip()
            if line_stripped:
                descriptions.append(line_stripped)
        return descriptions

    def product_name(self, response):
        return response.css(".at-dv-itemName::text").extract()[0].strip()

    def product_id(self, response):
        return re.findall("_([0-9A-Za-z]+)", response.url)[0]

    def size(self, response):
        size = response.css(".active::text").extract()[-1].replace('– ', '').strip()
        return size if size else "one_size"

    def color(self, response):
        return response.css(".at-dv-color::text").extract()[0].replace('— ', '')

    def category(self, response):
        return response.css("meta[name*='z_breadcrumb']::attr(content)").extract()[0].split(">")[:-1]

    def image_urls(self, response):
        return response.css(".imageThumb::attr(data-zoom-image)").extract()

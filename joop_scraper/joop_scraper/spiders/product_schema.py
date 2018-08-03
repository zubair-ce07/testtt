import scrapy
from urllib.parse import urlparse


class Parser(scrapy.Spider):
    name = "Parser"

    def parse(self, response):
        name = response.css('h2[itemprop="name"]::text').extract_first()
        colour = name.split()[-1]
        price = response.css('meta[itemprop="price"]::attr(content)').extract_first()
        currency = response.css('meta[itemprop="currency"]::attr(content)').extract_first()

        def get_skus(options):
            skus = {}
            for option in options:
                sku = {
                    "price":              100*float(price.replace(',', '.')),
                    "currency":           currency,
                    "size":               option.css('::text').extract_first().split()[0],
                    "colour":             colour,
                }
                if "unavailable" in option.css("::attr(class)").extract_first().split():
                    sku["out_of_stock"] = True
                previous_price = option.css("::attr(data-listprice)").extract_first()
                if previous_price:
                    sku["previous_prices"] = [100*float(previous_price[:-2].replace(",", "."))]
                skus[option.css("::attr(data-code)").extract_first()] = sku
            return skus
        url = urlparse(response.url)
        image_paths = response.css('li[data-mimetype="image/jpeg"]::attr(data-detail)').extract()
        breadcrumb = response.css('#breadcrumb a::text').extract()
        return {
           "retailer_sku":    response.css('span.js_addToCart::attr(data-code)').extract_first(),
           "lang":            "de",
           "uuid":            None,
           "trail":           [],
           "gender":          breadcrumb[0] if breadcrumb[0] != "living" else None,
           "category":        breadcrumb,
           "industry":        None,
           "brand":           "Joop",
           "url":             f'{url.scheme}://{url.netloc}{url.path}',
           "market":          "DE",
           "retailer":        "joop-de",
           "url_original":    response.url,
           "name":            name,
           "description":     response.css('div[itemprop=description]>div>p::text').extract_first().split(". "),
           "care":            response.css('div[itemprop=description]>div>span')[-2].css(' ::text').extract(),
           "image_urls":      [f'{url.scheme}://{url.netloc}{path}' for path in image_paths],
           "skus":            get_skus(response.css('option[data-code]')),
           "price":           100*float(price.replace(',', '.')),
           "currency":        currency
        }


complain_id = "01930755"

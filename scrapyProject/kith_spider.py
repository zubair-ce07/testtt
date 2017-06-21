from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class KithSpider(CrawlSpider):
    name = "kith"
    start_urls = ['https://kith.com/']
    allowed_domains = ['kith.com']
    DOWNLOAD_DELAY = 0.5
    css = ['ul.ksplash-header-upper-items', 'ul li.main-nav-list-item']
    rules = (
        Rule(LinkExtractor(restrict_css=css)),
        Rule(LinkExtractor(restrict_css='a.product-card-info'), callback="parse_products"),
    )

    def parse_products(self, response):
        garment = {}
        garment['description'] = self.get_description(response)
        garment['image-urls'] = self.get_image_urls(response)
        garment['name'] = self.get_name(response)
        garment['retailer_sku'] = self.get_retailer_sku(response)
        garment['skus'] = self.get_skus(response)
        garment['gender'] = self.get_gender(response)
        garment['url'] = self.get_url(response)
        return garment

    def get_image_urls(self, response):
        css = 'div.super-slider-thumbnails-slide-wrapper img::attr(src)'
        return response.css(css).extract()

    def get_name(self, response):
        css = 'h1.product-header-title span::text'
        return response.css(css).extract_first().strip()

    def get_retailer_sku(self, response):
        css = '#product_id::attr(value)'
        return response.css(css).extract_first()

    def get_url(self, response):
        return response.url

    def get_gender(self, response):
        product_name = self.get_name(response)
        if "Kidset" in product_name:
            return "unisex - kids"

        css = 'nav.breadcrumb a::attr(href)'
        product_header = response.css(css).extract_first().strip()
        if "women" in product_header:
            return "women"
        return "men"

    def get_description(self, response):
        css1 = '.product-single-details-dropdown div p::text'
        css2 = '.product-single-details-dropdown div ul li::text'
        description1 = response.css(css1).extract()
        description2 = response.css(css2).extract()
        description = description1 + description2
        description = [info.strip().replace('\xa0', '') for info in description if info != '\xa0']
        return description

    def get_skus(self, response):
        skus = {}
        sizes_css = '.product-single-form-wrapper form div select option::text'
        sizes = response.css(sizes_css).extract()

        products_id_css = '.product-single-form-wrapper form div select option::attr(value)'
        product_ids = response.css(products_id_css).extract()

        currency_css = 'div.product-single-header meta::attr(content)'
        currency = response.css(currency_css).extract_first()

        color_css = 'div.product-single-header div span::text'
        color = response.css(color_css).extract_first().strip()

        price_css = 'span.product-header-title -price::attr(content)'
        price = response.css(price_css).extract_first()

        details = {"colour": color, "currency": currency, "price": price}
        for product_id, size in zip(product_ids, sizes):
            skus[product_id] = {}
            skus[product_id] = details.copy()
            skus[product_id]["size"] = size.strip()
        return skus


import scrapy


class Skus:
    def __int__(self):
        self.sku_id = ""
        self.size = ""
        self.price = ""
        self.currency = ""
        self.previous_prices = []


class Garment:
    def __int__(self):
        self.price = ""
        self.name = ""
        self.lang = ""
        self.gender = ""
        self.currency = ""
        self.brand = ""
        self.image_urls = []
        self.category = []
        self.care = []
        self.skus = []
        self.trail = []
        self.retailer_sku = ""


class PuketSpider(scrapy.Spider):
    name = "puket"
    start_urls = [
        'http://www.puket.com.br/mulher/pijamas/pijamas-curtos/pijama-curto-manga-curta-multibichos-adulto_1707544?skuId=0306016043902',
    ]

    def parse(self, response):

        garment = Garment()
        garment.lang = response.css('html::attr(lang)').extract_first()
        garment.name = response.css('article.infoProduct > h1.nameProduct::text').extract_first()

        garment.category = response.css('div.product-breadcrumb > a::text').extract()[1:]
        garment.gender = garment.category[0]
        garment.trail = [response.css('div.product-breadcrumb > a::attr(href)').extract()[1]]
        garment.care = response.css('div.descProduct::text').extract()[1:]
        garment.image_urls = response.css('ul.list-thumbs > li > a::attr(href)').extract()

        garment.brand = response.css('h1.logo > a > img::attr(alt)').extract_first()
        garment.price = response.css('article.infoProduct > div.priceProduct > p.bestPrice > span.val::text').extract_first()
        garment.currency = response.css('article.infoProduct > div.priceProduct > span[itemprop="priceCurrency"]::attr(content)').extract_first()
        garment.retailer_sku = response.css('span#product-showcase-image::attr(data-product-id)').extract_first()

        skus = response.css('div.wrap-sku-selection > fieldset > div[data-dimension="Tamanho"] > ul > li').extract()
        for sku in skus:
            sku_ = Skus()
            sku_.sku_id = sku.css('input::attr(data-skurel)').extract_first()
            sku_.size = sku.css('input::attr(value)').extract_first()
            sku_.price = garment.price
            sku_.currency = garment.currency
            sku_.previous_prices = response.css('article.infoProduct > div.priceProduct > p.oldPrice > span.val::text').extract()
            garment.skus.append(sku_.__dict__)

        return garment.__dict__
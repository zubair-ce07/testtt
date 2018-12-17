from scrapy.spiders import Rule, Request
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean

class Mixin:
	retailer = 'fila'
	allowed_domains = ['fila.com.br']


class MixinBR(Mixin):
	default_brand = 'Fila'
	market = 'BR'
	retailer = Mixin.retailer + '-br'
	start_urls = [
		'https://www.fila.com.br/'
	]


class FilaParseSpider(BaseParseSpider, Mixin):
	description_css = care_css = '.wrap-description ::text, .wrap-long-description ::text'

	def parse(self, response):
		sku_id = self.product_id(response)
		garment = self.new_unique_garment(sku_id)

		if not garment:
			return

		self.boilerplate_normal(garment, response)
		garment['gender'] = self.product_gender(response)
		garment['image_urls'] = self.product_images(response)
		garment['skus'] = self.skus(response)

		garment['meta'] = {'requests_queue': self.colour_requests(response)}

		return self.next_request_or_garment(garment)

	def parse_colours(self, response):
		garment = response.meta['garment']
		garment['image_urls'].extend(self.product_images(response))
		garment['skus'].update(self.skus(response))
		return self.next_request_or_garment(garment)	

	def skus(self, response):
		size_css = '#configurable_swatch_size .swatch-label::text'
		skus = {}
		price, old_price = self.product_prices(response)
		colour = clean(response.css('.wrap-sku>small ::text'))[1]

		if not price:
			return skus
			
		common = self.product_pricing_common(response, money_strs=[price + old_price])
		common['colour'] = colour
		available_size = [size for size in clean(response.css(size_css))]

		for size in available_size:
			sku = common.copy()
			sku['size'] = size
			skus['{}_{}'.format(colour, size)] = sku
		
		return skus
	
	def product_images(self, response):
		return clean(response.css('a.thumb-link>img::attr(src)'))
	
	def product_gender(self, response):
		return self.gender_lookup(self.product_name(response)) 

	def product_prices(self, response):
		old_price = response.css('.pdv_original ::text').extract_first() or ''
		price = response.css('.normal_price_span ::text').extract_first()
		return price, old_price
		
	def product_category(self, response):
		return clean(response.css('.breadcrumbs a[href] ::text'))[1:]

	def product_id(self, response):
		return clean(response.css('.wrap-sku>small ::text'))[0].split('_')[0]

	def product_name(self, response):
		return clean(response.css('.product-name ::text'))[0]
	
	def colour_requests(self, response):
		css = '.wrap-other-desktop .carrossel-link::attr(href)'
		urls = clean(response.css(css))
		current_url = clean(response.css('.thumb-block.current a::attr(href)'))
		if current_url:
			urls.remove(current_url[0])
		return [Request(url, callback=self.parse_colours, dont_filter=True) \
					for url in urls]
	
	def next_request_or_garment(self, garment, drop_meta=True):
		if not (garment['meta'] and garment['skus']):
			garment['out_of_stock'] = True
		return super().next_request_or_garment(garment, drop_meta=drop_meta)


class FilaCrawlSpider(BaseCrawlSpider, Mixin):
	listings_css = ['a.level2', '[title="Próximo"]']
	products_css = '.product-image'

	rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )


class FilaBRParseSpider(FilaParseSpider, MixinBR):
	name = MixinBR.retailer + '-parse'
	custom_settings = {
		'DOWNLOAD_DELAY': 5,
	}


class FilaBRCrawlSpider(FilaCrawlSpider, MixinBR):
	name = MixinBR.retailer + '-crawl'
	parse_spider = FilaBRParseSpider()

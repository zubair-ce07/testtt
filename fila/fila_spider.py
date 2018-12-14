from scrapy.spiders import Rule, Request
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean

class Mixin:
	retailer = 'fila'
	allowed_domains = ['fila.com.br']
	one_sizes = ['U']


class MixinBR(Mixin):
	market = 'BR'
	lang = 'pt'
	retailer = Mixin.retailer + '-br'
	start_urls = [
		'https://www.fila.com.br/'
	]


class MixinAR(Mixin):
	market = "AR"
	lang = ''


class FilaParseSpider(BaseParseSpider, Mixin):

	def parse(self, response):
		care_css = '.wrap-description ::text'
		sku_id = self.product_id(response)

		garment = self.new_unique_garment(sku_id)

		if not garment:
			return

		self.boilerplate_normal(garment, response)
		garment['gender'] = self.gender_lookup(garment['name'])
		garment['image_urls'] = []
		garment['skus'] = {}

		garment['meta'] = {'requests_queue': self.colour_requests(response)}

		return self.next_request_or_garment(garment)
	
	def next_request_or_garment(self, garment, drop_meta=True):
		"""
			Assuming that ['meta']['requests_queue'] contains queue of prepared requests,
			to be processed from right to left
		"""
		if not 'meta' in garment:
			return garment

		if garment['meta']['requests_queue']:
			request = garment['meta']['requests_queue'].pop()
			request.meta.setdefault('garment', garment)
			return [self.elevate_request_priority(request)]

		garment['meta'].pop('requests_queue')

		if drop_meta or not garment['meta']:
			garment.pop('meta')

		if not garment['skus']:
			garment['out_of_stock'] = True

		return garment

	def colour_requests(self, response):
		css = '.wrap-other-desktop .carrossel-link::attr(href)'
		return [response.follow(url, callback=self.parse_colours, dont_filter=True) for  url in response.css(css).extract()]

	def parse_colours(self, response):
		garment = response.meta['garment']
		garment['image_urls'].extend(self.product_images(response))
		garment['skus'].update(self.skus(response))
		return self.next_request_or_garment(garment)	

	def product_images(self, response):
		return clean(response.css('a.thumb-link>img::attr(src)'))

	def skus(self, response):
		skus = {}
		price, old_price = self.product_prices(response)
		colour = self.product_colour(response)

		if not price:
			return skus
			
		common = self.product_pricing_common(response, money_strs=[price + old_price])
		common['colour'] = colour
		available_size = self.product_sizes(response)

		for size in available_size:
			sku = common.copy()
			sku['size'] = size
			skus['{}_{}'.format(colour, size)] = sku
		
		return skus
	
	def product_prices(self, response):
		old_price = response.css('.pdv_original ::text').extract_first()
		old_price = old_price if old_price else ''
		price = response.css('.normal_price_span ::text').extract_first()
		return price, old_price
	
	def product_sizes(self, response):
		css = '#configurable_swatch_size .swatch-label::text'
		return [self.one_size if size in self.one_sizes else size for size in response.css(css).extract()]
	
	def product_description(self, response):
		css = '.wrap-description ::text, .wrap-long-description ::text'
		return clean(response.css(css))

	def product_colour(self, response):
		return response.css('.wrap-sku>small ::text').extract()[1]
	
	def product_brand(self, response):
		return 'Fila'
		
	def product_category(self, response):
		return clean(response.css('.breadcrumbs a[href] ::text'))[1:]

	def product_id(self, response):
		return response.css('.wrap-sku>small ::text').extract_first().split('_')[0]

	def product_name(self, response):
		return clean(response.css('.product-name ::text'))[0]


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
		"DOWNLOAD_DELAY": 3,
	}


class FilaBRCrawlSpider(FilaCrawlSpider, MixinBR):
	name = MixinBR.retailer + '-crawl'
	custom_settings = {
		"HTTPCACHE_ENABLED": True,
	}
	parse_spider = FilaBRParseSpider()
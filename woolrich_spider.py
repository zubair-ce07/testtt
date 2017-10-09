from scrapy import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WoolRichSpider(CrawlSpider):

    name = 'woolrich'
    allowed_domains = ['woolrich.com']
    start_urls = ['http://www.woolrich.com/woolrich/details/women-s-literary-rex-eskimo-john-rich-bros/_/R-WW1058']
    skus_url = "http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp"
    navigation_css = ['.mobile-menu-list', '.nav-list nav-', '.addMore']
    product_css = '.hover_img'
    rules = (
        Rule(LinkExtractor(restrict_css=(navigation_css), tags=('a', 'div'), attrs=('href', 'nextpage')),),
        Rule(LinkExtractor(restrict_css=(product_css,)), callback='parse_product'),
    )

    def parse_product(self, response):
        garment = {}
        garment['skus'] = {}
        garment['requests'] = []
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['retailer_sku'] = self.product_retailer_sku(response)
        garment['currency'] = self.product_currency(response)
        garment['url'] = self.product_url(response)
        garment['original_url'] = self.product_original_url(response)
        garment['price'] = self.product_price(response)
        garment['category'] = self.product_categories(response)
        garment['care'] = self.product_care(response)
        garment['trail'] = self.product_trail(response)
        garment['image_urls'] = self.porduct_image_urls(response)
        colors = self.product_color_ids(response)
        if colors:
            return self.parse_color(response, garment, colors)
        else:
            return garment

    def parse_color(self, response, garment, colors):
        color_ids = colors
        color_names = self.product_color_names(response)
        selected_size = self.product_selected_size(response)
        if not selected_size:
            selected_size = ""
        for color_id, color_name in zip(color_ids, color_names):
            product_id = garment['retailer_sku']
            data = {
                'productId': product_id,
                'colorId': color_id,
                'colorDisplayName': color_name,
                'size': selected_size
            }
            garment['requests'].append(FormRequest(url=self.skus_url, formdata=data,
                                                   callback=self.parse_size,
                                                   meta={'garment': garment}))

        return garment['requests']

    def parse_size(self, response):
        self.remove_processed_request(response)
        color_id = self.product_selected_color_id(response)
        color_display_name = self.product_selected_color_name(response)
        sku_ids = self.product_sku_ids(response, selector="sizelist")
        dimensions = self.product_dimensions(response)
        if dimensions:
            for size in sku_ids:
                data = {
                    'productId': response.meta['garment']['retailer_sku'],
                    'colorId': color_id,
                    'colorDisplayName': color_display_name,
                    'skuId': "",
                    'selectedSize': size
                }
                response.meta['garment']['requests'].append(FormRequest(url=self.skus_url, formdata=data,
                                                                        callback=self.parse_fit,
                                                                        meta={'garment': response.meta['garment']}))
        else:
            for sku_id in sku_ids:
                selected_size = self.product_selected_size(response, sku_id)
                data = {
                    'productId': response.meta['garment']['retailer_sku'],
                    'colorId': color_id,
                    'colorDisplayName': color_display_name,
                    'skuId': sku_id,
                    'selectedSize': selected_size
                }
                response.meta['garment']['requests'].append(FormRequest(url=self.skus_url, formdata=data,
                                                                        callback=self.parse_skus,
                                                                        meta={'garment': response.meta['garment']}))

        return response.meta['garment']['requests']

    def parse_fit(self, response):
        self.remove_processed_request(response)
        sku_ids = self.product_sku_ids(response, selector="dimensionslist")
        dimensions = self.product_stocked_dimensions(response)
        color_id = self.product_color_id(response)
        selected_size = self.product_selected_size(response)
        for sku_id, selected_dimension in zip(sku_ids, dimensions):
            data = {
                'productId': response.meta['garment']['retailer_sku'],
                'colorId': color_id,
                'skuId': sku_id,
                'selectedSize': selected_size,
                'selectedDimension': selected_dimension
            }
            response.meta['garment']['requests'].append(FormRequest(url=self.skus_url, formdata=data,
                                                                    callback=self.parse_skus,
                                                                    meta={'garment': response.meta['garment']}))
        return response.meta['garment']['requests']

    def parse_skus(self, response):
        self.remove_processed_request(response)
        size = ""
        dimension = ""
        currency = self.sku_currency(response)
        price = self.sku_price(response)
        color = self.sku_color(response)
        sku_id = self.sku_id(response, selector="dimensionslist")
        if sku_id:
            size = self.sku_size(response)
            dimension = self.sku_dimension(response)
        else:
            sku_id = self.sku_id(response, selector="sizelist")
        if size and dimension:
            size = size + "/" + dimension.strip()
        response.meta['garment']['skus'][sku_id] = {
            "currency": currency,
            "price": price,
            "color": color,
            "size": size
        }
        if not response.meta['garment']['requests']:
            del response.meta['garment']['requests']
            return response.meta['garment']

    def product_urls(self, response):
        return response.css(".hover_img > a::attr(href)").extract()

    def product_scroll_url(self, response):
        return response.css(".addMore::attr(nextpage)").extract_first()

    def product_name(self, response):
        return response.css('.pdp_title [itemprop="name"]::text').extract_first().strip()

    def product_description(self, response):
        description_css = 'span[itemprop="description"]::text, span[itemprop="description"] li::text'
        return response.css(description_css).extract()

    def product_retailer_sku(self, response):
        return response.css('.pdp::attr(productid)').extract_first()

    def product_url(self, response):
        return response.css('link[rel="canonical"]::attr(href)').extract_first()

    def product_original_url(self, response):
        return response.url

    def product_care(self, response):
        return response.css('label[for="feature"] + div li::text').extract()

    def product_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::text').extract_first()

    def product_categories(self, response):
        return response.css('#breadcrumbs a::text').extract()[1:]

    def product_price(self, response):
        price = response.css('.price [itemprop="price"]::attr(content)').extract_first()
        if not price:
            low_price = response.css('.price [itemprop="lowPrice"]::attr(content)').extract_first()
            high_price = response.css('.price [itemprop="highPrice"]::attr(content)').extract_first()
            price = low_price + " - " + high_price
        return price

    def product_trail(self, response):
        trail_urls = response.css('#breadcrumbs a::attr(href)').extract()
        trail = [response.urljoin(trail_url) for trail_url in trail_urls]
        return trail

    def porduct_image_urls(self, response):
        image_urls = response.css('#prod-detail__slider-nav img::attr(src)').extract()
        urls = [response.urljoin(image_url) for image_url in image_urls]
        if urls:
            return urls
        else:
            return [response.urljoin(response.css('#largeImg::attr(src)').extract_first())]

    def product_color_id(self, response):
        return response.css(".colorlist a[class~='selected'] img::attr(colorid)").extract_first()

    def product_color_ids(self, response):
        return response.css(".colorlist a:not([class~='disabled']) img::attr(colorid)").extract()

    def product_color_names(self, response):
        return response.css(".colorlist a:not([class~='disabled'])::attr(title)").extract()

    def product_selected_size(self, response, sku_id=None):
        if sku_id:
            return response.css('#' + sku_id + '::attr(title)').extract_first()
        else:
            return response.css('.sizelist a[class~="selected"]::attr(title)').extract_first()

    def product_selected_color_id(self, response):
        return response.css(".colorlist a[class~='selected'] img::attr(colorid)").extract_first()

    def product_selected_color_name(self, response):
        return response.css(".colorlist a[class~='selected']::attr(title)").extract_first()

    def product_sku_ids(self, response, selector):
        return response.xpath('//ul[@class="' + selector + '"]/li/a[@stocklevel>0]/@id').extract()

    def product_dimensions(self, response):
        return response.css(".dimensionslist a").extract()

    def product_stocked_dimensions(self, response):
        return response.xpath('//ul[@class="dimensionslist"]/li/a[@stocklevel>0]/@title').extract()

    def sku_id(self, response, selector):
        return response.css('.' + selector + ' a[class~="selected"]::attr(id)').extract_first()

    def sku_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()

    def sku_price(self, response):
        return response.css('[itemprop="price"]::attr(content)').extract_first()

    def sku_color(self, response):
        return response.css('.colorName::text').extract_first().strip()

    def sku_size(self, response):
        return response.css('.sizelist a[class~="selected"]::attr(title)').extract_first()

    def sku_dimension(self, response):
        return response.css('.dimensionslist a[class~="selected"]::text').extract_first().strip()

    def remove_processed_request(self, response):
        response.meta['garment']['requests'].remove(response.request)

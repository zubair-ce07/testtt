
import re
import json

from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.http import HtmlResponse

from crawler_tasks.items import GenericProduct


class LanebryantSpider(Spider):
    name = 'lanebryant'
    allowed_domains = ['lanebryant.com', 'lanebryant.scene7.com']
    start_urls = ['http://www.lanebryant.com/']

    base_url = 'http://www.lanebryant.com'
    product_skus_url = 'http://www.lanebryant.com/lanebryant/baseAjaxServlet?pageId=PDP_getProductSKU'
    pagination_url_t = 'http://www.lanebryant.com/lanebryant/plp/includes/plp-filters.jsp?N={}&No={}'
    product_imgs_url_t = 'http://lanebryant.scene7.com/is/image/lanebryantProdATG/{}?req=set,json'
    product_category_url_t = 'http://www.lanebryant.com/lanebryant/baseAjaxServlet?pageId=UserState'\
                             '&Action=Header.userState&userState_id=pId%3D{}&fetchFavorites=false'

    def parse(self, response):
        links = LinkExtractor(allow=('\/P-(\d+)$',)).extract_links(response)
        for link in links:
            page_id = re.search('P-(\d+)', link.url).group(1)
            page_url = self.pagination_url_t.format(page_id, 0)
            yield Request(page_url, callback=self.parse_product_list)

    def parse_product_list(self, response):
        json_response = json.loads(response.text)
        products_html = HtmlResponse(url='', body=json_response['product_grid']['html_content']
                                     .encode('ascii', 'ignore'))

        product_links = products_html.css('.mar-prd-item-image-container::attr(href)').extract()
        for link in product_links:
            yield Request(url='{}{}'.format(self.base_url, link), callback=self.parse_product)

        next_page_url = json_response.get('nextPageUrl')
        if not next_page_url:
            return

        match = re.search('N=(\d+)&No=(\d+)', next_page_url)
        next_url = self.pagination_url_t.format(match.group(1), match.group(2))
        yield Request(next_url, callback=self.parse_product_list)

    def parse_product(self, response):
        desc1 = response.css('#tab1 p::text').extract()
        desc2 = response.css('#tab1 li::text').extract()

        product = GenericProduct()
        product['brand'] = ''
        product['market'] = ''
        product['merch_info'] = ''
        product['gender'] = 'Women'
        product['url'] = response.url
        product['description'] = desc1 + desc2
        product['care'] = response.css('#tab2::text').extract()

        formdata = {
            'id': re.search('prd-(\d+)', response.url).group(1),
            'Action': 'PDP.getProduct'
        }
        yield FormRequest(
            self.product_skus_url, formdata=formdata,
            callback=self.parse_product_skus, meta={'product': product}
        )

    def parse_product_skus(self, response):
        product_detail = json.loads(response.text)['product'][0]
        colors_map = {}
        for color in product_detail['all_available_colors'][0]['values']:
            colors_map[color['id']] = color['name']

        sizes_map = {}
        for size in product_detail['all_available_sizes'][0]['values']:
            sizes_map[size['id']] = size['value']

        skus = {}
        for item in product_detail['skus']:
            match = re.search('^(\w+|\W) ?(.*)', item['prices']['list_price'])
            currency, price = match.group(1), match.group(2)
            skus[item['sku_id']] = {
                'currency': currency,
                'price': price,
                'size': sizes_map[item['size']],
                'colour': colors_map[item['color']]
            }

        product = response.meta['product']
        product['skus'] = skus
        product['product_id'] = product_detail['product_id']
        product['name'] = product_detail['product_name']

        img_server_url = 'http:{}'.format(product_detail['scene7_params']['server_url'])
        imageset = product_detail['default_imageset']
        meta = {
            'product': product,
            'other': {
                'img_server_url': img_server_url
            }
        }
        yield Request(self.product_imgs_url_t.format(imageset),
                      callback=self.parse_product_img_urls, meta=meta)

    def parse_product_img_urls(self, response):
        img_server_url = response.meta['other']['img_server_url']
        product = response.meta['product']
        raw_images = re.search('{.*}', response.text).group()
        img_items = json.loads(raw_images)['set']['item']

        image_urls = []
        if isinstance(img_items, dict):
            image_urls.append(img_server_url + img_items['i']['n'])
        elif isinstance(img_items, list):
            for item in img_items:
                image_urls.append(img_server_url + item['i']['n'])

        product['image_urls'] = image_urls
        url = self.product_category_url_t.format(product['product_id'])
        yield Request(url, callback=self.parse_product_category, meta={'product': product})

    def parse_product_category(self, response):
        product = response.meta['product']
        breadcrumb = json.loads(response.text)['breadCrumbData']
        product['category'] = [item['displayName'] for item in breadcrumb]
        return product

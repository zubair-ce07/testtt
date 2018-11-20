import scrapy
import json

from scrapy import Request
from ScrapyPractice.items import ProductItem, SizeItem, VariationItem


class AvenueSpider(scrapy.Spider):
    name = 'avenuespider'

    start_url = "https://www.avenue.com/on/demandware.store/Sites-Avenue-Site"

    Uagent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    cookies = "__cfduid=d5ed7c37f34b620105a43ad1ab8a538de1540360911; " \
              "dwac_dgFpYiaagBlLaaaad6bReBc4NC=l7Bg2GugWDt8dWwng-Pn9uzQKJxqD7q8Yss%3D|dw-only|||USD|false|US" \
              "%2FCentral|true; cqcid=ab3dsD5JyEfaem6DyCsL6iR5CY; entrySiteID=avenue; " \
              "sid=l7Bg2GugWDt8dWwng-Pn9uzQKJxqD7q8Yss; " \
              "dwanonymous_3d7746b169a3b5c0b3754df18c19f3e2=ab3dsD5JyEfaem6DyCsL6iR5CY; " \
              "dwsecuretoken_3d7746b169a3b5c0b3754df18c19f3e2=Z4hpS0oPGlVcQoengsCbQ8YhmmTN-afR2g==; __cq_dnt=0; " \
              "dw_dnt=0; dwsid=GEkoEm68mp4Ln-khirz0qWMpYFZvE3gZFSFAF4C9vjDQGYdBOAgNzPcNRekqtDJjcvebf2H2dLQ2HkxWOPlqhg" \
              "==; dw=1; __atuvc=1%7C43; __atuvs=5bd00ad5f5fb1ac0000; utag_vnum=1542952918890&vn=1; " \
              "utag_invisit=true; product_finding_method=browse; product_finding_method_sub=other; wlcme=true; " \
              "__cq_uuid=51df9f20-d752-11e8-9fd8-f9454f2decf6; _ga=GA1.2.1992505425.1540360920; " \
              "_gid=GA1.2.772161696.1540360920; _gat=1; sr_pik_session_id=cee9c4b9-273e-6251-270d-ae134b7e31dd; " \
              "sr_browser_id=aa99352f-4dd8-4f9b-91d8-fb0be3b23b50; s_vi=[CS]v1|2DE8056B85312A61-400001088000C021[CE]; " \
              "_caid=a6a17d7f-28b4-41a0-bed8-1ef7bf261909; _cavisit=166a4aa5c81|; " \
              "__utma=49071904.1992505425.1540360920.1540360921.1540360921.1; __utmc=49071904; " \
              "__utmz=49071904.1540360921.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; " \
              "__utmb=49071904.1.10.1540360921; xyz_cr_436_et_100=; consumerId=56ba38b9-e224-4cd2-9478-80033afe6517; " \
              "_svsid=3f74fec516892194d550d9d1473efde2; rmarlgd=1; " \
              "bounceClientVisit3056v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0AhgG4CmAdgK41kDGA9gLZEgA0IATjBAgAvkA; " \
              "_px3=b45362a94a680d0427856bee7a4155a52285b58d531a7d4c28c887ebe5c368e2:nhlUnEDvbRNwIHYI3T6" \
              "/VHw5DB6YWAxHPKNFCvzonJkfFE2hcWbz19Zavz3jAMPhaIVpJo5L7NNV2caVHp7UxQ==:1000" \
              ":02ZkYVP9icIYmQzJakrZJiuwGEh7jw3Lx5p7Ud4Qux2Zk1DCn01jCY0WgQU" \
              "+5mKvBe9SAqz6ax1QqMAwxTq8h4K9EiOaVKrYbf1vd5QvB8724qL9IEhEF5HiZm308AH5" \
              "/NLwmjGco8F35ZZcVks9XY1MLkWz3DXgaLImZLEGJzA=; " \
              "__idcontext=eyJkZXZpY2VJRCI6IjE5cDBjQlVPdUJWVnBwZ1FyanA5Vm12WjdPZyIsImNvb2tpZUlEIjoiMUMwZVE4UUZaR29jQnowN0pjd1JoSFpYbXFTIn0%3D; uuid=3c4f1ca4fff34210b494823222dbcad6; utag_dslv_s=Less than 1 day; utag_dslv=1540360950140; utag_main=v_id:0166a4aa576500207999c3795870030690017061009dc$_sn:1$_ss:1$_pn:1%3Bexp-session$_st:1540362718885$ses_id:1540360918885%3Bexp-session$_prevpage:undefined%3Bexp-1540364550142; s_pers=%20productnum%3D1%7C1542952919195%3B%20s_fid%3D76DE4DE6632A62ED-1D0C69122426C68E%7C1603519350144%3B%20s_nr%3D1540360950146-New%7C1542952950146%3B%20s_vs%3D1%7C1540362750148%3B; s_sess=%20s_cc%3Dtrue%3B%20s_cpc%3D1%3B%20s_stv%3Dnon-search%3B%20s_sq%3D%3B; FiftyOne_Akamai=GB|GBP|0.9397225000|2 "
    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": Uagent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.avenue.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookies,
    }

    listings_xpath = "//div[@class='menu-wrapper']//li[@role='menuitem']/a/@href"
    product_xpath = "//div[contains(@class,'product-image')]/a/@href"
    nextpage_xpath = "//div[@data-loading-state='unloaded' and not(@data-page)]/@data-grid-url"
    product_info_xpath = "//script[contains(text(),'utag_data_ave')]/text()"
    breadcrumbs_xpath = "//ul[contains(@class,'breadcrumb')]/li//text()"
    descript_xpath = "//div[@id='tab1']//p/text() | //div[@id='tab1']//ul/li/text()"
    color_name_xpath = "//div[@class='attribute color']//ul/li/a/text()"
    color_image_xpath = "//div[@class='attribute color']//ul/li/a/@data-lgimg"
    size_xpath = "//div[@class='attribute size']//ul/li[@class != 'selected-value' and @class != " \
                 "'size-chart-link']/a/text() "

    def start_requests(self):
        yield Request(
            url=self.start_url,
            callback=self.parse,
            headers=self.headers
        )

    def parse(self, response):
        listings_urls = response.xpath(self.listings_xpath).extract()

        for url in listings_urls:
            yield Request(
                url=url,
                callback=self.parse_listings,
                meta={'dont_merge_cookies': True},
                headers=self.headers,
            )

    def parse_listings(self, response):
        nextpage_url = response.xpath(self.nextpage_xpath).extract_first(default=None)
        products_urls = response.xpath(self.product_xpath).extract()

        for url in products_urls:
            yield Request(
                url=url,
                callback=self.parse_product,
                meta={'dont_merge_cookies': True},
                headers=self.headers,
            )
        if nextpage_url:
            yield Request(
                url=nextpage_url,
                headers=self.headers,
                meta={'dont_merge_cookies': True},
                callback=self.parse_listings,
            )

    def parse_product(self, response):
        info_html = response.xpath(self.product_info_xpath).extract_first()[21:-2]
        breadcrumbs = response.xpath(self.breadcrumbs_xpath).extract()
        breadcrumbs = [b for b in breadcrumbs if b != ' ']

        description = response.xpath(self.descript_xpath).extract()
        product_info = json.loads(info_html)

        product_item = ProductItem(
            product_url=product_info['product_url'],
            store_keeping_unit=product_info['productID_ave'],
            title=product_info['products_ave'],
            brand='avenue',
            locale='en_' + product_info['current_country_code_ave'],
            currency=product_info['current_currency_code_ave'],
            variations=self.variation_info(response, product_info),
            breadcrumbs=breadcrumbs,
            description=description,
        )

        yield product_item

    def variation_info(self, response, product_info):
        color_names = response.xpath(self.color_name_xpath).extract()
        color_names = [color.strip() for color in color_names]
        color_image_urls = response.xpath(self.color_image_xpath).extract()
        color_image_urls.append('{"url":""}')

        variations = []
        for index, name in enumerate(color_names):
            color = VariationItem(
                display_color_name=name,
                images_urls=json.loads(color_image_urls[index])['url'],
                sizes=self.size_info(response, product_info),
            )
            variations.append(color)
        return variations

    def size_info(self, response, product_info):
        size_list = response.xpath(self.size_xpath).extract()
        size_list = [size.strip() for size in size_list]

        currency_rate = float(product_info['current_currency_rate_ave'])
        real_price = float(product_info['product_standard_price_ave']) * currency_rate
        discounted_price = float(product_info['product_sales_price_ave']) * currency_rate
        is_discounted = False if real_price == discounted_price else True

        sizes = []
        for size in size_list:
            size_item = SizeItem(
                size_name=size,
                is_available=True,
                price=real_price,
                is_discounted=is_discounted,
                discounted_price=discounted_price if is_discounted else '',
            )
            sizes.append(size_item)

        return sizes

import re
from inline_requests import inline_requests
from scrapinghub import ScrapinghubClient

from scrapy import Spider, Item, Field, Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst

from xml.dom import minidom


class GoodReadsAttributesItem(Item):
    born = Field()
    website = Field()
    twitter = Field()
    genre = Field()
    member = Field()
    url = Field()


class GoodReadsBooksItem(Item):
    title = Field()
    gr_url = Field()
    gr_bid = Field()
    avg_rating = Field()
    rating_count = Field()
    published = Field()
    editions_count = Field()
    gr_edition_url = Field()


class GoodReadsItem(Item):
    gr_aid = Field()
    gr_url = Field()
    name = Field()
    image_url = Field()
    avg_ratings = Field()
    ratings_count = Field()
    reviews = Field()
    distinct_works = Field()
    similar_authors = Field()
    attributes = Field()
    books = Field()


class GoodReadsItemLoader(ItemLoader):
    default_item_class = GoodReadsItem

    default_input_processor = Identity()
    default_output_processor = TakeFirst()
    similar_authors_out = Identity()
    books_out = Identity()


class GoodReadsAttributesItemLoader(ItemLoader):
    default_item_class = GoodReadsAttributesItem

    default_input_processor = Identity()
    default_output_processor = TakeFirst()
    genre_out = Identity()


class GoodReadsBooksItemLoader(ItemLoader):
    default_item_class = GoodReadsBooksItem

    default_input_processor = Identity()
    default_output_processor = TakeFirst()


class GoodReadsProducerSpider(Spider):
    name = '5145_goodreads_com_producer'

    # There are more than 500 sitemaps available.
    # Parsing only sitemaps with authors
    start_urls = [
        'https://www.goodreads.com/sitemap.162.xml.gz', 'https://www.goodreads.com/sitemap.109.xml.gz',
        'https://www.goodreads.com/sitemap.99.xml.gz', 'https://www.goodreads.com/sitemap.123.xml.gz',
        'https://www.goodreads.com/sitemap.93.xml.gz', 'https://www.goodreads.com/sitemap.163.xml.gz',
        'https://www.goodreads.com/sitemap.116.xml.gz', 'https://www.goodreads.com/sitemap.100.xml.gz',
        'https://www.goodreads.com/sitemap.96.xml.gz', 'https://www.goodreads.com/sitemap.164.xml.gz',
        'https://www.goodreads.com/sitemap.153.xml.gz', 'https://www.goodreads.com/sitemap.97.xml.gz',
        'https://www.goodreads.com/sitemap.95.xml.gz', 'https://www.goodreads.com/sitemap.147.xml.gz',
        'https://www.goodreads.com/sitemap.110.xml.gz', 'https://www.goodreads.com/sitemap.128.xml.gz',
        'https://www.goodreads.com/sitemap.107.xml.gz', 'https://www.goodreads.com/sitemap.92.xml.gz',
        'https://www.goodreads.com/sitemap.145.xml.gz', 'https://www.goodreads.com/sitemap.127.xml.gz',
        'https://www.goodreads.com/sitemap.86.xml.gz', 'https://www.goodreads.com/sitemap.84.xml.gz',
        'https://www.goodreads.com/sitemap.142.xml.gz', 'https://www.goodreads.com/sitemap.156.xml.gz',
        'https://www.goodreads.com/sitemap.130.xml.gz', 'https://www.goodreads.com/sitemap.152.xml.gz',
        'https://www.goodreads.com/sitemap.134.xml.gz', 'https://www.goodreads.com/sitemap.80.xml.gz',
        'https://www.goodreads.com/sitemap.143.xml.gz', 'https://www.goodreads.com/sitemap.78.xml.gz',
        'https://www.goodreads.com/sitemap.161.xml.gz', 'https://www.goodreads.com/sitemap.88.xml.gz',
        'https://www.goodreads.com/sitemap.154.xml.gz', 'https://www.goodreads.com/sitemap.119.xml.gz',
        'https://www.goodreads.com/sitemap.148.xml.gz', 'https://www.goodreads.com/sitemap.94.xml.gz',
        'https://www.goodreads.com/sitemap.125.xml.gz', 'https://www.goodreads.com/sitemap.129.xml.gz',
        'https://www.goodreads.com/sitemap.139.xml.gz', 'https://www.goodreads.com/sitemap.112.xml.gz',
        'https://www.goodreads.com/sitemap.81.xml.gz', 'https://www.goodreads.com/sitemap.121.xml.gz',
        'https://www.goodreads.com/sitemap.118.xml.gz', 'https://www.goodreads.com/sitemap.102.xml.gz',
        'https://www.goodreads.com/sitemap.136.xml.gz', 'https://www.goodreads.com/sitemap.140.xml.gz',
        'https://www.goodreads.com/sitemap.144.xml.gz', 'https://www.goodreads.com/sitemap.106.xml.gz',
        'https://www.goodreads.com/sitemap.160.xml.gz', 'https://www.goodreads.com/sitemap.137.xml.gz',
        'https://www.goodreads.com/sitemap.103.xml.gz', 'https://www.goodreads.com/sitemap.89.xml.gz',
        'https://www.goodreads.com/sitemap.77.xml.gz', 'https://www.goodreads.com/sitemap.117.xml.gz',
        'https://www.goodreads.com/sitemap.124.xml.gz', 'https://www.goodreads.com/sitemap.98.xml.gz',
        'https://www.goodreads.com/sitemap.87.xml.gz', 'https://www.goodreads.com/sitemap.104.xml.gz',
        'https://www.goodreads.com/sitemap.133.xml.gz', 'https://www.goodreads.com/sitemap.85.xml.gz',
        'https://www.goodreads.com/sitemap.111.xml.gz', 'https://www.goodreads.com/sitemap.157.xml.gz',
        'https://www.goodreads.com/sitemap.146.xml.gz', 'https://www.goodreads.com/sitemap.90.xml.gz',
        'https://www.goodreads.com/sitemap.82.xml.gz', 'https://www.goodreads.com/sitemap.149.xml.gz',
        'https://www.goodreads.com/sitemap.159.xml.gz', 'https://www.goodreads.com/sitemap.131.xml.gz',
        'https://www.goodreads.com/sitemap.108.xml.gz', 'https://www.goodreads.com/sitemap.122.xml.gz',
        'https://www.goodreads.com/sitemap.151.xml.gz', 'https://www.goodreads.com/sitemap.126.xml.gz',
        'https://www.goodreads.com/sitemap.132.xml.gz', 'https://www.goodreads.com/sitemap.158.xml.gz',
        'https://www.goodreads.com/sitemap.101.xml.gz', 'https://www.goodreads.com/sitemap.91.xml.gz',
        'https://www.goodreads.com/sitemap.141.xml.gz', 'https://www.goodreads.com/sitemap.138.xml.gz',
        'https://www.goodreads.com/sitemap.120.xml.gz', 'https://www.goodreads.com/sitemap.113.xml.gz',
        'https://www.goodreads.com/sitemap.115.xml.gz', 'https://www.goodreads.com/sitemap.83.xml.gz',
        'https://www.goodreads.com/sitemap.155.xml.gz', 'https://www.goodreads.com/sitemap.105.xml.gz',
        'https://www.goodreads.com/sitemap.114.xml.gz', 'https://www.goodreads.com/sitemap.150.xml.gz',
        'https://www.goodreads.com/sitemap.79.xml.gz', 'https://www.goodreads.com/sitemap.135.xml.gz'
    ]

    def parse(self, response):
        xml_urls = minidom.parseString(response.body)
        xml_urls_list = xml_urls.getElementsByTagName('url')
        for url_object in xml_urls_list:
            url = url_object.getElementsByTagName('loc')[0].firstChild.nodeValue
            if '/author/show' in url:
                yield {'url': url}



class GoodReadsAuthorsSpider(Spider):
    name = '5145_goodreads_com'

    start_urls = ['https://www.goodreads.com/author/on_goodreads']

    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        if not hasattr(self, 'job_id'):
            self.log('Input job with author urls missing. Collecting authors from '
                     'https://www.goodreads.com/author/on_goodreads')
            yield Request(self.start_urls[0])
        else:
            client = ScrapinghubClient(self.settings.get('SC_APIKEY'))
            self.job = client.get_job(self.job_id)
            if not hasattr(self, 'start_ind'):
                self.start_ind = 0
            if not hasattr(self, 'end_ind'):
                self.end_ind = 5000000
            for ind, item in enumerate(self.job.items.iter()):
                if int(self.start_ind) <= ind <= int(self.end_ind):
                    yield Request(item.get('url'), callback=self.parse_author,
                                  headers={'Referer': 'https://www.goodreads.com/author/on_goodreads'})

    def parse(self, response):
        if 'goodreads.com' in response.url:
            for url in response.xpath('//a[contains(@href,"/author/show/")]/@href').extract():
                yield response.follow(url, callback=self.parse_author)
            for next_page in response.xpath('//a[@rel="next"]/@href').extract():
                yield response.follow(next_page)

    @inline_requests
    def parse_author(self, response):
        il = GoodReadsItemLoader(selector=response)
        attr_il = GoodReadsAttributesItemLoader(selector=response)
        attr_il.add_xpath('born', '//div[contains(text(),"Born")]/following-sibling::text()',
                          lambda x: ''.join(x).strip())
        attr_il.add_xpath('website', '//div[contains(text(),"Website")]/following-sibling::div[@class="dataItem"]//@href')
        attr_il.add_xpath('twitter', '//div[contains(text(),"Twitter")]/following-sibling::div[@class="dataItem"]//@href')
        attr_il.add_xpath('genre', '//div[contains(text(),"Genre")]/following-sibling::div[@class="dataItem"][1]//@href',
                          lambda x: [f'https://www.goodreads.com{xx}' for xx in x])
        attr_il.add_xpath('member', '//div[contains(text(),"Member")]/following-sibling::div[@class="dataItem"][1]/text()')
        attr_il.add_xpath('url', '//div[contains(text(),"URL")]/following-sibling::div[1]/text()',
                          lambda x: ''.join(x).strip())
        attr_item = dict(attr_il.load_item())

        il.add_value('gr_url', response.url)
        il.add_value('gr_aid', response.url, re='/show/(\d+)')
        il.add_value('attributes', attr_item)
        il.add_xpath('name', '//span[@itemprop="name"]/text()')
        il.add_xpath('image_url', '//meta[@property="og:image"]/@content')
        il.add_xpath('avg_ratings', '//div[@class="hreview-aggregate"]//span[@class="average"]/text()')
        il.add_xpath('ratings_count', '//div[@class="hreview-aggregate"]//span[@itemprop="ratingCount"]/@content')
        il.add_xpath('reviews', '//div[@class="hreview-aggregate"]//span[@itemprop="reviewCount"]/@content')
        il.add_xpath('distinct_works', '//a[contains(text(),"distinct work")]/text()', re='\d+')

        if b'Similar authors' in response.body:
            similar_authors_url = response.url.replace('/show/', '/similar/')
            r = yield Request(similar_authors_url)
            similar_authors = self.get_similar_authors(r)
            il.add_value('similar_authors', similar_authors)
        else:
            il.add_value('similar_authors', [])

        if b'More books by' in response.body:
            books_url = response.url.replace('/show/', '/list/') + '?page=1&per_page=1500'
            r = yield Request(books_url)
            books = self.get_books(r)
        else:
            books = self.get_books(response)
        il.add_value('books', books)

        yield il.load_item()

    def get_similar_authors(self, response):
        similar_authors = []
        for author in response.xpath('//li[@class="listElement"]'):
            similar_authors.append({
                'gr_aid': author.xpath('.//a[@class="bookTitle"]/@href').re('/show/(\d+)')[0],
                'gr_url': 'https://www.goodreads.com{}'.format(author.xpath('.//a[@class="bookTitle"]/@href').extract()[0]),
                'author_name': author.xpath('.//a[@class="bookTitle"]/text()').extract()[0]
            })
        return similar_authors[1:]

    def get_books(self, response):
        books = []
        for book in response.xpath('//tr[@itemtype="http://schema.org/Book"]'):
            bil = GoodReadsBooksItemLoader(selector=book)
            bil.add_xpath('title', './/span[@itemprop="name"]/text()')
            bil.add_xpath('gr_url', './/a[@itemprop="url"]/@href',
                          lambda x: f"https://www.goodreads.com{x[0]}" if x else None)
            bil.add_xpath('gr_bid', './/a[@itemprop="url"]/@href',
                          re='/book/show/(\d+)')
            bil.add_xpath('avg_rating', './/span[@class="minirating"]/text()',
                          lambda x: ''.join(re.findall('(.*) avg rating', ''.join(x))).strip())
            bil.add_xpath('rating_count', './/span[@class="minirating"]/text()',
                          lambda x: ''.join(re.findall('— (.*) rating', ''.join(x))).replace(',', '').strip())
            bil.add_xpath('published', './/span[@class="minirating"]/following-sibling::text()',
                          re='\d{4}')
            bil.add_xpath('editions_count', './/span[@class="minirating"]/following-sibling::a/text()',
                          re='(\d+) editions')
            bil.add_xpath('gr_edition_url', './/span[@class="minirating"]/following-sibling::a/@href',
                          lambda x: f"https://www.goodreads.com{''.join(x)}" if x else None)
            b = dict(bil.load_item())
            books.append(b)
        return books
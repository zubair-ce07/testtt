import scrapy
from scrapy.http.request import Request
from gymboree.items import GymboreeItem


class GymboreeSpider(scrapy.Spider):
    name = "gymboreeSpider"
    allowed_domains = ["gymboree.com"]
    start_urls = [
        "http://www.gymboree.com/"
        #  "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse_detail(self, response):
        i=0
        crawled=[]
        for rec in response.xpath('.//*[@class="collection-pricing"]//a'):
            item = GymboreeItem()
            if(i<2):
                link=rec.xpath('./@href').extract()
                if(link[0] in crawled):
                    continue
                else:
                    crawled.append(link[0])

                    #item['title'] = rec.xpath('./text()').extract()

                    print '\n\n\n link is \n\n\n',link
                    i=i+1
                    yield Request(url=link[0], callback=self.parse_child,dont_filter=True)
            else:
                break


    def parse_get_detail(self, response):
        item = GymboreeItem()
        item['skus']={}
        arr={}

        crwaled=[]
        for rec in response.xpath('//data'):

            item['title']= rec.xpath('.//head/@name').extract()
            item['retailer_sk']= rec.xpath('.//head/@code').extract()
            list=rec.xpath('.//options/text()').extract()
            item['description']=list[0].split('#')

            color=rec.xpath('.//product/@title').extract()
            item['spy_name']=self.name
            link=rec.xpath('.//product/@readReviewsURL').extract()
            item['link']=link[0].replace('#readReviews','')
            image=response.meta["images"]
            real=rec.xpath('.//product/@image').extract()
            image.append(real[0])
            item['image_urls']=image
        skus={}
        for rec in response.xpath('//sku'):
            arr={}
            id=rec.xpath('./@id').extract()
            print id
            arr['size']=rec.xpath('./@title').extract()
            print arr['size']
            arr['color']=color
            arr['currency']='USD'
            r_price=rec.xpath('./@reg-price').extract()
            st=r_price[0].find('$')
            ts=r_price[0].find('<',st+1)
            arr['previous_price']=r_price[0][st:ts]
            print arr['previous_price']
            s_price=rec.xpath('./@sale-price').extract()
            sst=s_price[0].find('$')
            sts=s_price[0].find('<',sst+1)
            arr['price']=s_price[0][st:ts]
            skus[id[0]]=arr
            item['skus']=skus
        yield item








    def parse_child(self, response):
        link=''
        strt=''
        nxt=''
        image={}
        images=[]
        item = GymboreeItem()
        i=0

        crawled=[]
        for rec in response.xpath('//body'):


            link=rec.xpath('./@onload').extract()
            print '\n\n\n linkd is \n\n\n', link[0]
            strt=link[0].find('http://')
            nxt=link[0].find('http://',strt+1)
            end=link[0].find(')',nxt+1)
            print 'start',strt,'end',nxt, link[0][nxt:end-1]
            send_link=link[0][nxt:end-1]
            print send_link
            image['images']=rec.xpath('.//*[@id="product-image-section"]//a//img/@src').extract()
            i=i+1
            if(send_link in crawled):
                continue
            else:

                yield Request(url=send_link, callback=self.parse_get_detail, dont_filter=True,meta=image)


    def parse_side(self, response):
        i=0
        for rec in response.xpath('.//*[@id="left-menu"]//a[not(contains(@href,"#"))]'):

            link=rec.xpath('./@href').extract()
            return Request(url=link[0], callback=self.parse_detail, dont_filter=True)

            #return Request(url=item['link'][0], callback=self.parse_detail, dont_filter=True)


    def parse(self, response):
        # sel = Selector(response)
        for rec in response.xpath('//ul/li[1]/a[contains(@href,"department") and contains(@href,"ASSORTMENT")]'):
            #item = GymboreeItem()
            link=rec.xpath('./@href').extract()

            #print item['link']
            #yield item
            yield Request(url=link[0], callback=self.parse_side, dont_filter=True)


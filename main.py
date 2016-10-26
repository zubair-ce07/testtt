from c_spider import CSpider

def main():
    domain = "https://arbisoft.com/"
    spider = CSpider(domain)
    spider.crawl()

    print(spider.size)

if __name__=="__main__":
    main()

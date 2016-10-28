from p_spider import PSpider

def main():
    domain = "https://arbisoft.com/"
    spider = PSpider(domain)
    spider.start()

    print(spider.size)

if __name__=="__main__":
    main()

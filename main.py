from scrapy import cmdline


def main():
    cmdline.execute("scrapy crawl journelle -o products.json".split())


if __name__ == '__main__':
    main()

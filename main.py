from scrapy import cmdline


def main():
    cmdline.execute("scrapy crawl journelle".split())


if __name__ == '__main__':
    main()

from scrapy import cmdline


cmdline.execute("scrapy crawl ernstings_family -o data.json".split())
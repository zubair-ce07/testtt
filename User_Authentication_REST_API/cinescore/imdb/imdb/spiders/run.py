from scrapy import cmdline
cmdline.execute("scrapy crawl imdb -o movies.json".split())

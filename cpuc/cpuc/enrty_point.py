from scrapy.cmdline import execute

# execute(['scrapy', 'crawl', 'cpuc'])
execute(['scrapy', 'crawl', 'cpuc', '-o', 'cpuc.json'])
# execute(['scrapy', 'crawl', 'quotes'])
# execute(['scrapy', 'shell', 'https://www.sheego.de/'])
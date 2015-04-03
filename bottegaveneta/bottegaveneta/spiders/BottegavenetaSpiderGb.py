from bottegaveneta.spiders.BottegavenetaSpider import BottegavenetaSpider

class BottegavenetaSpiderGb(BottegavenetaSpider):
    name = "bottegavenetaSpiderGb"
    #allowed_domains = ["bottegaveneta.com"]
    start_urls = [
        "http://www.bottegaveneta.com/gb"
    ]


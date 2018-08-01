# -*- coding: utf-8 -*-

# Scrapy settings for scrapy3_sears project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy3_sears'

SPIDER_MODULES = ['scrapy3_sears.spiders']
NEWSPIDER_MODULE = 'scrapy3_sears.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
USER_AGENT_LIST = "/home/abdul/Documents/firstWeek/Tasks/Task1/the-lab/scrapy3_sears/scrapy3_sears/user_agents.txt"

RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408]
RETRY_ENABLED = True
RETRY_TIMES = 5

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)d
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapy3_sears.middlewares.Scrapy3SearsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'scrapy3_sears.middlewares.Scrapy3SearsDownloaderMiddleware': 543,
    #'captchaMiddleware.middleware.CaptchaMiddleware':500,
    #'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    #'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
    # 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    # 'zipru_scraper.middlewares.ThreatDefenceRedirectMiddleware': 400,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'scrapy3_sears.pipelines.Scrapy3SearsPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ROTATING_PROXY_LIST = [
    "199.47.225.57:8080",
    "159.203.176.16:8080",
    "207.246.116.162:8080"
]

cookie = {
"__CT_Data":"gpv=94&ckp=tld&dm=sears.com&apv_99_www04=94&cpv_99_www04=94",
"__gads":"ID=efbff47026e94939:T=1532603997:S=ALNI_MZ9_M1ggIfjEezxku1LZtnFBOxrrg",
"_ga":"xxx123",
"aam_tnt":"seg=3397584~1914623~4980649~3061246~4980656~3061289~2938850~3610337~4267563",
"aam_uuid":"0164d650f73d0019ad5873ef9ab20004c0038009009dc",
"ak_bmsc":"5129C29AD7D36350843D2F1F0A2EFD1048F7B2E7343A000022E95E5B174D6852~plr6lYHc+GLYm8+QqGcyP6XbTpuqLWjuFWI+G5uVPjeWNeEZGeS5yPeKZkmH2RLwgQZ9OHUVpa1wOKG0OT5pv0ZGB3MW+9Wc1NRQA3aKHPZdNHXgUbERGca+x8FwrJUh/xjS3qgcPXXJUNrwSXjYv/vfW16vyvLJIRfXMVijqhaklZgP4Am1RPaleHlOfUNA9bw7A95ObvCNwEyn8FgCSm2ifBJZDh05KRCwKdZ7R9ZcY=",
"AKA_A2":"A",
"bm_sv":"DBA70D73F0CF8E297A21BB57BA3D56D5~NSW+kcdqbVqlxKDkoCLeZFdKvTrygFFXAppumWa2lIQciW6LJF9ZDpjSKXw4T67INN0G1BMDz1q8Em42JiDneZLb+rADlSlpHuKBdVg2VkGQcphdbE9cw8cE9xz9q76xzIOxtNu67WDw7FM0A2BPouTAWP6JJX4PLoa8ZEvGg78=",
"check":"true",
"CRTOABE":"0",
"ctm":"{'pgv':4601954770243453|'vst':1327638880538253|'vstr':4563401770954496|'intr':1532948818355|'v':1|'lvst':48}",
"cto_lwid":"0846399a-5c98-4114-ab30-f49d77806c78",
"cust_info":{"customerinfo":{"userName":"","isAkamaiZipSniff":False,"isGuest":True,"isSYWR":False,"sywrNo":"","encryptedSywrNo":"","sywrPoints":0,"sywrAmount":0,"expiringPoints":0,"expiringPointsDate":None,"expiringPointsWarn":False,"spendingYear":0,"vipLevel":"","nextLevel":0,"maxStatus":"SVU","maxSavings":0,"sessionID":"5f32f5e6-79f4-42ec-ac8a-e7dee8b55253","globalID":"137518967877470051_40670_25450","memberID":"137518967877470051_40670_25450","associate":False,"pgtToken":"","displayName":"","partialLogin":False,"cartCount":0}},
"dt":"desktop",
"expo_us_llt":"ac14fcc8-e8b8-4a08-b6a8-57d417c3c16d",
"fsr.r":{"d":90,"i":"d048012-57026351-8341-8701-38cd2","e":1533292615224,"s":1},
"fsr.s":{"v1":-1,"v2":-2,"rid":"d048012-57026351-8341-8701-38cd2","sd":1,"lk":1,"r":"www.sears.com","st":"","c":"https://www.sears.com/tools-hand-tools-screwdrivers/b-1021298","pv":10,"lc":{"d1":{"v":10,"s":True}},"cd":1,"cp":{"usrSessionID":"5f32f5e6-79f4-42ec-ac8a-e7dee8b55253|wj5//Z+NlmNI2SFFeVvL5laMpiUUbcCP4cYweNQjRro=|G|137518967877470051_40670_25450|0|1197882459","shcMPSHC":"MP PIDs seen|MP & SHC PIDs seen"}},
"gbi_visitorId":"cjk3t09t8000124kqs4jg5x6j",
"IntnlShip":"US|USD",
"irp":"5f32f5e6-79f4-42ec-ac8a-e7dee8b55253|wj5//Z+NlmNI2SFFeVvL5laMpiUUbcCP4cYweNQjRro=|G|137518967877470051_40670_25450|0|1197882459",
"KI_FLAG":"false",
"mbox":"PC#a73d55a6fa9047b0b61ad56dc6c4ceb1.21_18#1596191524|session#6bbef0de9eef413d9d1fc6d09a0f5833#1532950165",
"OAX":"fdFuSltZrlsAAmy4",
"ot":"i1-prod-ch3-vX-",
"phfsid":"default",
"ra_id":"xxx1532603987271|G|0",
"RES_TRACKINGID":"53855671756555",
"s_pers":"s_vnum=1690283987899%26vn%3D9|1690283987899; s_fid=6941D67789B8518C-0E85A6BE72C8E3D3|1690714705838; s_invisit=true|1532950105840; s_depth=17|1532950105841; gpv_pn=Tools%20%3E%20Hand%20Tools%20%3E%20Screwdrivers|1532950105843; gev_lst=event80|1532950105843; gpv_sc=Tools|1532950105844; gpv_pt=Subcategory|1532950105845;",
"s_sess":"s_sq=; s_e30=Anonymous; s_e26=MP%20PIDs%20seen%7CMP%20%26%20SHC%20PIDs%20seen; s_cc=true;",
"s_sso":"s_r|Y|",
"s_vi":"[CS]v1|2DACD72A85317DA1-6000010DE0000FD4[CE]",
"sn.chatAppID":"chatAppID||pcfForCustomersIntent",
"sn.isOfficeTime":"isOfficeTime||false",
"sn.tpc":"1",
"sn.vi":"9deeb250-a028-4c88-81fa-7a349d715d6d",
"utag_main":"v_id:0164d650f73d0019ad5873ef9ab20004c0038009009dc$_sn:10$_ss:0$_st:1532950108118$_metrics:undefined$dc_visit:10$segGroup:3$ses_id:1532941279547;exp-session$_pn:17;exp-session$_tntCampaign:undefined;exp-session$dc_event:18;exp-session$dc_region:eu-central-1;exp-session",
}